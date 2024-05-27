from odoo import api, models, fields


class LivestockType(models.Model):
    _name = 'g2p.livestock.type'

    name = fields.Char(string='Name')
    


class LivestockBreed(models.Model):
    _name = 'g2p.livestock.breed'
    
    name = fields.Char(string='Name')
    


