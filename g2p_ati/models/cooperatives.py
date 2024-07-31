from odoo import fields, models


class G2PPrimaryCooperative(models.Model):
    _name = "g2p.primary.cooperative"
    _description = "Primary Cooperative"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PCooperativeUnion(models.Model):
    _name = "g2p.cooperative.union"
    _description = "Cooperative Union"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]
