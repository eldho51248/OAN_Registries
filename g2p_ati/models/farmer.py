from odoo import api,models,fields


class G2PFarmer(models.Model):
    _inherit = "res.partner"

    grand_father_name = fields.Char(translate=False)
    hh_size = fields.Integer(string='Household Size')
    hh_income = fields.Float(string="House Hold Income") # might also change to Monetary if needed
    ed_level = fields.Selection([
        ('pr', 'Primary School'),
        ('ss', 'Secondary School'),
        ('tvs', 'Technical and Vocation Sciences'),
        ('col', 'College'),
        ('unv', 'University')
    ],string = "Educational Level")

    farming_type = fields.Many2one('g2p.farming.type', string='Farming Type')

    # Farmer Details
    # Membership
    
    is_member_of_primary_cooperative = fields.Boolean(string="Is Member Of Primary Cooperative? ")
    is_member_of_union = fields.Boolean(string="Is Member In Union? ")
    is_member_in_farmer_cluster = fields.Boolean(string="Is Member In Farmer Cluster? ")

    # Agricultural Input
    amount_fertilizer_utilized = fields.Float(string="Amount Of fertilizer Utilized in kg")
    amount_pesticide_utilized = fields.Float(string="Amount Of Pesticide Utilized in kg")
    amount_insecticide_utilized = fields.Float(string="Amount Of Insecticide Utilized in kg")
    amount_improved_seed_utilized = fields.Float(string="Amount Of Improved Seed Utilized in kg")

    # Financial Services
    fund_received_type = fields.Selection(
        string='Fund Received Type',
        selection=[('cash', 'Cash'), ('inkind', 'In Kind')]
    )
    
    loans  = fields.Boolean(string="Loans")
    insurance  = fields.Boolean(string="Insurance")
    savings  = fields.Boolean(string="Savings")


    # Access To resources
    access_to_water = fields.Boolean(string="Access To Water")
    access_to_machinery = fields.Boolean(string="Access To Machinery")


    












    




