import re
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from . import eth_date


class G2PLiveStockInformation(models.Model):
    _name = "g2p.livestock.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer", required=True)
    is_diseased = fields.Selection(
        string="Has this livestock been affected by illness?", selection=[("yes", "Yes"), ("no", "No")]
    )
    livestock_type = fields.Many2one(
        "g2p.livestock.type",
        required=True,
    )
    number_of_livestock = fields.Integer(string="Number", required=True)
    illness_type = fields.Many2many("g2p.illness.type", string="Disease")
    collected_gc = fields.Date(string="Collected GC")
    collected_ec = fields.Char(string="Collected EC")
    season = fields.Many2one("g2p.season")

    @api.constrains("number_of_livestock")
    def _check_number_of_livestock_positive(self):
        for record in self:
            if record.number_of_livestock <= 0:
                raise ValidationError(_("Number of livestock must be greater than 0."))

    @api.constrains("collected_gc", "collected_ec")
    def _check_collected_dates(self):
        for record in self:
            if not record.collected_gc and not record.collected_ec:
                raise ValidationError(_("Either Collected GC or Collected EC must be filled."))

    @api.constrains("is_diseased", "illness_type")
    def _check_illness_type_required(self):
        """Ensure illness_type is required if is_diseased is 'yes'."""
        for record in self:
            if record.is_diseased == "yes" and not record.illness_type:
                error_message = _("Illness type is required when the crop is diseased.")
                raise ValidationError(error_message)

    @api.onchange("collected_gc")
    def _onchange_collected_gc(self):
        if self.collected_gc:
            cdate = date(self.collected_gc.year, self.collected_gc.month, self.collected_gc.day)
            ethiopian_date_str = eth_date.to_ethiopian(cdate.year, cdate.month, cdate.day)
            self.collected_ec = eth_date.convert_tuple_to_string_with_separator(ethiopian_date_str)
            season = self.env["g2p.season"].search(
                [("start_gc", "<=", self.collected_gc), ("end_gc", ">=", self.collected_gc)], limit=1
            )
            if season:
                self.season = season.id
            else:
                self.season = False

    @api.onchange("collected_ec")
    def _onchange_collected_ec(self):
        if self.collected_ec:
            date_list = re.split("[-/,]", self.collected_ec)
            gc_date = eth_date.to_gregorian(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            self.collected_gc = gc_date


class G2PIllnessType(models.Model):
    _name = "g2p.illness.type"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    illness_type = fields.Selection(
        string="Type", selection=[("crop", "Crop"), ("animal", "Livestock")], required=True
    )

    @api.constrains("illness_type")
    def _check_name(self):
        for record in self:
            if not record.illness_type:
                error_message = _("illness_type should not empty.")
                raise ValidationError(error_message)

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name:
                error_message = _("name should not empty.")
                raise ValidationError(error_message)

    @api.constrains("code")
    def _check_code(self):
        records = self.search([])
        for record in self:
            if not record.code:
                error_message = _("Code should not empty.")
                raise ValidationError(error_message)

        for rec in records:
            if self.code.lower() == rec.code.lower() and self.id != rec.id:
                raise ValidationError(_("The code must be unique!"))
