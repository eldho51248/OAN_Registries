from odoo import fields, models


class G2PLivestockType(models.Model):
    _name = "g2p.livestock.type"

    name = fields.Char()


class G2PLivestockBreed(models.Model):
    _name = "g2p.livestock.breed"

    name = fields.Char()
