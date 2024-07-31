from odoo import fields, models


class G2PWaterSource(models.Model):
    _name = "g2p.water.source"
    _description = "Water Source"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PHHIncome(models.Model):
    _name = "g2p.hh.income"
    _description = "House Hold Income"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PFinanceAccess(models.Model):
    _name = "g2p.finance.access"
    _description = "Finance Access"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PMachinery(models.Model):
    _name = "g2p.machinery"
    _description = "Machinery"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]
