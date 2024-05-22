from odoo import api, fields, models, _

class CropInformation(models.Model):
    _name = "crop.information"

    partner_id = fields.Many2one('res.partner', string="partner")

    crop = fields.Many2one('g2p.crop',string="Crop")
    variety = fields.Many2one('crop.variety', string='Crop Variety')
    illness_type = fields.Many2many('crop.illness.type', string='Illness Type')
    illness_images = fields.Many2many('ir.attachment', string="illness images")



class CropIllnessType(models.Model):
    _name = "crop.illness.type"

    name = fields.Char(string="Name")


    