from odoo import fields, models


class G2PCropInformation(models.Model):
    _name = "g2p.crop.information"

    partner_id = fields.Many2one("res.partner", string="partner")
    crop = fields.Many2one("g2p.crop")
    variety = fields.Many2one("g2p.crop.variety", string="Crop Variety")
    illness_type = fields.Many2many("g2p.crop.illness.type")
    illness_images = fields.Many2many("ir.attachment")


class G2PCropIllnessType(models.Model):
    _name = "g2p.crop.illness.type"

    name = fields.Char()
