# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo import api, models

import logging

_logger = logging.getLogger(__name__)


class ResPartnerATIWebsub(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
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

    def write(self, vals):
        old_states = {rec.id: rec.state for rec in self if rec.is_registrant}
        res = super().write(vals)

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
