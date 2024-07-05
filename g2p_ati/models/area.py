from odoo import fields, models


class Region(models.Model):
    _name = "g2p.region"

    name = fields.Char()
    code = fields.Char()
    int_code = fields.Char()
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class Zone(models.Model):
    _name = "g2p.zone"

    region = fields.Many2one("g2p.region", string="Region")
    code = fields.Char()
    name = fields.Char()
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class Woreda(models.Model):
    _name = "g2p.woreda"

    zone = fields.Many2one("g2p.zone", string="Zone")
    code = fields.Char()
    name = fields.Char()
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class Kebele(models.Model):
    _name = "g2p.kebele"

    woreda = fields.Many2one("g2p.woreda", string="Woreda")
    code = fields.Char()
    name = fields.Char()
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]
