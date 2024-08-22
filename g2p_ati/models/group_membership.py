from odoo import models


class G2PGroupMembershipInherited(models.Model):
    _inherit = "g2p.group.membership"

    def open_individual_form(self):
        return {
            "name": "Individual Member",
            "view_mode": "form",
            "mode": "primary",
            "res_model": "res.partner",
            "res_id": self.individual.id,
            "view_id": self.env.ref("g2p_ati.g2p_registry_individual_form_view_inherit").id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_is_group": False},
            "flags": {"mode": "readonly"},
        }
