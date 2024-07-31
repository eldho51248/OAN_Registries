from odoo import fields, models


class G2PCropCategory(models.Model):
    _name = "g2p.crop.category"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PCrop(models.Model):
    _name = "g2p.crop"
    _description = "Crop Information Model"

    category = fields.Many2one("g2p.crop.category", required=True)
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]
