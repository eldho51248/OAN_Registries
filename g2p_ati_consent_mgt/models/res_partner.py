from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_consent_parent = fields.Boolean(string="Consent Parent", default=False, index=True)
    consent_portal_user_ids = fields.One2many(
        "res.users",
        "consent_parent_partner_id",
        string="Portal Users",
    )
    consent_portal_user_count = fields.Integer(
        string="Portal Users",
        compute="_compute_consent_portal_user_count",
    )

    @api.depends("consent_portal_user_ids")
    def _compute_consent_portal_user_count(self):
        grouped_data = self.env["res.users"].sudo().read_group(
            [("consent_parent_partner_id", "in", self.ids)],
            ["consent_parent_partner_id"],
            ["consent_parent_partner_id"],
        )
        counts = {
            item["consent_parent_partner_id"][0]: item["consent_parent_partner_id_count"]
            for item in grouped_data
        }
        for partner in self:
            partner.consent_portal_user_count = counts.get(partner.id, 0)

    def action_open_consent_portal_users(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Portal Users"),
            "res_model": "res.users",
            "view_mode": "tree,form",
            "domain": [("consent_parent_partner_id", "=", self.id)],
            "context": {"default_consent_parent_partner_id": self.id},
        }

    def action_open_create_portal_user_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Portal User"),
            "res_model": "g2p.ati.create.portal.user.wizard",
            "view_mode": "form",
            "view_id": self.env.ref(
                "g2p_ati_consent_mgt.view_g2p_ati_create_portal_user_wizard_form"
            ).id,
            "target": "new",
            "context": {"default_parent_partner_id": self.id},
        }

