from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    consent_parent_partner_id = fields.Many2one(
        "res.partner",
        string="Parent Partner",
        index=True,
        domain=[("is_consent_parent", "=", True)],
    )

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        users._sync_partner_parent_from_consent_parent()
        return users

    def write(self, vals):
        result = super().write(vals)
        if {"partner_id", "consent_parent_partner_id"} & set(vals):
            self._sync_partner_parent_from_consent_parent()
        return result

    def _sync_partner_parent_from_consent_parent(self):
        for user in self.filtered(lambda rec: rec.partner_id and rec.consent_parent_partner_id):
            if user.partner_id.parent_id != user.consent_parent_partner_id:
                user.partner_id.sudo().write({"parent_id": user.consent_parent_partner_id.id})

