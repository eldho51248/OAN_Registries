from odoo import fields, models


class G2PLiveStockInformation(models.Model):
    _name = "g2p.livestock.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer")
    is_diseased = fields.Selection(
        string="Does this livestock have been affected by illness? ", selection=[("yes", "Yes"), ("no", "No")]
    )

    # livestock_type = fields.Char(string="Livestock Type")
    livestock_type = fields.Many2one("g2p.livestock.type")

    # livestock_bred = fields.Char(string="Breed")
    # livestock_bred = fields.Many2one("g2p.livestock.breed", string="Breed")

    number_of_livestock = fields.Char(string="Number")
    # water_resources = fields.Many2many('g2p.water.source', string="What Water Sources do you use?")
    illness_type = fields.Many2many("g2p.livestock.illness.type")
    # illness_images = fields.Many2many("ir.attachment")


class G2PLiveStockIllnessType(models.Model):
    _name = "g2p.livestock.illness.type"

    name = fields.Char()
    type = fields.Selection(string="Type", selection=[("crop", "Crop"), ("animal", "Livestock")])
