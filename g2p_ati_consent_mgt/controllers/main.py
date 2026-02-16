import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class G2PATIConsentController(http.Controller):
    def _error(self, message, code=400):
        return {"success": False, "code": code, "message": message}

    def _success(self, data=None, message="OK"):
        return {"success": True, "message": message, "data": data or {}}

    def _find_farmer(self, payload):
        partner_obj = request.env["res.partner"].sudo()

        farmer_db_id = payload.get("farmer_db_id")
        farmer_id = payload.get("farmer_id")
        national_id = payload.get("national_id")

        if farmer_db_id:
            return partner_obj.search(
                [("id", "=", int(farmer_db_id)), ("is_registrant", "=", True), ("is_group", "=", False)],
                limit=1,
            )
        if farmer_id:
            return partner_obj.search(
                [("farmer_id", "=", farmer_id), ("is_registrant", "=", True), ("is_group", "=", False)],
                limit=1,
            )
        if national_id:
            return partner_obj.search(
                [("reg_ids.value", "=", national_id), ("is_registrant", "=", True), ("is_group", "=", False)],
                limit=1,
            )

        return partner_obj.browse()

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
