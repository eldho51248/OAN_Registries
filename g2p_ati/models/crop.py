from odoo import fields, models


class G2PCropCategory(models.Model):
    _name = "g2p.crop.category"

    name = fields.Char()


class G2PCrop(models.Model):
    _name = "g2p.crop"
    _description = "Crop Information Model"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    category = fields.Many2one("g2p.crop.category")
    name = fields.Char(string="Crop")


class G2PCropVariety(models.Model):
    _name = "g2p.crop.variety"

    name = fields.Char()
