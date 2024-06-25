from odoo import fields, models


class G2pLang(models.Model):
    _name = "g2p.lang"

    name = fields.Char(string="Language")
    code = fields.Char(string="Code")
