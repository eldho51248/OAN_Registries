from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    land_information_ids = fields.One2many('land.information',
                                   'partner_id',
                                   string="Land Information")

    crop_information_ids = fields.One2many('crop.information',
                                   'partner_id',
                                   string="Crop Information")

    livestock_information_ids = fields.One2many('live.stock.information',
                                   'partner_id',
                                   string="Live Stock Information")

class LandInformation(models.Model):
    _name = "land.information"


    location = fields.Char(string="Location")
    geolocation = fields.Char(string="Geolocation")
    total_land_area = fields.Char('Total Land Area')
    # total_land_area = fields.Float('Total Land Area')
    ownership_type = fields.Selection(selection=[('owner', 'Owner'),
                                           ('tenant', 'Tenant')],
                                                required=True)
    partner_id = fields.Many2one('res.partner', string="partner")
    



