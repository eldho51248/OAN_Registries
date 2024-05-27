from odoo import fields, models


class G2PFarmingType(models.Model):
    _name = "g2p.farming.type"

    name = fields.Char()
