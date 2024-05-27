from odoo import fields, models


class LivestockType(models.Model):
    _name = "g2p.livestock.type"

    name = fields.Char()


class LivestockBreed(models.Model):
    _name = "g2p.livestock.breed"

    name = fields.Char()
