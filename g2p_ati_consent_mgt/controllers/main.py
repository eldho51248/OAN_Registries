import base64
import logging
from datetime import datetime, timedelta

from odoo import fields, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class G2PATIConsentController(http.Controller):
    _MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10MB

    def _error(self, message, code=400):
        return {"success": False, "code": code, "message": message}

    def _success(self, data=None, message="OK"):
        return {"success": True, "message": message, "data": data or {}}

    def _get_consent_partner(self):
        """Return the consent parent partner for the current portal user, or None."""
        user = request.env.user
        if not user.consent_parent_partner_id:
            return None
        return user.consent_parent_partner_id

    def _find_farmer(self, payload):
        """Find farmer by farmer_db_id, farmer_id, or national_id/UID.
        
        Uses multiple search strategies similar to SQL approach:
        - Partner ID (farmer_db_id)
        - farmer_id field
        - unique_id field
        - reg_ids.value (any ID type for national_id, UID type for UID)
        """
        partner_obj = request.env["res.partner"].sudo()
        reg_id_obj = request.env["g2p.reg.id"].sudo()

        base_domain = [("is_registrant", "=", True), ("is_group", "=", False)]
        
        farmer_db_id = payload.get("farmer_db_id")
        farmer_id = payload.get("farmer_id")
        national_id = payload.get("national_id")

        if farmer_db_id:
            return partner_obj.search(
                base_domain + [("id", "=", int(farmer_db_id))],
                limit=1,
            )
        if farmer_id:
            return partner_obj.search(
                base_domain + [("farmer_id", "=", farmer_id)],
                limit=1,
            )
        if national_id:
            search_value = str(national_id).strip()
            partner_ids = set()
            
            # Search by unique_id
            farmers = partner_obj.search(base_domain + [("unique_id", "=", search_value)], limit=1)
            if farmers:
                return farmers[0]
            
            # Search by reg_ids.value (any ID type)
            reg_ids = reg_id_obj.search([("value", "=", search_value)], limit=100)
            if reg_ids:
                partner_ids.update(reg_ids.mapped("partner_id").ids)
                farmers = partner_obj.search(
                    base_domain + [("id", "in", list(partner_ids))], limit=1
                )
                if farmers:
                    return farmers[0]

        return partner_obj.browse()

    # -------------------------------------------------------------------------
    # Portal: consent management page and farmer search
    # -------------------------------------------------------------------------

    @http.route("/consent/management", type="http", auth="user", website=True)
    def consent_management_page(self, **kw):
        partner = self._get_consent_partner()
        if not partner:
            return request.redirect("/my")
        ConsentRequest = request.env["g2p.consent.request"].sudo()
        requests_domain = [("partner_record_id", "=", partner.id)]
        consent_requests = ConsentRequest.search(requests_domain, order="create_date desc", limit=200)
        data_fields = partner.allowed_data_field_ids or request.env["g2p.consent.data.field"].sudo().search([("active", "=", True)])
        review_request = request.env["g2p.consent.request"].browse()
        review_id = kw.get("review_id") or request.params.get("review_id")
        if review_id:
            try:
                review_id = int(review_id)
            except (TypeError, ValueError):
                review_id = 0
            if review_id:
                review_request = ConsentRequest.search(
                    [("id", "=", review_id), ("partner_record_id", "=", partner.id)],
                    limit=1,
                )
        return request.render(
            "g2p_ati_consent_mgt.portal_consent_management",
            {
                "consent_partner": partner,
                "consent_requests": consent_requests,
                "data_fields": data_fields,
                "review_request": review_request,
            },
        )

    @http.route("/consent/management/review/<int:review_id>", type="http", auth="user", website=True)
    def consent_management_page_review(self, review_id, **kw):
        kw["review_id"] = review_id
        return self.consent_management_page(**kw)

    @http.route("/consent/request/<int:consent_id>/capture_image", type="http", auth="user")
    def consent_request_capture_image(self, consent_id, **kw):
        partner = self._get_consent_partner()
        if not partner:
            return request.not_found()

        consent = request.env["g2p.consent.request"].sudo().search(
            [("id", "=", consent_id), ("partner_record_id", "=", partner.id)],
            limit=1,
        )
        if not consent or not consent.portal_capture_image:
            return request.not_found()

        try:
            image_data = base64.b64decode(consent.portal_capture_image)
        except Exception:
            return request.not_found()

        headers = [
            ("Content-Type", "image/jpeg"),
            ("Content-Length", str(len(image_data))),
        ]
        return request.make_response(image_data, headers=headers)

    @http.route("/consent/search_farmer", type="json", auth="user")
    def consent_search_farmer(self, farmer_id=None, national_id=None, uid=None, query=None, **kw):
        """Search by Farmer ID or UID only. No is_registrant/is_group filter so portal always finds matches."""
        if not self._get_consent_partner():
            return self._error("Access denied", code=403)
        
        search_value = None
        if query and str(query).strip():
            search_value = str(query).strip()
        elif farmer_id and str(farmer_id).strip():
            search_value = str(farmer_id).strip()
        elif national_id and str(national_id).strip():
            search_value = str(national_id).strip()
        elif uid and str(uid).strip():
            search_value = str(uid).strip()
        if not search_value:
            return self._error("Provide farmer_id, national_id, uid, or query")
        
        partner_obj = request.env["res.partner"].sudo()
        reg_id_obj = request.env["g2p.reg.id"].sudo()
        partner_ids = set()
        
        # 1) By farmer_id
        for p in partner_obj.search([("farmer_id", "=", search_value)], limit=10):
            partner_ids.add(p.id)
        # 2) By unique_id
        for p in partner_obj.search([("unique_id", "=", search_value)], limit=10):
            partner_ids.add(p.id)
        # 3) By reg_ids.value (IDs tab – UID / ID Number) – direct from g2p.reg.id, no partner domain
        for reg in reg_id_obj.search([("value", "=", search_value)], limit=100):
            if reg.partner_id:
                partner_ids.add(reg.partner_id.id)
        
        if not partner_ids:
            return self._success(data={"farmers": []})
        
        farmers = partner_obj.browse(sorted(partner_ids)[:10])
        return self._success(
            data={
                "farmers": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "farmer_id": p.farmer_id or "",
                        "reg_ids": [r.value for r in (p.reg_ids or [])],
                    }
                    for p in farmers
                ]
            }
        )

    @http.route("/consent/request/submit", type="http", auth="user", methods=["POST"], csrf=True)
    def consent_request_submit(self, **post):
        """Create a consent request from portal form (with optional attachment)."""
        try:
            partner = self._get_consent_partner()
            if not partner:
                return request.redirect("/consent/management?error=access_denied")
            
            farmer_id = post.get("farmer_id")
            if not farmer_id:
                return request.redirect("/consent/management?error=missing_farmer")
            
            try:
                farmer_id = int(farmer_id)
            except (TypeError, ValueError):
                return request.redirect("/consent/management?error=invalid_farmer")
            
            farmer = request.env["res.partner"].sudo().browse(farmer_id)
            if not farmer.exists() or farmer.is_group:
                return request.redirect("/consent/management?error=farmer_not_found")
            
            consent_type = post.get("consent_type", "specific") or "specific"
            purpose = (post.get("purpose") or "").strip()
            if not purpose:
                return request.redirect("/consent/management?error=missing_purpose")
            validity_months = post.get("validity_months")
            try:
                validity_months = int(validity_months) if validity_months else 12
            except (TypeError, ValueError):
                validity_months = 12
            
            form_data = request.httprequest.form or {}
            allowed_data_field_ids = form_data.getlist("allowed_data_field_ids") if hasattr(form_data, "getlist") else []
            if not allowed_data_field_ids and post.get("allowed_data_field_ids"):
                # Fallback for edge cases where only kwargs are populated.
                allowed_data_field_ids = [post.get("allowed_data_field_ids")]
            allowed_ids = []
            for fid in allowed_data_field_ids:
                try:
                    allowed_ids.append(int(fid))
                except (TypeError, ValueError):
                    pass
            
            if partner.allowed_data_field_ids:
                allowed_ids = [i for i in allowed_ids if i in partner.allowed_data_field_ids.ids]
            if not allowed_ids:
                return request.redirect("/consent/management?error=missing_data_fields")
            
            now = fields.Datetime.now()
            validity_from = now
            validity_to = now + timedelta(days=validity_months * 30)
            
            vals = {
                "partner_record_id": partner.id,
                "farmer_id": farmer_id,
                "consent_type": consent_type,
                "purpose": purpose,
                "validity_from": validity_from,
                "validity_to": validity_to,
                "originated_from": "partner",
                "status": "pending",
            }
            
            if allowed_ids:
                vals["allowed_data_field_ids"] = [(6, 0, allowed_ids)]
            
            attachment_ids = []
            try:
                files = request.httprequest.files or {}
                upload = files.get("attachment")
                if not upload or not getattr(upload, "filename", None):
                    return request.redirect("/consent/management?error=missing_attachment")

                upload_data = upload.read()
                if not upload_data:
                    return request.redirect("/consent/management?error=missing_attachment")
                if len(upload_data) > self._MAX_ATTACHMENT_SIZE:
                    return request.redirect("/consent/management?error=attachment_too_large")

                Attachment = request.env["ir.attachment"].sudo()
                att = Attachment.create(
                    {
                        "name": upload.filename or "consent_form.pdf",
                        "datas": base64.b64encode(upload_data),
                        "res_model": "g2p.consent.request",
                        "res_id": 0,
                    }
                )
                attachment_ids.append(att.id)
                vals["attachment_ids"] = [(6, 0, attachment_ids)]

                camera_data_b64 = (post.get("camera_capture_data") or "").strip()
                if camera_data_b64:
                    if "," in camera_data_b64:
                        camera_data_b64 = camera_data_b64.split(",", 1)[1]
                    try:
                        camera_data = base64.b64decode(camera_data_b64, validate=True)
                    except Exception:
                        return request.redirect("/consent/management?error=invalid_camera_data")
                    if len(camera_data) > self._MAX_ATTACHMENT_SIZE:
                        return request.redirect("/consent/management?error=camera_too_large")
                    vals["portal_capture_image"] = base64.b64encode(camera_data)
                    vals["portal_capture_image_filename"] = "camera_capture.jpg"
                    capture_ts_raw = (post.get("camera_capture_taken_at") or "").strip()
                    if capture_ts_raw:
                        capture_dt = fields.Datetime.to_datetime(capture_ts_raw)
                        if not capture_dt:
                            return request.redirect("/consent/management?error=invalid_camera_timestamp")
                        vals["portal_capture_taken_at"] = fields.Datetime.to_string(capture_dt)
            except Exception as e:
                _logger.error("Error processing attachments/camera capture: %s", e, exc_info=True)
                return request.redirect("/consent/management?error=server_error")
            
            ConsentRequest = request.env["g2p.consent.request"].sudo()
            consent = ConsentRequest.create(vals)

            for att_id in attachment_ids:
                request.env["ir.attachment"].sudo().browse(att_id).write({"res_id": consent.id})
            
            _logger.info(
                "Consent request created via portal: id=%s farmer_id=%s partner_id=%s",
                consent.id,
                consent.farmer_id.id,
                consent.partner_record_id.id,
            )
            return request.redirect("/consent/management?success=1")
        except Exception as e:
            _logger.error("Error creating consent request: %s", e, exc_info=True)
            return request.redirect("/consent/management?error=server_error")

    @http.route("/api/consent/request/create", type="json", auth="user", methods=["POST"], csrf=False)
    def create_consent_request(self, **kwargs):
        payload = request.jsonrequest or {}
        partner_record_id = payload.get("partner_record_id") or payload.get("partner_id")

        if not partner_record_id:
            return self._error("partner_id is required")

        farmer = self._find_farmer(payload)
        if not farmer:
            return self._error("Farmer not found. Provide farmer_db_id, farmer_id or national_id")

        partner_record = request.env["res.partner"].sudo().browse(int(partner_record_id))
        if not partner_record.exists() or not partner_record.is_consent_parent:
            return self._error("Consent partner not found")
        if not partner_record.active:
            return self._error("Consent partner is inactive")

        vals = {
            "partner_record_id": partner_record.id,
            "farmer_id": farmer.id,
            "consent_type": payload.get("consent_type", "specific"),
            "consent_provider_register": payload.get("consent_provider_register"),
            "consent_provider_person_id": payload.get("consent_provider_person_id"),
            "consent_target_object_ids": payload.get("consent_target_object_ids"),
            "attribute_lists": payload.get("attribute_lists"),
            "purpose": payload.get("purpose"),
            "originated_from": payload.get("originated_from"),
            "validity_from": payload.get("validity_from"),
            "validity_to": payload.get("validity_to"),
            "rejection_reason": payload.get("rejection_reason"),
        }

        if payload.get("consent_creation_request_id"):
            vals["consent_creation_request_id"] = payload.get("consent_creation_request_id")

        allowed_data_field_ids = payload.get("allowed_data_field_ids") or []
        if allowed_data_field_ids:
            vals["allowed_data_field_ids"] = [(6, 0, allowed_data_field_ids)]

        consent = request.env["g2p.consent.request"].sudo().create(vals)

        _logger.info(
            "Consent request created via API: id=%s request_id=%s farmer_id=%s partner_id=%s",
            consent.id,
            consent.consent_creation_request_id,
            consent.farmer_id.id,
            consent.partner_record_id.id,
        )

        return self._success(
            {
                "id": consent.id,
                "consent_creation_request_id": consent.consent_creation_request_id,
                "status": consent.status,
            },
            message="Consent request created",
        )

    @http.route("/api/consent/request/approve", type="json", auth="user", methods=["POST"], csrf=False)
    def approve_consent_request(self, **kwargs):
        payload = request.jsonrequest or {}
        consent_id = payload.get("consent_id")
        consent_request_id = payload.get("consent_creation_request_id")

        domain = []
        if consent_id:
            domain = [("id", "=", int(consent_id))]
        elif consent_request_id:
            domain = [("consent_creation_request_id", "=", consent_request_id)]
        else:
            return self._error("Provide consent_id or consent_creation_request_id")

        consent = request.env["g2p.consent.request"].sudo().search(domain, limit=1)
        if not consent:
            return self._error("Consent request not found", code=404)

        consent.action_approve()
        return self._success(
            {
                "id": consent.id,
                "consent_creation_request_id": consent.consent_creation_request_id,
                "status": consent.status,
            },
            message="Consent request approved",
        )

    @http.route("/api/consent/request/reject", type="json", auth="user", methods=["POST"], csrf=False)
    def reject_consent_request(self, **kwargs):
        payload = request.jsonrequest or {}
        consent_id = payload.get("consent_id")
        consent_request_id = payload.get("consent_creation_request_id")

        domain = []
        if consent_id:
            domain = [("id", "=", int(consent_id))]
        elif consent_request_id:
            domain = [("consent_creation_request_id", "=", consent_request_id)]
        else:
            return self._error("Provide consent_id or consent_creation_request_id")

        consent = request.env["g2p.consent.request"].sudo().search(domain, limit=1)
        if not consent:
            return self._error("Consent request not found", code=404)

        rejection_reason = payload.get("rejection_reason")
        if rejection_reason:
            consent.write({"rejection_reason": rejection_reason})

        consent.action_reject()
        return self._success(
            {
                "id": consent.id,
                "consent_creation_request_id": consent.consent_creation_request_id,
                "status": consent.status,
            },
            message="Consent request rejected",
        )

    @http.route("/api/consent/request/revoke", type="json", auth="user", methods=["POST"], csrf=False)
    def revoke_consent_request(self, **kwargs):
        payload = request.jsonrequest or {}
        consent_id = payload.get("consent_id")
        consent_request_id = payload.get("consent_creation_request_id")

        domain = []
        if consent_id:
            domain = [("id", "=", int(consent_id))]
        elif consent_request_id:
            domain = [("consent_creation_request_id", "=", consent_request_id)]
        else:
            return self._error("Provide consent_id or consent_creation_request_id")

        consent = request.env["g2p.consent.request"].sudo().search(domain, limit=1)
        if not consent:
            return self._error("Consent request not found", code=404)

        consent.action_revoke()
        return self._success(
            {
                "id": consent.id,
                "consent_creation_request_id": consent.consent_creation_request_id,
                "status": consent.status,
            },
            message="Consent request revoked",
        )

    @http.route("/api/consent/request/pending", type="json", auth="user", methods=["POST"], csrf=False)
    def list_pending_consent_requests(self, **kwargs):
        payload = request.jsonrequest or {}
        limit = int(payload.get("limit", 80))

        consents = request.env["g2p.consent.request"].sudo().search([("status", "=", "pending")], limit=limit)
        return self._success(
            {
                "count": len(consents),
                "items": [
                    {
                        "id": consent.id,
                        "consent_creation_request_id": consent.consent_creation_request_id,
                        "farmer_id": consent.farmer_id.id,
                        "farmer_name": consent.farmer_id.display_name,
                        "partner_id": consent.partner_record_id.id,
                        "partner_name": consent.partner_record_id.name,
                        "status": consent.status,
                    }
                    for consent in consents
                ],
            }
        )
