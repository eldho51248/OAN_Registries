import re
from datetime import date
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from .utils import eth_date

class G2PSeason(models.Model):
    _name = "g2p.season"
    _description = "Season"

    name = fields.Char(required=True)
    start_gc = fields.Date()
    start_ec = fields.Char()
    end_gc = fields.Date()
    end_ec = fields.Char()
    year_gc = fields.Integer()
    year_ec = fields.Integer()

    @api.onchange("start_gc")
    def _compute_start_ec_from_start_gc(self):
        for record in self:
            if record.start_gc:
                cdate = date(self.start_gc.year, self.start_gc.month, self.start_gc.day)
                ethiopian_date_str = eth_date.to_ethiopian(cdate.year, cdate.month, cdate.day)
                if self.end_gc and self.start_gc:
                    if self.end_gc < self.start_gc:
                        error_msg = "Season end must be greater than or equal to season start"
                        raise ValidationError(error_msg)
                self.start_ec = eth_date.convert_tuple_to_string_with_separator(ethiopian_date_str)
                self.year_gc = self.start_gc.year
            else:
                record.start_ec = False

    @api.onchange("start_ec")
    def _compute_start_gc_from_start_ec(self):
        for record in self:
            if record.start_ec:
                date_list = re.split("[-/,]", self.start_ec)
                gc_date = eth_date.to_gregorian(int(date_list[0]), int(date_list[1]), int(date_list[2]))
                self.start_gc = gc_date
                self.year_ec = int(date_list[0])
            else:
                record.start_gc = False

    @api.onchange("end_gc")
    def _compute_end_ec_from_end_gc(self):
        for record in self:
            if record.end_gc and self.start_gc:
                if record.end_gc < self.start_gc:
                    error_msg = "Season end must be greater than or equal to season start"
                    raise ValidationError(error_msg)

                cdate = date(self.end_gc.year, self.end_gc.month, self.end_gc.day)
                ethiopian_date_str = eth_date.to_ethiopian(cdate.year, cdate.month, cdate.day)
                self.end_ec = eth_date.convert_tuple_to_string_with_separator(ethiopian_date_str)

    @api.onchange("end_ec")
    def _compute_end_gc_from_end_ec(self):
        for record in self:
            if record.end_ec:
                date_list = re.split("[-/,]", self.end_ec)
                gc_date = eth_date.to_gregorian(int(date_list[0]), int(date_list[1]), int(date_list[2]))

                if gc_date and self.start_gc:
                    if gc_date < self.start_gc:
                        error_msg = "Season end must be greater than or equal to season start"
                        raise ValidationError(error_msg)

                self.end_gc = gc_date

    @api.constrains("start_gc", "start_ec")
    def _check_start_dates(self):
        for record in self:
            if not record.start_gc and not record.start_ec:
                raise ValidationError(_("Either Start date GC or Start date GC should not be empty."))

    @api.constrains("end_ec", "end_gc")
    def _check_end_dates(self):
        for record in self:
            if not record.end_gc and not record.end_ec:
                raise ValidationError(_("Either End date EC or End date GC should not be empty."))

    @api.constrains("start_gc", "end_gc")
    def _check_no_overlap_within_same_year_gc(self):
        for record in self:
            overlapping_seasons = self.search(
                [
                    ("year_gc", "=", record.year_gc),
                    ("id", "!=", record.id),
                    "&",
                    ("start_gc", "<=", record.end_gc),
                    ("end_gc", ">=", record.start_gc),
                ],
                limit=1,
            )
            if overlapping_seasons:
                raise ValidationError(_("There cannot be overlapping seasons within the same year."))
