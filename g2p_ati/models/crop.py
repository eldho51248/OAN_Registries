from odoo import api, models, fields


class CropCategory(models.Model):
    _name = 'crop.category'

    name = fields.Char(
        string='Name',
    )
    

class G2PCrop(models.Model):
    _name = 'g2p.crop'
    _description = 'Crop Information Model'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    category = fields.Many2one('crop.category', string='Category')
    name = fields.Char(string='Crop')


class CropVariety(models.Model):
    _name = 'crop.variety'
    
    name = fields.Char(string='Name')



