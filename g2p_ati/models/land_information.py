from odoo import fields, models


class G2PLandInformation(models.Model):
    _name = "g2p.land.information"

    # location = fields.Char()
    # geolocation = fields.Char()
    total_land_area = fields.Float(string='Size In Hectare')
    land_certificate = fields.Many2one('storage.file', string='Land Certificate')
    # total_land_area = fields.Float('Total Land Area')
    ownership_type = fields.Selection(selection=[("owner", "Owner"), ("tenant", "Tenant")], required=True)
    partner_id = fields.Many2one("res.partner", string="partner")
