from datetime import datetime

from dateutil.relativedelta import relativedelta
from ethiopian_date import ethiopian_date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

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
}


class G2PPrimaryCooperative(models.Model):
    _name = "g2p.primary.cooperative"
    _description = "Primary Cooperative"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PCooperativeUnion(models.Model):
    _name = "g2p.cooperative.union"
    _description = "Cooperative Union"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PPrimaryCommodity(models.Model):
    _name = "g2p.primary.commodity"
    _description = "Primary Commodity"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PWaterSource(models.Model):
    _name = "g2p.water.source"
    _description = "Water Source"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PHHIncome(models.Model):
    _name = "g2p.hh.income"
    _description = "House Hold Income"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PFinanceAccess(models.Model):
    _name = "g2p.finance.access"
    _description = "Finance Access"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PMachinery(models.Model):
    _name = "g2p.machinery"
    _description = "Machinery"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )
    _sql_constraints = [("code_unique", "unique(code)", "The code must be unique!")]


class G2PFarmer(models.Model):
    _inherit = "res.partner"

    # Basic Information
    regionn = fields.Many2one("g2p.region", string="Region")
    zone = fields.Many2one("g2p.zone", domain="[('region', '=', region)]")
    woreda = fields.Many2one("g2p.woreda", domain="[('zone', '=', zone)]")
    kebele = fields.Many2one("g2p.kebele", domain="[('woreda', '=', woreda)]")

    given_name = fields.Char(string="First Name(English)", translate=False)
    family_name = fields.Char(string="Father Name(English)", translate=False)
    gf_name_eng = fields.Char(string="Grand Father Name(English)", translate=False)

    first_name_amh = fields.Char(string="First Name(Amharic)", translate=False)
    family_name_amh = fields.Char(string="Father Name(Amharic)", translate=False)
    gf_name_amh = fields.Char(string="Grand Father Name(Amharic)", translate=False)

    first_name_oro = fields.Char(string="First Name(Afaan Oromo)", translate=False)
    family_name_oro = fields.Char(string="Father Name(Afaan Oromo)", translate=False)
    gf_name_oro = fields.Char(string="Grand Father Name(Afaan Oromo)", translate=False)

    farmer_location_longitude = fields.Float(string="Longitude")
    farmer_location_latitude = fields.Float(string="Latitude")

    has_personal_phone = fields.Selection(
        string="Do you have a personal phone number? ", selection=[("yes", "Yes"), ("no", "No")]
    )
    has_national_id = fields.Selection(
        string="Do you have a national id? ", selection=[("yes", "Yes"), ("no", "No")]
    )

    birthdate_ec = fields.Date(string="Date Of Birth(EC)")

    primary_Language = fields.Many2one("g2p.lang")

    is_farmer = fields.Selection(string="Are you a Farmer? ", selection=[("yes", "Yes"), ("no", "No")])

    farming_type = fields.Selection(
        selection=[("agro_pastoral", "Agro-Pastoral"), ("pastoral", "Pastoral"), ("mixed", "Mixed Farming")],
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
            ("rejected", "rejected"),
            ("update_requested", "Update Requested"),
            ("approved", "Approved"),
        ],
        default="draft",
    )

    # AGRICULTURAL RESOURCES
    amount_fertilizer_utilized = fields.Float(string="What is The amount Of fertilizer you have(qt)? ")
    amount_pesticide_utilized = fields.Float(string="What is The amount Of pesticide you have(L)? ")
    amount_insecticide_utilized = fields.Float(string="What is The amount Of insecticide you have in(L)? ")
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

    total_land_area = fields.Float()
    age_int = fields.Integer(compute="_compute_calc_age_int", store=True)

    land_ownership = fields.Selection(
        selection=[("owner", "Owner"), ("tenant", "Tenant"), ("hybrid", "Hybrid")],
        compute="_compute_land_ownership",
        store=True,
        copy=False,
        readonly=True,
    )

    livestock_information_ids = fields.One2many(
        "g2p.livestock.information", "partner_id", string="Live Stock Information"
    )
    data_enumerator_name = fields.Char(string="Data Enumerator")
    data_collection_date = fields.Date()
    odk_reference_id = fields.Char()

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
                name += self.gf_name_eng + " "

            vals.update({"name": name.upper()})
            self.update(vals)

    # @api.depends("land_information_ids.total_land_area")
    def _compute_total_land_area(self):
        for record in self:
            record.total_land_area = sum(land.total_land_area for land in record.land_information_ids)

    @api.depends("land_information_ids.total_land_area")
    def _compute_total_land_area(self):
        for record in self:
            record.total_land_area = sum(land.total_land_area for land in record.land_information_ids)

    @api.depends("land_information_ids.ownership_type")
    def _compute_land_ownership(self):
        for record in self:
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

    @api.onchange("birthdate")
    def _onchange_birthdate(self):
        if self.birthdate:
            converter = ethiopian_date.EthiopianDateConverter()
            ethiopian_date_str = converter.date_to_ethiopian(self.birthdate)
            self.birthdate_ec = ethiopian_date_str

    @api.onchange("birthdate_ec")
    def _onchange_birthdate_ec(self):
        if self.birthdate_ec:
            converter = ethiopian_date.EthiopianDateConverter()
            self.check_birthdate(self.birthdate_ec)

            gregorian_date = converter.to_gregorian(
                self.birthdate_ec.year, self.birthdate_ec.month, self.birthdate_ec.day
            )

            self.birthdate = gregorian_date

    @api.model_create_multi
    def create(self, vals):
        if "phone_number_ids" in vals and not vals.get("phone_number_ids"):
            error_msg = "You must add at least one phone number."
            raise ValidationError(error_msg)

        return super().create(vals)

    @api.onchange("has_finance_access")
    def _onchange_has_finance_access(self):
        if self.has_finance_access == "no":
            return {"finance_accesses": [(6, 0, [])]}

    def check_birthdate(self, birthdate_ec):
        converter = ethiopian_date.EthiopianDateConverter()
        ethiopian_date_today = converter.date_to_ethiopian(fields.date.today())
        actual_month_number = ETHIOPIAN_MONTH_ORDER[birthdate_ec.strftime("%B")]
        actual_selected_ec = datetime(birthdate_ec.year, actual_month_number, birthdate_ec.day).date()

        if actual_selected_ec > ethiopian_date_today:
            error_msg = "You can't select a date of birth greater than today"
            raise ValidationError(error_msg)

    def state_approve(self):
        self.state = "approved"

    def state_reject(self):
        self.state = "rejected"

    def check_user_group(self):
        return self.env.user.has_group("g2p_ati.group_data_enumerator")

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
            # years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            years_months_days = str(delta.years)

        return years_months_days

    def write(self, vals):
        if self.check_user_group():
            error_msg = "You cannot edit record."
            raise UserError(error_msg)
        return super().write(vals)
