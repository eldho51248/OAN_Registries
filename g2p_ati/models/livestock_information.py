from odoo import api, fields, models


class LIveStockInformation(models.Model):
    _name = "live.stock.information"

    partner_id = fields.Many2one('res.partner', string="partner")

    # livestock_type = fields.Char(string="Livestock Type")
    livestock_type = fields.Many2one('g2p.livestock.type', string='Livestock Type')

    # livestock_bred = fields.Char(string="Breed")
    livestock_bred = fields.Many2one('g2p.livestock.breed', string='Breed')

    number_of_livestock = fields.Char(string="Number")

    illness_type = fields.Many2many('livestock.illness.type', string='Illness Type')
    illness_images = fields.Many2many('ir.attachment', string="illness images")


    



class LIveStockIllnessType(models.Model):
    _name = "livestock.illness.type"

    name = fields.Char(string="Name")
