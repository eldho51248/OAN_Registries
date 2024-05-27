from odoo import api, fields, models


class FarmingType(models.Model):
    _name = 'g2p.farming.type' 

    name = fields.Char(string='Name')
