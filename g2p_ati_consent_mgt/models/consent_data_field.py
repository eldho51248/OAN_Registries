from odoo import fields, models


class G2PConsentDataField(models.Model):
    _name = "g2p.consent.data.field"
    _description = "Consent Data Field"
    _rec_name = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("g2p_consent_data_field_code_uniq", "unique(code)", "Data field code must be unique."),
    ]
