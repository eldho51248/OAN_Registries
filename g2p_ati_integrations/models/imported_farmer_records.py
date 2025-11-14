import json

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ImportedRecordSource(models.Model):
    _name = 'g2p.imported.record.source'
    _description = 'Imported Record Source'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color Index', default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Source name already exists!"),
    ]



class G2PImportedRecord(models.Model):
    _name = "g2p.imported.record"
    _description = "Imported Record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char()
    given_name = fields.Char(string="First Name")
    family_name = fields.Char(string="Father's Name")
    gf_name_eng = fields.Char(string="Grand Father's Name")
    phone = fields.Char(required=True)
    gender = fields.Char()
    region = fields.Char()
    state = fields.Selection(selection=[("draft", "Draft"), ("moved", "Created")], default="draft")
    language = fields.Char()
    record_from = fields.Char()
    record_type = fields.Selection(selection=[("single", "Single Source"), ("composed", "Composed")])
    db_import = fields.Boolean("Imported", default=False)
    zone = fields.Char(string="Zone")
    woreda = fields.Char(string="Woreda")
    kebele = fields.Char(string="Kebele")
    source = fields.Json(string="Source Information", help="Stores the source information in JSON format")
    source_ids = fields.Many2many('g2p.imported.record.source', compute='_compute_source_ids', string='Sources', store=False)
    
    @api.depends('source')
    def _compute_source_ids(self):
        source_model = self.env['g2p.imported.record.source']
        for record in self:
            source_ids = []
            if record.source:
                # Handle both single source and list of sources
                sources = [record.source] if isinstance(record.source, dict) else record.source
                if not isinstance(sources, list):
                    sources = [sources]
                    
                for src in sources:
                    if not src:
                        continue
                    source_name = src.get('source', 'Unknown')
                    # Find or create source record
                    source = source_model.search([('name', '=', source_name)], limit=1)
                    if not source:
                        source = source_model.create({'name': source_name})
                    source_ids.append(source.id)
            
            record.source_ids = [(6, 0, source_ids)] if source_ids else False


    assigned_region = fields.Many2one(
        "g2p.region", string="Regions Assigned"
    )
    assigned_languages = fields.Many2many(
        "g2p.lang", string="Language Assigned"
    )

    _sql_constraints = [
        ("phone_unique", "unique(phone)", "The phone number must be unique."),
    ]


    @api.constrains('assigned_region', 'assigned_languages')
    def _check_region_languages(self):
        for record in self:
            if record.assigned_region and not record.assigned_languages:
                raise ValidationError(_("Please specify at least one language when a region is assigned."))
            if record.assigned_languages and not record.assigned_region:
                raise ValidationError(_("Please specify a region when languages are assigned."))



    @api.onchange("family_name", "given_name", "gf_name_eng")
    def name_change_farmer(self):
        name = ""
        if self.given_name:
            name += self.given_name + " "
        if self.family_name:
            name += self.family_name + " "
        if self.gf_name_eng:
            name += self.gf_name_eng

        self.name = name.upper()

    def action_view_draft_records(self):
        return {
            "name": "Draft Records",
            "type": "ir.actions.act_window",
            "res_model": "draft.record",
            "view_mode": "kanban,form",
            "domain": [("import_record_id", "=", self.id)],
            "context": dict(self.env.context, default_import_record_id=self.id),
        }


    def action_to_draft(self):
        
        for record in self:
            associated_records = self.env["draft.record"].sudo().search([
                ("import_record_id", "=", record.id)
            ])

            # Check for published records
            if any(rec.state == "published" for rec in associated_records):
                raise ValidationError(
                    _("Cannot set to draft. There are associated records that are already published.")
                )

            # Only non-admin users are restricted by create_uid
            if not self.env.user.has_group("g2p_draft_publish.group_int_admin"):
                unauthorized_records = associated_records.filtered(
                    lambda rec: rec.create_uid.id != self.env.uid
                )
                if unauthorized_records:
                    raise ValidationError(
                        _("You cannot remove associated records that were not created by you.")
                    )

            # Admins or allowed users can delete the records
            associated_records.unlink()
            record.write({"state": "draft"})




    def action_move(self):
        self.write({"state": "moved"})

    def create_draft_imported_record(self):
        self.ensure_one()

        started = self.env["g2p.validation.status"].sudo().search([("name", "=", "Started")])
        partner_data = {
            "given_name": self.given_name,
            "family_name": self.family_name,
            "addl_name": self.gf_name_eng,
            "gf_name_eng": self.gf_name_eng,
            "phone": self.phone,
            "gender": self.gender,
            "region": self.region,
        }

        data = {
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "addl_name": self.gf_name_eng,
            "gf_name_eng": self.gf_name_eng,

            "phone": self.phone,
            "gender": self.gender,
            "region": self.region,
            "import_record_id": self.id,
            "validation_status": started.id,
            "partner_data": json.dumps(partner_data),
        }

        new_record = self.env["draft.record"].sudo().create(data)
        new_record.sudo().write({"message_partner_ids": [(6, 0, self.message_partner_ids.ids)]})

        self.write({"state": "moved"})

        return {
            "name": "Draft Records",
            "type": "ir.actions.act_window",
            "res_model": "draft.record",
            "view_mode": "kanban,form,tree",
            "domain": [("import_record_id", "=", self.id)],
            "context": dict(self.env.context, default_import_record_id=self.id),
        }

    def assign_records(self):
        return {
            "name": "Draft Records",
            "type": "ir.actions.act_window",
            "res_model": "assign.records.wizard",
            "view_mode": "form",
            "target": "new",
        }
