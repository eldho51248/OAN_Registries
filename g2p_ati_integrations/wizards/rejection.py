import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class RejectWizard(models.TransientModel):
    _inherit = "reject.wizard"

    def confirm_rejection(self):
        result = super().confirm_rejection()

        active_ids = self._context.get("active_ids")
        if not active_ids:
            return result

        record = self.env["draft.record"].browse(active_ids[0])
        if not record:
            return result

        activities = self.sudo().env["mail.activity"].search(
            [("res_model", "=", "draft.record"), ("res_id", "=", record.id)]
        )
        if activities:
            activities.action_done()

        if record.create_uid and record.create_uid.partner_id:
            owner_partner = record.create_uid.partner_id
            record.sudo().message_subscribe(partner_ids=[owner_partner.id])
            record.sudo().message_post(
                body=f"Your draft record was rejected: {self.rejection_reason}",
                subject="Record Rejected",
                message_type="notification",
                partner_ids=[owner_partner.id],
            )

        return result
