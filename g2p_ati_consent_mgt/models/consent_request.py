import json
from uuid import uuid4

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class G2PConsentRequest(models.Model):
    _name = "g2p.consent.request"
    _description = "Consent Request"
    _order = "create_date desc"

    name = fields.Char(compute="_compute_name", store=True)
    consent_creation_request_id = fields.Char(required=True, default=lambda self: str(uuid4()), copy=False, index=True)
    consent_type = fields.Selection(
        [("baseline", "Baseline"), ("specific", "Specific")],
        required=True,
        default="specific",
    )
    partner_record_id = fields.Many2one(
        "res.partner",
        required=True,
        string="Partner",
        domain="[('is_consent_parent', '=', True)]",
    )
    partner_id = fields.Char(string="Partner ID", compute="_compute_partner_id", store=True, readonly=True)
    partner_code = fields.Char(related="partner_record_id.ref", string="Partner Code", store=True, readonly=True)
    farmer_id = fields.Many2one(
        "res.partner",
        string="Farmer",
        required=True,
        domain="[('is_registrant', '=', True), ('is_group', '=', False), ('is_farmer', '=', 'yes')]",
    )
    allowed_data_field_ids = fields.Many2many(
        "g2p.consent.data.field",
        "g2p_consent_request_data_field_rel",
        "consent_id",
        "field_id",
        string="Allowed Data Points",
        help="Requested fields for this consent.",
    )
    consent_provider_register = fields.Char()
    consent_provider_person_id = fields.Char()
    consent_target_object_ids = fields.Text(help='JSON list[dict], e.g. [{"register": ["<ids>"]}]')
    attribute_lists = fields.Text(help='JSON list[dict], e.g. [{"register": ["<fields>"]}]')
    purpose = fields.Text()
    validity_from = fields.Datetime(string="Valid From")
    validity_to = fields.Datetime(string="Valid Until")
    originated_from = fields.Selection(
        [
            ("beneficiary", "Beneficiary"),
            ("agent", "Agent"),
            ("staff", "Staff"),
            ("partner", "Partner"),
        ]
    )
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("revoked", "Revoked"),
            ("denied", "Denied"),
            ("expired", "Expired"),
        ],
        default="pending",
        required=True,
    )
    created_at = fields.Datetime(default=fields.Datetime.now, readonly=True)
    approved_at = fields.Datetime(readonly=True)
    rejected_at = fields.Datetime(readonly=True)
    expired_at = fields.Datetime(readonly=True)
    rejection_reason = fields.Text()
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "g2p_consent_request_attachment_rel",
        "consent_id",
        "attachment_id",
        string="Consent Attachments",
    )

    _sql_constraints = [
        (
            "g2p_consent_creation_request_id_uniq",
            "unique(consent_creation_request_id)",
            "Consent creation request ID must be unique.",
        ),
    ]

    @api.depends("farmer_id", "partner_record_id")
    def _compute_name(self):
        for rec in self:
            farmer_label = rec.farmer_id.display_name or _("Unknown Farmer")
            partner_label = rec.partner_record_id.display_name or _("Unknown Partner")
            rec.name = f"{farmer_label} - {partner_label}"

    @api.depends("partner_record_id")
    def _compute_partner_id(self):
        for rec in self:
            rec.partner_id = str(rec.partner_record_id.id) if rec.partner_record_id else False

    @api.constrains("validity_from", "validity_to")
    def _check_validity_range(self):
        for rec in self:
            if rec.validity_from and rec.validity_to and rec.validity_from > rec.validity_to:
                raise ValidationError(_("Valid From must be earlier than or equal to Valid Until."))

    def _set_status(self, status, timestamp_field=None):
        vals = {"status": status}
        if timestamp_field:
            vals[timestamp_field] = fields.Datetime.now()
        self.write(vals)

    def _build_attribute_lists_payload(self) -> str:
        self.ensure_one()
        tokens = []
        for data_field in self.allowed_data_field_ids:
            token = (data_field.code or data_field.name or "").strip()
            if token:
                tokens.append(token)
        tokens = list(dict.fromkeys(tokens))
        if not tokens:
            return "[]"
        return json.dumps([{"register": tokens}], ensure_ascii=False)

    def _extract_attribute_tokens(self) -> list[str]:
        self.ensure_one()
        raw = (self.attribute_lists or "").strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return []
        if not isinstance(parsed, list):
            return []
        tokens: list[str] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            for value in item.values():
                if isinstance(value, list):
                    tokens.extend([str(v).strip() for v in value if str(v).strip()])
                elif value is not None and str(value).strip():
                    tokens.append(str(value).strip())
        return list(dict.fromkeys(tokens))

    def _sync_attribute_lists_from_allowed_fields(self):
        for rec in self:
            payload = rec._build_attribute_lists_payload()
            if rec.attribute_lists != payload:
                rec.with_context(_skip_attribute_lists_sync=True).write({"attribute_lists": payload})

    def _sync_allowed_fields_from_attribute_lists(self):
        data_field_model = self.env["g2p.consent.data.field"]
        for rec in self:
            tokens = rec._extract_attribute_tokens()
            current_ids = set(rec.allowed_data_field_ids.ids)
            if not tokens:
                if current_ids:
                    rec.with_context(_skip_attribute_lists_sync=True).write({"allowed_data_field_ids": [(5, 0, 0)]})
                continue
            by_code = data_field_model.search([("code", "in", tokens)])
            remaining = [t for t in tokens if t not in set(by_code.mapped("code"))]
            by_name = data_field_model.search([("name", "in", remaining)]) if remaining else data_field_model.browse()
            target_ids = set((by_code | by_name).ids)
            if current_ids != target_ids:
                rec.with_context(_skip_attribute_lists_sync=True).write({"allowed_data_field_ids": [(6, 0, list(target_ids))]})

    @api.onchange("allowed_data_field_ids")
    def _onchange_allowed_data_field_ids_sync_attribute_lists(self):
        self._sync_attribute_lists_from_allowed_fields()

    @api.onchange("attribute_lists")
    def _onchange_attribute_lists_sync_allowed_fields(self):
        self._sync_allowed_fields_from_attribute_lists()

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("_skip_attribute_lists_sync"):
            return super().create(vals_list)
        records = super().create(vals_list)
        for rec, vals in zip(records, vals_list):
            if "allowed_data_field_ids" in vals and "attribute_lists" not in vals:
                rec._sync_attribute_lists_from_allowed_fields()
            elif "attribute_lists" in vals and "allowed_data_field_ids" not in vals:
                rec._sync_allowed_fields_from_attribute_lists()
            elif "allowed_data_field_ids" in vals and "attribute_lists" in vals:
                rec._sync_attribute_lists_from_allowed_fields()
        return records

    def write(self, vals):
        if self.env.context.get("_skip_attribute_lists_sync"):
            return super().write(vals)
        result = super().write(vals)
        if "allowed_data_field_ids" in vals and "attribute_lists" not in vals:
            self._sync_attribute_lists_from_allowed_fields()
        elif "attribute_lists" in vals and "allowed_data_field_ids" not in vals:
            self._sync_allowed_fields_from_attribute_lists()
        elif "allowed_data_field_ids" in vals and "attribute_lists" in vals:
            self._sync_attribute_lists_from_allowed_fields()
        return result

    def action_approve(self):
        self._set_status("approved", "approved_at")

    def action_reject(self):
        self._set_status("rejected", "rejected_at")

    def action_revoke(self):
        self._set_status("revoked", "expired_at")

    def action_expire(self):
        self._set_status("expired", "expired_at")
