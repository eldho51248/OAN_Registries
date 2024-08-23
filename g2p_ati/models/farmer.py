import logging
import re
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .utils import eth_date

_logger = logging.getLogger(__name__)

ETHIOPIAN_MONTH_ORDER = {
    "September": 1,
    "October": 2,
    "November": 3,
    "December": 4,
    "January": 5,
    "February": 6,
    "March": 7,
    "April": 8,
    "May": 9,
    "June": 10,
    "July": 11,
    "August": 12,
    "Pagume": 13,
}


class G2PFarmer(models.Model):
    _inherit = "res.partner"
    _order = "registration_date desc"

    zone = fields.Many2one("g2p.zone", domain="[('region', '=', region)]")
    woreda = fields.Many2one("g2p.woreda", domain="[('zone', '=', zone)]")
    kebele = fields.Many2one("g2p.kebele", domain="[('woreda', '=', woreda)]")
    given_name = fields.Char(string="First Name(English)", translate=False)
    family_name = fields.Char(string="Father's Name(English)", translate=False)
    gf_name_eng = fields.Char(string="Grand Father's Name(English)", translate=False)
    first_name_amh = fields.Char(string="First Name(Amharic)", translate=False)
    family_name_amh = fields.Char(string="Father's Name(Amharic)", translate=False)
    gf_name_amh = fields.Char(string="Grand Father's Name(Amharic)", translate=False)
    first_name_other = fields.Char(string="First Name", translate=False)
    family_name_other = fields.Char(string="Father's Name", translate=False)
    gf_name_other = fields.Char(string="Grand Father's Name", translate=False)

    has_personal_phone = fields.Selection(
        string="Do you have a personal phone number? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    has_national_id = fields.Selection(
        string="Do you have a national id? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    birthdate_ec = fields.Char(string="Date Of Birth (EC)", help="YYYY-MM-DD")
    primary_Language = fields.Many2one("g2p.lang")
    is_farmer = fields.Selection(
        string="Are you a Farmer? ", index=True, selection=[("yes", "Yes"), ("no", "No")]
    )
    farming_type = fields.Selection(
        selection=[
            ("crop_farming", "Crop Farming"),
            ("livestock_farming", "Livestock Farming"),
            ("mixed_farming", "Mixed Farming"),
        ]
    )
    is_disabled = fields.Selection(string="Are you disabled? ", selection=[("yes", "Yes"), ("no", "No")])

    # MEMEBERSHIP
    is_member_of_primary_cooperative = fields.Selection(
        string="Is Member Of Primary Cooperative? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    primary_cooperatives = fields.Many2one("g2p.primary.cooperative")
    is_member_of_cooperative_union = fields.Selection(
        string="Is Member Of Cooperative Union? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    cooperative_unions = fields.Many2one("g2p.cooperative.union")
    is_member_in_farmer_cluster = fields.Selection(
        string="Is Member In Farmer Cluster? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    primary_commodity = fields.Many2one("g2p.primary.commodity")
    role_in_farmer_cluster = fields.Selection(
        selection=[
            ("lead", "Lead"),
            ("deputy", "Deputy"),
            ("secretary", "Secretary"),
            ("accountant", "Accountant"),
            ("member", "Member"),
        ],
    )
    state = fields.Selection(
        tracking=True,
        selection=[
            ("draft", "Draft"),
            ("rejected", "Rejected"),
            ("update_requested", "Update Requested"),
            ("approved", "Approved"),
        ],
        index=True,
        default="draft",
    )

    # AGRICULTURAL RESOURCES
    do_you_use_fertilizer = fields.Selection(
        string="Do you use fertilizer? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    amount_fertilizer_utilized = fields.Float(string="What is The amount Of fertilizer you have(qt)? ")
    do_you_use_pesticide = fields.Selection(
        string="Do you use pesticide? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    amount_pesticide_utilized = fields.Float(string="What is The amount Of pesticide you have(L)? ")
    do_you_use_insecticide = fields.Selection(
        string="Do you use insecticide? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    amount_insecticide_utilized = fields.Float(string="What is The amount Of insecticide you have in(L)? ")
    do_you_use_improved_seed = fields.Selection(
        string="Do you use improved_seed? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    amount_improved_seed_utilized = fields.Float(
        string="What is The amount Of improved seed you have used(qt)? "
    )

    # ACCESS TO RESOURCES
    crop_water_sources = fields.Many2many(
        "g2p.water.source",
        "crop_water",
        "crop_water_source_rel",
        string="What water sources do you use for your crops? ",
    )
    livestock_water_sources = fields.Many2many(
        "g2p.water.source",
        "livestock_water",
        "livestock_water_source_rel",
        string="What water sources do you use for your livestock? ",
    )
    access_to_machinery = fields.Selection(
        string="Do you use machinery? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    type_of_machinery = fields.Many2many("g2p.machinery", string="What kind of machinery do you use? ")
    irrigation_types = fields.Selection(
        string="What Type of Irrigation do you use?", selection=[("pump", "Pump"), ("canal", "canal")]
    )
    has_finance_access = fields.Selection(
        string="Do you have Financial Access ", selection=[("yes", "Yes"), ("no", "No")], default="no"
    )
    finance_accesses = fields.Many2many(comodel_name="g2p.finance.access")
    other_farmer_in_hh = fields.Selection(
        string="Is there any other farmer in the household who has separate land? ",
        selection=[("yes", "Yes"), ("no", "No")],
    )
    # SOCIO-ECONOMIC DATA
    martial_status = fields.Selection(
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("widowed", "Widowed"),
        ],
    )
    education = fields.Selection(
        [
            ("illiterate", "Illiterate"),
            ("read_write", "Can Read and Write"),
            ("basic", "Basic(1-8)"),
            ("intermediary", "Intermediary(9-12)"),
            ("higher_education", "Higher Education(University and College)"),
        ],
        string="Educational Level",
    )
    hh_is_household_head = fields.Selection(
        string="Are You a household head? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    hh_income_type = fields.Many2many(comodel_name="g2p.hh.income", string="House Hold Income")

    # Land INFORMATIONS
    land_information_ids = fields.One2many("g2p.land.information", "partner_id", string="Land Information")
    crop_information_ids = fields.One2many("g2p.crop.information", "partner_id", string="Crop Information")
    total_land_area = fields.Float(default=0.0, readonly=True, compute="_compute_total_land_area", store=True)
    age_int = fields.Integer(compute="_compute_calc_age_int", store=True)
    land_ownership = fields.Selection(
        selection=[("owner", "Owner"), ("tenant", "Tenant"), ("hybrid", "Hybrid")],
        compute="_compute_land_ownership",
        store=True,
        readonly=True,
    )
    livestock_information_ids = fields.One2many(
        "g2p.livestock.information", "partner_id", string="Live Stock Information"
    )
    rejection_reason = fields.Text()

    farmer_id = fields.Char(string="Farmer ID", compute="_compute_farmer_id", store=True, index=True)

    @api.onchange("is_group", "family_name", "given_name", "gf_name_eng")
    def name_change_farmer(self):
        vals = {}
        if not self.is_group:
            name = ""
            if self.given_name:
                name += self.given_name + " "
            if self.family_name:
                name += self.family_name + " "
            if self.gf_name_eng:
                name += self.gf_name_eng
            vals.update({"name": name.upper()})
            self.update(vals)

    @api.depends("land_information_ids.total_land_area")
    def _compute_total_land_area(self):
        for record in self:
            record.total_land_area = sum(land.total_land_area for land in record.land_information_ids)

    @api.depends("land_information_ids.ownership_type")
    def _compute_land_ownership(self):
        for record in self:
            if record.land_information_ids:
                land_info_records = record.land_information_ids
                owner_count = len(land_info_records.filtered(lambda r: r.ownership_type == "owner"))
                tenant_count = len(land_info_records.filtered(lambda r: r.ownership_type == "tenant"))
                if owner_count > 0 and tenant_count == 0:
                    record.land_ownership = "owner"
                elif tenant_count > 0 and owner_count == 0:
                    record.land_ownership = "tenant"
                elif owner_count > 0 and tenant_count > 0:
                    record.land_ownership = "hybrid"
                else:
                    record.land_ownership = False
            else:
                record.land_ownership = False

    @api.onchange("birthdate")
    def _onchange_birthdate(self):
        if self.birthdate:
            bday = date(self.birthdate.year, self.birthdate.month, self.birthdate.day)
            ethiopian_date_str = eth_date.to_ethiopian(bday.year, bday.month, bday.day)
            self.birthdate_ec = eth_date.convert_tuple_to_string_with_separator(ethiopian_date_str)

    @api.constrains("birthdate")
    def _add_birthdate_ec(self):
        if self.birthdate:
            bday = date(self.birthdate.year, self.birthdate.month, self.birthdate.day)
            ethiopian_date_str = eth_date.to_ethiopian(bday.year, bday.month, bday.day)
            self.birthdate_ec = eth_date.convert_tuple_to_string_with_separator(ethiopian_date_str)

    @api.onchange("birthdate_ec")
    def _onchange_birthdate_ec(self):
        if self.birthdate_ec:
            eth_date.check_ethipian_date_str(self.birthdate_ec)
            date_list = re.split("[-/,]", self.birthdate_ec)
            gc_date = eth_date.to_gregorian(int(date_list[2]), int(date_list[1]), int(date_list[0]))
            if gc_date > fields.date.today():
                raise ValidationError(_("You can't select a date of birth greater than today"))
            self.birthdate = gc_date

    @api.onchange("has_finance_access")
    def _onchange_has_finance_access(self):
        if self.has_finance_access == "no":
            return {"finance_accesses": [(6, 0, [])]}

    def state_approve(self):
        self.state = "approved"

    def state_reject(self):
        return {
            "name": _("Enter Rejection Reason"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.rejection.reason.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.depends("birthdate")
    def _compute_calc_age_int(self):
        for line in self:
            line.age_int = self.compute_age_int_from_dates(line.birthdate)

    def compute_age_int_from_dates(self, partner_dob):
        now = datetime.strptime(str(fields.Datetime.now())[:10], "%Y-%m-%d")
        years_months_days = None
        if partner_dob:
            dob = partner_dob
            delta = relativedelta(now, dob)
            years_months_days = str(delta.years)
        return years_months_days

    @api.depends("ref_id", "is_farmer")
    def _compute_farmer_id(self):
        for record in self:
            if record.is_farmer == "yes" and record.ref_id:
                record.farmer_id = f"FR-{record.ref_id}"
            else:
                record.farmer_id = False
