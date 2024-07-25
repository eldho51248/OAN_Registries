from odoo import fields, models


class G2PCropInformation(models.Model):
    _name = "g2p.crop.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer")
    crop = fields.Many2one("g2p.crop")
    is_diseased = fields.Selection(
        string="Has this crop been affected by illness?", selection=[("yes", "Yes"), ("no", "No")]
    )
    illness_type = fields.Many2many("g2p.illness.type", string="Disease")

    # illness_images = fields.Many2many("ir.attachment")
