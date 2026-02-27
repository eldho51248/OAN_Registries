import logging
from datetime import date, datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
CONSENT_WEBSUB_EVENT = "WEBSUB_INDIVIDUAL_UPDATED"


class G2PConsentDataFieldMapLine(models.Model):
    _name = "g2p.consent.data.field.map.line"
    _description = "Consent Data Field Mapping Line"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    data_field_id = fields.Many2one(
        "g2p.consent.data.field",
        required=True,
        ondelete="cascade",
    )
    payload_key = fields.Char(
        help="Optional key to use inside this data field payload. Defaults to the final segment of source path."
    )
    source_path = fields.Char(
        required=True,
        help=(
            "Dot path from farmer (res.partner), e.g. "
            "'region.name' or 'land_information_ids.total_land_area'."
        ),
    )


class G2PConsentDataField(models.Model):
    _inherit = "g2p.consent.data.field"

    payload_key = fields.Char(
        help="Payload key for this data field. Defaults to the field code."
    )
    source_path = fields.Char(
        help=(
            "Optional simple source path from farmer (res.partner). "
            "If empty, the system tries to use code as path."
        ),
    )
    mapping_line_ids = fields.One2many(
        "g2p.consent.data.field.map.line",
        "data_field_id",
        string="Advanced Mapping",
    )


class G2PDatashareConfigWebsubConsent(models.Model):
    _inherit = "g2p.datashare.config.websub"

    @api.model
    def publish_consent_payload(self, payload, config):
        config = config.sudo() if config else self.browse()
        if not config:
            _logger.warning("Consent WebSub - Missing selected WebSub configuration. Skipping publish.")
            return
        if not config.active or config.event_type != CONSENT_WEBSUB_EVENT:
            _logger.warning(
                "Consent WebSub - Selected configuration '%s' is not active or event mismatch (%s).",
                config.display_name,
                CONSENT_WEBSUB_EVENT,
            )
            return
        if self.env.context.get("test_mode"):
            config.publish_event_websub(payload)
            return

        job = config.with_delay()._publish_consent_payload_job(payload)
        _logger.info(
            "Consent WebSub - Enqueued queue job uuid=%s state=%s config_id=%s event=%s",
            getattr(job, "uuid", None),
            getattr(job, "state", None),
            config.id,
            CONSENT_WEBSUB_EVENT,
        )

    def _publish_consent_payload_job(self, payload):
        self.ensure_one()
        self.publish_event_websub(payload)


class G2PConsentRequestWebsub(models.Model):
    _inherit = "g2p.consent.request"

    def _ensure_websub_configuration_before_approval(self):
        for record in self.filtered(lambda rec: rec.status != "approved"):
            partner = record.partner_record_id.sudo()
            partner_name = partner.display_name or _("Unknown Partner")
            config = partner.consent_websub_config_id.sudo()
            if not config:
                raise UserError(
                    _(
                        "WebSub configuration is not selected for partner '%s'. "
                        "Please select a WebSub configuration before approval."
                    )
                    % partner_name
                )
            if config.event_type != CONSENT_WEBSUB_EVENT or not config.active:
                raise UserError(
                    _(
                        "Selected WebSub configuration '%(config)s' is invalid for partner '%(partner)s'. "
                        "Expected an active configuration with event '%(event)s'."
                    )
                    % {
                        "config": config.display_name,
                        "partner": partner_name,
                        "event": CONSENT_WEBSUB_EVENT,
                    }
                )

    def action_approve(self):
        self._ensure_websub_configuration_before_approval()
        old_statuses = {record.id: record.status for record in self}
        result = super().action_approve()
        approved_now = self.filtered(
            lambda rec: old_statuses.get(rec.id) != "approved" and rec.status == "approved"
        )
        approved_now._publish_consent_approved_websub()
        return result

    def _publish_consent_approved_websub(self):
        datashare_obj = self.env["g2p.datashare.config.websub"].sudo()
        for record in self:
            config = record.partner_record_id.sudo().consent_websub_config_id
            payload = record._build_consent_websub_payload()
            if not payload.get("selected_data"):
                _logger.info(
                    "Consent WebSub - Skipping consent %s because selected_data is empty.",
                    record.consent_creation_request_id,
                )
                continue
            try:
                datashare_obj.publish_consent_payload(payload, config)
            except Exception:
                _logger.exception(
                    "Consent WebSub - Failed publishing consent %s.",
                    record.consent_creation_request_id,
                )

    def _build_consent_websub_payload(self):
        self.ensure_one()
        farmer = self.farmer_id.sudo()
        partner = self.partner_record_id.sudo()

        selected_data = {}
        for data_field in self.allowed_data_field_ids:
            payload_key = (data_field.payload_key or data_field.code or data_field.name or "").strip()
            if not payload_key:
                continue
            value = self._extract_data_field_value(data_field, farmer)
            if self._is_empty_payload_value(value):
                continue
            selected_data[payload_key] = value

        now = fields.Datetime.now()
        return {
            "source": "g2p_ati_consent_mgt",
            "event_type": CONSENT_WEBSUB_EVENT,
            "published_at": fields.Datetime.to_string(now),
            "consent": {
                "id": self.id,
                "consent_creation_request_id": self.consent_creation_request_id,
                "consent_type": self.consent_type,
                "status": self.status,
                "approved_at": fields.Datetime.to_string(self.approved_at) if self.approved_at else None,
                "validity_from": fields.Datetime.to_string(self.validity_from) if self.validity_from else None,
                "validity_to": fields.Datetime.to_string(self.validity_to) if self.validity_to else None,
                "requested_field_codes": self.allowed_data_field_ids.mapped("code"),
            },
            "consent_partner": {
                "id": partner.id,
                "name": partner.display_name,
                "ref": partner.ref,
                "websub_config_id": partner.consent_websub_config_id.id,
                "websub_config_name": partner.consent_websub_config_id.display_name,
            },
            "farmer": {
                "id": farmer.id,
                "farmer_id": farmer.farmer_id,
                "name": farmer.display_name,
            },
            "selected_data": selected_data,
        }

    def _extract_data_field_value(self, data_field, farmer):
        mapping_lines = data_field.mapping_line_ids.sorted(key=lambda line: (line.sequence, line.id))
        if mapping_lines:
            collection_payload = self._extract_collection_mapping_payload(mapping_lines, farmer)
            if collection_payload is not None:
                return collection_payload

            payload = {}
            for line in mapping_lines:
                line_value = self._resolve_source_path(farmer, line.source_path)
                if self._is_empty_payload_value(line_value):
                    continue
                key = (line.payload_key or self._fallback_payload_key(line.source_path)).strip()
                if not key:
                    continue
                payload[key] = line_value
            return payload

        source_path = (data_field.source_path or data_field.code or "").strip()
        if not source_path:
            return None
        return self._resolve_source_path(farmer, source_path)

    def _extract_collection_mapping_payload(self, mapping_lines, farmer):
        """Build list[object] payload when all mapping lines target one collection root."""
        root_path_infos = []
        for line in mapping_lines:
            info = self._get_collection_root_info(farmer._name, line.source_path)
            if not info:
                return None
            root_path_infos.append((line, info))

        root_paths = {tuple(info["root_segments"]) for _, info in root_path_infos}
        if len(root_paths) != 1:
            return None

        root_segments = list(next(iter(root_paths)))
        root_values = self._resolve_raw_path_values(farmer, root_segments)
        root_records = [value for value in root_values if isinstance(value, models.BaseModel)]
        if not root_records:
            return []

        rows = []
        for root_record in root_records:
            row = {}
            for line, info in root_path_infos:
                key = (line.payload_key or self._fallback_payload_key(line.source_path)).strip()
                if not key:
                    continue

                remaining_segments = info["remaining_segments"]
                if remaining_segments:
                    line_value = self._resolve_source_path(root_record, ".".join(remaining_segments))
                else:
                    line_value = self._serialize_payload_value(root_record)

                if self._is_empty_payload_value(line_value):
                    continue
                row[key] = line_value

            if row:
                rows.append(row)

        return rows

    def _get_collection_root_info(self, model_name, source_path):
        source_path = (source_path or "").strip()
        if not source_path:
            return None

        segments = [segment.strip() for segment in source_path.split(".") if segment.strip()]
        if not segments:
            return None

        current_model = self.env[model_name]
        root_segments = []
        for idx, segment in enumerate(segments):
            field = current_model._fields.get(segment)
            if not field:
                return None

            root_segments.append(segment)
            if field.type in ("one2many", "many2many"):
                return {
                    "root_segments": root_segments,
                    "remaining_segments": segments[idx + 1 :],
                }

            if field.type == "many2one":
                current_model = self.env[field.comodel_name]
                continue

            return None

        return None

    def _resolve_raw_path_values(self, source_record, segments):
        values = [source_record]
        for segment in segments:
            next_values = []
            for value in values:
                if isinstance(value, models.BaseModel):
                    if not value or segment not in value._fields:
                        continue
                    field = value._fields[segment]
                    field_value = value[segment]
                    if field.type in ("one2many", "many2many"):
                        if field_value:
                            next_values.extend(field_value)
                    elif field.type == "many2one":
                        if field_value:
                            next_values.append(field_value)
                    else:
                        next_values.append(field_value)
                elif isinstance(value, dict):
                    if segment in value:
                        next_values.append(value.get(segment))

            values = next_values
            if not values:
                return []

        return values

    def _fallback_payload_key(self, source_path):
        if not source_path:
            return ""
        return source_path.split(".")[-1].strip()

    def _resolve_source_path(self, farmer, source_path):
        source_path = (source_path or "").strip()
        if not source_path:
            return None

        segments = [segment.strip() for segment in source_path.split(".") if segment.strip()]
        if not segments:
            return None

        values = [farmer]
        force_list = False

        for segment in segments:
            next_values = []
            for value in values:
                if isinstance(value, models.BaseModel):
                    if not value or segment not in value._fields:
                        continue
                    field = value._fields[segment]
                    field_value = value[segment]
                    if field.type in ("one2many", "many2many"):
                        force_list = True
                        if field_value:
                            next_values.extend(field_value)
                    elif field.type == "many2one":
                        if field_value:
                            next_values.append(field_value)
                    else:
                        next_values.append(field_value)
                elif isinstance(value, dict):
                    if segment in value:
                        next_values.append(value.get(segment))
            values = next_values
            if not values:
                return [] if force_list else None

        serialized = []
        for value in values:
            serialized_value = self._serialize_payload_value(value)
            if self._is_empty_payload_value(serialized_value):
                continue
            serialized.append(serialized_value)

        if not serialized:
            return [] if force_list else None
        if force_list:
            return serialized
        if len(serialized) == 1:
            return serialized[0]
        return serialized

    def _serialize_payload_value(self, value):
        if isinstance(value, models.BaseModel):
            if len(value) > 1:
                return [self._serialize_payload_value(rec) for rec in value]
            if not value:
                return None
            record = value[0]
            payload = {
                "id": record.id,
                "name": record.display_name,
            }
            if "code" in record._fields and record.code:
                payload["code"] = record.code
            return payload
        if isinstance(value, datetime):
            return fields.Datetime.to_string(value)
        if isinstance(value, date):
            return fields.Date.to_string(value)
        if isinstance(value, dict):
            return {k: self._serialize_payload_value(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._serialize_payload_value(v) for v in value]
        return value

    def _is_empty_payload_value(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (list, tuple, set, dict)):
            return len(value) == 0
        return False
