from odoo import fields, models, api

class Region(models.Model):
    _name = 'g2p.region'
    
    name = fields.Char(string="Name")
    

class Zone(models.Model):
    _name = 'g2p.zone'
    _rec_name="code"
    
    
    region = fields.Many2one("g2p.region", string="Region")
    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    


class Woreda(models.Model):
    _name = 'g2p.woreda'
    _rec_name="code"
    
    
    zone = fields.Many2one("g2p.zone", string="Zone")
    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    


class Kebele(models.Model):
    _name = 'g2p.kebele'
    _rec_name="code"
    
    woreda = fields.Many2one("g2p.woreda", string="Woreda")
    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    

