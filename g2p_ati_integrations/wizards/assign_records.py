from odoo import _, fields, models
from odoo.exceptions import UserError


class G2PAssignRecordsWizard(models.TransientModel):
    _name = "assign.records.wizard"

    assigned_region = fields.Many2one("g2p.region")
    language_skills = fields.Many2many("g2p.lang", string="Languages")

    def assign_groups(self):
        domain = []
        if not self.assigned_region and not self.language_skills:
            raise UserError(_("Please Select at leaste one of the fields"))

        if self.assigned_region:
            domain.append(("asigned_region", "=", self.assigned_region.id))

        if self.language_skills:
            domain.append(("language_skills", "in", self.language_skills.ids))
        # Fetch partner records that match the domain
        partners = self.env["res.partner"].search(domain)
        active_ids = self._context["active_ids"]
        records = self.env["g2p.imported.record"].browse(active_ids)
        partner_ids = partners.mapped("id")
        # Assign the users as followers
        for record in records:
            record.message_subscribe(partner_ids=partner_ids)
        return partners.ids
