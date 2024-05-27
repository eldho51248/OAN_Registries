from odoo import fields, models


class FarmingType(models.Model):
    _name = "g2p.farming.type"

    name = fields.Char()
