from odoo import models, fields, api, _

class G2PValidationStatus(models.Model):
    _name = 'g2p.validation.status'
    _fold_name = 'fold'
    
    fold = fields.Boolean(string= 'Folded in Kanban', default=False)
    name = fields.Char()
