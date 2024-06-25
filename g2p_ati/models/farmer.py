from odoo import fields, models, api
from ethiopian_date import ethiopian_date
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class G2PPrimaryCooperative(models.Model):
    _name = 'g2p.primary.cooperative'
    _description = 'Primary Cooperative'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    
    code = fields.Char(
        string='Code',
        required=True,
    )

class G2PCooperativeUnion(models.Model):
    _name = 'g2p.cooperative.union'
    _description = 'Cooperative Union'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )

class G2PPrimaryCommodity(models.Model):
    _name = 'g2p.primary.commodity'
    _description = 'Primary Commodity'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )

class G2PWaterSource(models.Model):
    _name = 'g2p.water.source'
    _description = 'Water Source'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
   
class G2PMachinery(models.Model):
    _name = 'g2p.machinery'
    _description = 'Machinery'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )

#TODO add type to phone number and logic


class G2PFarmer(models.Model):
    _inherit = "res.partner"
    
    # Basic Information
    regionn = fields.Many2one("g2p.region", string="Region")
    zone = fields.Many2one("g2p.zone", string="Zone", domain="[('region', '=', region)]")
    woreda = fields.Many2one("g2p.woreda", string="Woreda", domain="[('zone', '=', zone)]")
    kebele = fields.Many2one("g2p.kebele", string="Kebele", domain="[('woreda', '=', woreda)]")
    
    
    given_name = fields.Char(string="First Name", translate=False)
    family_name = fields.Char(string="Father Name", translate=False)
    gf_name_eng = fields.Char(string="Grand Father Name", translate=False)
    
    first_name_amh = fields.Char(string="ስም", translate=False)
    family_name_amh = fields.Char(string="የአባት ስም", translate=False)
    gf_name_amh = fields.Char(string="የአያት ስም", translate=False)
    
    first_name_oro = fields.Char(string="First Name(Oro)", translate=False)
    family_name_oro = fields.Char(string="Father Name(Oro)", translate=False)
    gf_name_amh_oro = fields.Char(string="Grand Father Name(Oro)", translate=False)
    
    
    # birthdate = fields.Date(string="Date Of Birth(GC)")
    birthdate_ec = fields.Date(string="Date Of Birth(EC)")
    # birthplace = fields.Many2one('res.country', string='Birth Country', default=lambda self: self.env.ref('base.et_001').id)
    birthplace = fields.Many2one('res.country', string='Birth Country')
    
    primary_Language = fields.Many2one("res.lang", string="Primary language")
    

    is_farmer = fields.Selection(
        string='Are you a Farmer? ',
        selection=[('yes', 'Yes'), ('no', 'No')] )
    
    farming_type = fields.Selection(string="farming Type", selection=[  
                                                                      ('agro_pastoral', 'Agro-Pastoral'),
                                                                      ('pastoral', 'Pastoral'),
                                                                      ('mixed', 'Mixed Farming')])

    
    # MEMEBERSHIP
    is_member_of_primary_cooperative =    fields.Selection(
        string="Is Member Of Primary Cooperative? ",
        selection=[('yes', 'Yes'), ('no', 'No')] )  
    primary_cooperatives = fields.Many2one('g2p.primary.cooperative', string="Primary Cooperatives" )
    
    is_member_of_cooperative_union = fields.Selection(
        string="Is Member Of Cooperative Union? ",
        selection=[('yes', 'Yes'), ('no', 'No')] )
    cooperative_unions = fields.Many2one('g2p.cooperative.union', string="Cooperative Unions" )
    
    is_member_in_farmer_cluster = fields.Selection(
        string="Is Member In Farmer Cluster? ",
        selection=[('yes', 'Yes'), ('no', 'No')] )
    
    primary_commodity = fields.Many2one('g2p.primary.commodity', string="Primary Commodity")
    role_in_farmer_cluster = fields.Selection(string="Role In Farmer Cluster", selection=[
        ('lead', 'Lead'),
        ('deputy','Deputy'),
        ('secretary', 'Secretary'),
        ('accountant', 'Accounatnt'),
        ('member', 'Member')
    ])
    
    
    # AGRICULTURAL RESOURCES
    amount_fertilizer_utilized = fields.Float(string="What is The amount Of fertilizer you have(qt)? ")
    amount_pesticide_utilized = fields.Float(string="What is The amount Of pesticide you have(L)? ")
    amount_insecticide_utilized = fields.Float(string="What is The amount Of insecticide you have in(L)? ")
    amount_improved_seed_utilized = fields.Float(string="What is The amount Of improved seed you have used(qt)? ")
    
    
    # ACCESS TO RESOURCES  
    
    access_to_machinery = fields.Selection( string="Do you use machinery? ", selection=[('yes', 'Yes'), ('no', 'No')])  
    type_of_machinery =fields.Many2many('g2p.machinery', string='What kind of machinery do you use? ')
    irregation_types = fields.Selection(
        string='Martial Status',
        selection=[
            ('pump', 'Pump'), 
            ('canal', 'canal')
            ])
    

    no_finace_access = fields.Selection(
        string="No Finance Access ",
        selection=[('yes', 'Yes'), ('no', 'No')] )
    
    loans = fields.Selection(
        string="Loans ",
        selection=[('yes', 'Yes'), ('no', 'No')] )

    insurance =  fields.Selection(
        string="Insurance ",
        selection=[('yes', 'Yes'), ('no', 'No')] )
    
    savings = fields.Selection(
        string="Savings ",
        selection=[('yes', 'Yes'), ('no', 'No')] )
    


    other_farmer_in_hh = fields.Selection(
        string="Is there any other farmer in the household who has separate land? ",
        selection=[('yes', 'Yes'), ('no', 'No')] )  
    
    
    # SOCIO-ECONOMIC DATA
    martial_status = fields.Selection(
        string='Martial Status',
        selection=[
            ('single', 'Single'), 
            ('married', 'Married'), 
            ('divorced', 'Divorced'), 
            ('widowed', 'Widowed')])
    
    education = fields.Selection(
        [ ("illeterate", "Illeterate"),
            ("readwrite", "Can Read and Write"),
            ("basic", "Basic(1-8)"),
            ("intermediary", "Intermediary(9-12)"),
            ("technic", "Vocational and Technical School"),
            ("higher", "Higher education(Unversity, College)")], string="Educational Level",)
    hh_income = fields.Float(string='Total Amount')
    hh_size = fields.Integer(string="Household Size")
    hh_income_type = fields.Selection(string='House Hold Income Type',
        selection=[
            ('crop', 'Crop'), 
            ('livestock', 'Livestock'), 
            ('gov_ngo', 'Government/NGO Support'), 
            ('other', 'Other')])


    # Land INFORMATIONS
    land_information_ids = fields.One2many("g2p.land.information", "partner_id", string="Land Information")
    crop_information_ids = fields.One2many("g2p.crop.information", "partner_id", string="Crop Information")
    land_ownership = fields.Selection(
        selection=[('owner', 'Owner'), ('tenant', 'Tenant'), ('hybrid', 'Hybrid')],
        compute='_compute_land_ownership',
        store=True,
        copy=False,
        readonly=True,
        string='Land Ownership'
    )
    total_land_area = fields.Integer("Total Land Area")

    livestock_information_ids = fields.One2many("g2p.livestock.information", "partner_id", string="Live Stock Information")
    data_enumerator_name = fields.Char(string="Data Enumerator")
    data_collection_date= fields.Date(string="Data Collection Date")
    

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




    @api.depends('land_information_ids.total_land_area')
    def _compute_total_land_area(self):
        for record in self:
            total_area = sum(r.total_land_area for r in record.land_information_ids)
            record.total_land_area = total_area
        
        
    @api.depends('land_information_ids.ownership_type')
    def _compute_land_ownership(self):
        for record in self:
            land_info_records = record.land_information_ids
            owner_count = len(land_info_records.filtered(lambda r: r.ownership_type == 'owner'))
            tenant_count = len(land_info_records.filtered(lambda r: r.ownership_type == 'tenant'))
            if owner_count > 0 and tenant_count == 0:
                record.land_ownership = 'owner'
            elif tenant_count > 0 and owner_count == 0:
                record.land_ownership = 'tenant'
            elif owner_count > 0 and tenant_count > 0:
                record.land_ownership = 'hybrid'
            else:
                record.land_ownership = False


    @api.onchange('birthdate')
    def _onchange_birthdate(self):
        if self.birthdate:
            converter = ethiopian_date.EthiopianDateConverter()
            ethiopian_date_str = converter.date_to_ethiopian(self.birthdate)
            self.birthdate_ec = ethiopian_date_str


    @api.onchange('birthdate_ec')
    def _onchange_birthdate_ec(self):
        if self.birthdate_ec:
            converter = ethiopian_date.EthiopianDateConverter()
            gregorian_date = converter.to_gregorian(self.birthdate_ec.year,self.birthdate_ec.month,self.birthdate_ec.day)
            self.birthdate = gregorian_date


    @api.model
    def create(self, vals):
        if 'phone_number_ids' in vals and not vals.get('phone_number_ids'):
            raise ValidationError("You must add at least one phone number.")
        
        
    @api.depends('no_finace_access')
    def _compute_finance_values(self):
        for record in self:
            if record.no_finace_access!= 'yes':
                record.loans = 'no'
                record.insurance = 'no'
                record.savings = 'no'
        
    
    
