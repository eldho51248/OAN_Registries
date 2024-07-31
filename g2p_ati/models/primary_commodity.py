from odoo import fields, models


class G2PPrimaryCommodity(models.Model):
    _name = "g2p.primary.commodity"
    _description = "Primary Commodity"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]
