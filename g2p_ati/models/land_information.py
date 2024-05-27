from odoo import fields, models


class LandInformation(models.Model):
    _name = "land.information"

    location = fields.Char()
    geolocation = fields.Char()
    total_land_area = fields.Char()
    # total_land_area = fields.Float('Total Land Area')
    ownership_type = fields.Selection(selection=[("owner", "Owner"), ("tenant", "Tenant")], required=True)
    partner_id = fields.Many2one("res.partner", string="partner")
