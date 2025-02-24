from odoo import models, fields, api, _

class G2PValidationStatus(models.Model):
    _name = 'g2p.validation.status'
    _fold_name = 'fold'
    
    fold = fields.Boolean(string= 'Folded in Kanban', default=False)
    name = fields.Char()


class NarlisIntegration(models.Model):
    _name = 'narlis.integration'

    end_point_url = fields.Char()
    api_key = fields.Char()
    host_url = fields.Char()
