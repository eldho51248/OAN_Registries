# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo import api, models, _,fields
import logging

_logger = logging.getLogger(__name__)

import importlib

websub = importlib.import_module(
    'odoo.addons.g2p_registry_datashare_websub.models.registrant'
)
_logger = logging.getLogger(__name__)
g2p_websub_model = websub.ResPartner 

def patched_write(self, vals):
    ICP = self.env["ir.config_parameter"].sudo()
    disable_websub = ICP.get_param("g2p.websub.disable_websub") 
    disable_websub=disable_websub.lower() if disable_websub else ""
    if disable_websub == 'false':
        old_states = {rec.id: rec.state for rec in self if rec.is_registrant}
        res = super(g2p_websub_model).write(vals)
        for rec in self:
            if not rec.is_registrant or rec.state != "approved":
                continue

            old_state = old_states.get(rec.id)
            new_vals = (vals or {}).copy()
            new_vals["id"] = rec.id
            new_vals = rec._sanitize_for_json(new_vals)

            if old_state != "approved":
                event_type = "WEBSUB_GROUP_CREATED" if rec.is_group else "WEBSUB_INDIVIDUAL_CREATED"
            else:
                event_type = "WEBSUB_GROUP_UPDATED" if rec.is_group else "WEBSUB_INDIVIDUAL_UPDATED"

            _logger.info(
                "Approved partner (ID: %s) change detected. Publishing WebSub event: %s",
                rec.id,
                event_type,
            )
            self.env["g2p.datashare.config.websub"].with_delay().publish_event(event_type, new_vals)

        return res

    
    _logger.info("Patched write: skipping datashare websub publishing")
    return super(g2p_websub_model, self).write(vals) 

g2p_websub_model.write = patched_write

@api.model_create_multi
def patched_create(self, vals_list):
    ICP = self.env["ir.config_parameter"].sudo()
    disable_websub = ICP.get_param("g2p.websub.disable_websub") 
    disable_websub=disable_websub.lower() if disable_websub else ""
    if disable_websub == 'false': 
        records = super(g2p_websub_model).create(vals_list)
        for record, vals in zip(records, vals_list):
            if not record.is_registrant or record.state != "approved":
                continue
            new_vals = (vals or {}).copy()
            new_vals["id"] = record.id
            new_vals = record._sanitize_for_json(new_vals)
            event_type = "WEBSUB_GROUP_CREATED" if record.is_group else "WEBSUB_INDIVIDUAL_CREATED"
            _logger.info(
                "Approved partner created (ID: %s). Publishing WebSub event: %s",
                record.id,
                event_type,
            )
            self.env["g2p.datashare.config.websub"].with_delay().publish_event(event_type, new_vals)
        return records
    _logger.info("Patched create: skipping datashare websub publishing")
    
    return super(g2p_websub_model, self).create(vals_list) 

g2p_websub_model.create = patched_create

