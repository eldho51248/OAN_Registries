from odoo import fields, models
from ethiopian_date import ethiopian_date

class Region(models.Model):
    _name = 'g2p.region'
    
    code = fields.Char(string="Code")
    

class Zone(models.Model):
    _name = 'g2p.zone'
    
    region = fields.Many2one("g2p.region", string="Region")
    code = fields.Char(string="Code")



class Woreda(models.Model):
    _name = 'g2p.woreda'
    
    zone = fields.Many2one("g2p.zone", string="Zone")
    code = fields.Char(string="Code")


class Kebele(models.Model):
    _name = 'g2p.kebele'
    woreda = fields.Many2one("g2p.woreda", string="Woreda")
    code = fields.Char(string="Code")




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
    zone = fields.Many2one("g2p.zone", string="Zone")
    woreda = fields.Many2one("g2p.woreda", string="Woreda")
    kebele = fields.Many2one("g2p.kebele", string="Kebele")
    
    
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
    birthdate_gc = fields.Date(string="Date Of Birth(GC)")
    
    primary_Language = fields.Many2one("res.lang", string="Primary language")
    is_farmer = fields.Boolean("Are you a Farmer? ")
    farming_type = fields.Selection(string="farming Type", selection=[
        ('agro', 'Agro-Pastorial'),
        ('pastorial', 'Pastorial'),
        ('mixed', 'Mixed farming'),

    ])

    
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
    
    
    # Acces To Finance    
    # type_of_machinery =fields.Many2many('g2p.machinery',string='What kind of Machinery do you use? ')
    # fund_received_type = fields.Selection(selection=[("cash", "Cash"), ("inkind", "In Kind")])
    
    no_finace_access = fields.Boolean("No finance access")
    loans = fields.Boolean("Loans")
    insurance = fields.Boolean("Insurance")
    savings = fields.Boolean("Savings")
    
    other_farmer_in_hh = fields.Boolean('Is there any other farmer in the household who has separate land?')
    
    # Socio economic Data
    
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
    
    
    
    # @api.depends('field')
    
