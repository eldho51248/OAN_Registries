from odoo import fields, models


class G2PLandInformation(models.Model):
    _name = "g2p.land.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer")
    total_land_area = fields.Float(string="Size In Hectare")
    land_certificate = fields.Many2one("storage.file", string="Land Certificate")
    land_id =fields.Char(string='Land ID',)
    ownership_type = fields.Selection(
        string="Ownership Type", selection=[("owner", "Owner"), ("tenant", "Tenant")], required=True
    )
