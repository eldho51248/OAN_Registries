from odoo import api, fields, models
from odoo.exceptions import ValidationError


class G2PLandInformation(models.Model):
    _name = "g2p.land.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer", required=True, index=True)
    farmer_id = fields.Char(related="partner_id.farmer_id", string="Farmer ID", readonly=True)
    total_land_area = fields.Float(string="Area In Hectare", required=True, default=0.0)
    land_certificate = fields.Many2one("storage.file")
    land_id = fields.Char(string="Land ID", index=True)
    ownership_type = fields.Selection(selection=[("owner", "Owner"), ("tenant", "Tenant")], required=True)
    slug = fields.Char()

    @api.onchange("total_land_area")
    def _onchange_total_land_area(self):
        if self.total_land_area < 0.0:
            error_msg = "Area should not be negative"
            raise ValidationError(error_msg)

    @api.model
    def create(self, vals):
        if "land_certificate" in vals:
            storage_file = self.env["storage.file"].browse(vals["land_certificate"])
            if storage_file:
                vals["slug"] = storage_file.slug
        return super().create(vals)

    def write(self, vals):
        if "land_certificate" in vals:
            storage_file = self.env["storage.file"].browse(vals["land_certificate"])
            if storage_file:
                vals["slug"] = storage_file.slug
        return super().write(vals)
