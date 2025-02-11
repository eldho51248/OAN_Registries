from odoo import models, fields, api
import json
from odoo.exceptions import ValidationError


class G2PImportedFarmerRecord(models.Model):
    _inherit = 'g2p.imported.record'

    zone = fields.Char(string="Zone")
    woreda = fields.Char(string="Woreda")
    kebele = fields.Char(string="Kebele")
    
 
  
    def create_draft_imported_record(self):
        self.ensure_one() 
        
        enrichment_started = self.env.ref('g2p_draft_publish.enrichment_started')
        
        partner_data = {
            # 'name': self.name,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'gf_name_eng': self.gf_name_eng,
            'phone': self.phone,
            'gender': self.gender,
            'region': self.region,
            'zone': self.zone,
            'woreda': self.woreda,
            'kebele': self.kebele,
            'primary_language': self.language,
        }
        
        data = {
            'name': self.name,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'gf_name_eng': self.gf_name_eng,
            'phone': self.phone,
            'gender': self.gender,
            'region': self.region,
            'zone': self.zone,
            'woreda': self.woreda,
            'kebele': self.kebele,
            'import_record_id': self.id,
            'partner_data' : json.dumps(partner_data),
            'validation_status': enrichment_started.id
            
        }
        
        

        new_record = self.env['draft.imported.record'].sudo().create(data)
        new_record.sudo().write({
            'message_partner_ids': [(6, 0, self.message_partner_ids.ids)]
        })
        
        self.write({"state": "moved"})
        
        return {
            'name': 'Draft Records',
            'type': 'ir.actions.act_window',
            'res_model': 'draft.imported.record',
            'view_mode': 'kanban,form,tree',
            'domain': [('import_record_id', '=', self.id)],
            'context': dict(self.env.context, default_import_record_id=self.id),
        }

