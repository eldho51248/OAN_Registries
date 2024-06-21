from odoo import fields, models, api
from ethiopian_date import ethiopian_date

class G2PPrimaryCooperative(models.Model):
    _name = 'g2p.primary.cooperative'
    _description = 'Primary Cooperative'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
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

class G2PPrimaryCommodity(models.Model):
    _name = 'g2p.primary.commodity'
    _description = 'Primary Commodity'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
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

#TODO add type to phone number and logic




class G2PFarmer(models.Model):
    _inherit = "res.partner"
    
    
    # Basic Information
    
    region = fields.Many2one("g2p.region", string="Region")
    zone = fields.Many2one("g2p.zone", string="Zone", domain="[('region', '=', region)]")
    woreda = fields.Many2one("g2p.woreda", string="Woreda", domain="[('zone', '=', zone)]")
    kebele = fields.Many2one("g2p.kebele", string="Kebele", domain="[('woreda', '=', woreda)]")
    
    
    given_name = fields.Char(string="First Name(Eng)", translate=False)
    family_name = fields.Char(string="Father Name(Eng)", translate=False)
    gf_name_eng = fields.Char(string="Grand Father Name(Eng)", translate=False)
    
    first_name_amh = fields.Char(string="First Name(Amh)", translate=False)
    family_name_amh = fields.Char(string="Father Name(Amh)", translate=False)
    gf_name_amh = fields.Char(string="Grand Father Name(Amh)", translate=False)
    
    first_name_oro = fields.Char(string="First Name(Oro)", translate=False)
    family_name_oro = fields.Char(string="Father Name(Oro)", translate=False)
    gf_name_amh_oro = fields.Char(string="Grand Father Name(Oro)", translate=False)
    
    birthdate = fields.Date(string="Date Of Birth(GC)")
    birthdate_ec = fields.Date(string="Date Of Birth(EC)")
    
    primary_Language = fields.Many2one("res.lang", string="Primary language")
    is_farmer = fields.Boolean("Are you a Farmer? ")
    farming_type = fields.Selection(string="farming Type", selection=[
        ('agro', 'Agro-Pastorial'),
        ('pastorial', 'Pastorial'),
        ('mixed', 'Mixed farming')])

    
    # Memebership
    
    is_member_of_primary_cooperative = fields.Boolean(string="Is Member Of Primary Cooperative? ")
    primary_cooperatives = fields.Many2many('g2p.primary.cooperative', string="Primary Cooperatives" )

    is_member_of_cooperative_union = fields.Boolean(string="Is Member Of Cooperative Union? ")
    cooperative_unions = fields.Many2many('g2p.cooperative.union', string="Cooperative Unions" )
    
    is_member_in_farmer_cluster = fields.Boolean(string="Is Member In Farmer Cluster? ")
    primary_commodity = fields.Many2one('g2p.primary.commodity', string="Primary Commodity")
    role_in_farmer_cluster = fields.Selection(string="Role In Farmer Cluster", selection=[
        ('lead', 'Lead'),
        ('deputy','Deputy'),
        ('secretary', 'Secretary'),
        ('accountant', 'Accounatnt'),
        ('member', 'Member')
    ])
    
    
    # Agricultural Input
    amount_fertilizer_utilized = fields.Float(string="What is The amount Of fertilizer you have(qt)? ")
    amount_pesticide_utilized = fields.Float(string="What is The amount Of pesticide you have(L)? ")
    amount_insecticide_utilized = fields.Float(string="What is The amount Of insecticide you have in(L)? ")
    amount_improved_seed_utilized = fields.Float(string="What is The amount Of improved seed you have used(qt)? ")
    
    
    # Access To resources
    water_resources = fields.Many2many('g2p.water.source', string="What Water Sources do you use?")
    access_to_machinery = fields.Boolean(string="Do you use machinery? ")
    type_of_machinery =fields.Many2many('g2p.machinery', string='What kind of machinery do you use? ')
    
    no_finace_access = fields.Boolean("No finance access")
    loans = fields.Boolean("Loans")
    insurance = fields.Boolean("Insurance")
    savings = fields.Boolean("Savings")
    
    other_farmer_in_hh = fields.Boolean('Is there any other farmer in the household who has separate land?')
    
    # Socio economic Dat
    martial_status = fields.Selection(
        string='Martial Status',
        selection=[
            ('single', 'Single'), 
            ('married', 'Married'), 
            ('divorced', 'Divorced'), 
            ('widowed', 'Widowed')]
    )
    
    education = fields.Selection(
        [ ("illeterate", "Illeterate"),
            ("readwrite", "Can Read and Write"),
            ("basic", "Basic(1-8)"),
            ("intermediary", "Intermediary(9-12)"),
            ("technic", "Vocational and Technical School"),
            ("higher", "Higher education(Unversity, College)"),
        ],
        string="Educational Level",
    )
    hh_income = fields.Float(string='Total Amount')
    hh_size = fields.Integer(string="Household Size")

    # Land Informations
    land_information_ids = fields.One2many("g2p.land.information", "partner_id", string="Land Information")
    crop_information_ids = fields.One2many("g2p.crop.information", "partner_id", string="Crop Information")
    livestock_information_ids = fields.One2many(
        "g2p.livestock.information", "partner_id", string="Live Stock Information"
    )
    
    data_enumerator_name = fields.Char(string="Data Enumerator")
    data_collection_date= fields.Date(string="Data Collection Date")
    

    land_ownership = fields.Selection(
        selection=[('owner', 'Owner'), ('tenant', 'Tenant'), ('hybrid', 'Hybrid')],
        compute='_compute_land_ownership',
        store=True,
        copy=False,
        readonly=True,
        string='Land Ownership'
    )

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

    

    def write(self, values):
        
        
        
    
        result = super(G2PFarmer, self).write(values)
        return result
    
    
