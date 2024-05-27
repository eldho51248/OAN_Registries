from odoo import fields, models


class G2PLiveStockInformation(models.Model):
    _name = "g2p.livestock.information"

    partner_id = fields.Many2one("res.partner", string="partner")

    # livestock_type = fields.Char(string="Livestock Type")
    livestock_type = fields.Many2one("g2p.livestock.type")

    # livestock_bred = fields.Char(string="Breed")
    livestock_bred = fields.Many2one("g2p.livestock.breed", string="Breed")

    number_of_livestock = fields.Char(string="Number")
    illness_type = fields.Many2many("g2p.livestock.illness.type")
    illness_images = fields.Many2many("ir.attachment")


class G2PLiveStockIllnessType(models.Model):
    _name = "g2p.livestock.illness.type"

    name = fields.Char()
