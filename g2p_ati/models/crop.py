from odoo import fields, models


class CropCategory(models.Model):
    _name = "crop.category"

    name = fields.Char()


class G2PCrop(models.Model):
    _name = "g2p.crop"
    _description = "Crop Information Model"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    category = fields.Many2one("crop.category")
    name = fields.Char(string="Crop")


class CropVariety(models.Model):
    _name = "crop.variety"

    name = fields.Char()
