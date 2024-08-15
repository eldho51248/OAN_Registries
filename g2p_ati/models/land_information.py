from odoo import api, fields, models
from odoo.exceptions import ValidationError


class G2PLandInformation(models.Model):
    _name = "g2p.land.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer", required=True)
    total_land_area = fields.Float(string="Area In Hectare", required=True, default=0.0)
    land_certificate = fields.Many2one("storage.file")
    land_id = fields.Char(string="Land ID")
    ownership_type = fields.Selection(selection=[("owner", "Owner"), ("tenant", "Tenant")], required=True)


    @api.onchange("total_land_area")
    def _onchange_total_land_area(self):
        if self.total_land_area < 0.0:
            error_msg = "Area should not be negative"
            raise ValidationError(error_msg)
