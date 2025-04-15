from odoo import fields, models
from odoo.exceptions import ValidationError


class G2PValidationStatus(models.Model):
    _name = "g2p.validation.status"
    _fold_name = "fold"

    fold = fields.Boolean(string="Folded in Kanban", default=False)
    name = fields.Char()

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique.')
    ]



    def create(self, vals):
        if self.search([('name', '=', vals['name'].lower())]):
            raise ValidationError("The name must be unique (case-insensitive).")
        return super().create(vals)

    def write(self, vals):
        if 'name' in vals:
            existing_record = self.search([('name', '=', vals['name'].lower())])
            if existing_record and existing_record.id != self.id:
                raise ValidationError("The name must be unique (case-insensitive).")
        return super().write(vals)

class NarlisIntegration(models.Model):
    _name = "narlis.integration"

    end_point_url = fields.Char()
    api_key = fields.Char()
    host_url = fields.Char()
