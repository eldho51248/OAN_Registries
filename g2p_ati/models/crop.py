from odoo import fields, models

# class G2PCropCategory(models.Model):
#     _name = "g2p.crop.category"

#     name = fields.Char()
#     code = fields.Char()


class G2PCrop(models.Model):
    _name = "g2p.crop"
    _description = "Crop Information Model"

    # category = fields.Many2one("g2p.crop.category")
    name = fields.Char()
    code = fields.Char()
