# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo import api, models, _
import logging

_logger = logging.getLogger(__name__)


class ResPartnerATI(models.Model):
    _inherit = "res.partner"

    def state_approve(self):
        """
        Override state approval to show confirmation wizard with WebSub/Kafka status
        """
        # Return wizard action to show approval confirmation
        return {
            'name': _('Partner Approval Confirmation'),
            'type': 'ir.actions.act_window',
            'res_model': 'partner.approval.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_ids': self.ids,
                'active_model': 'res.partner',
            }
        }

    def write(self, vals):
        """
        Override write to handle state changes and publish for approved partners
        """
        # Store old states before update
        old_states = {rec.id: rec.state for rec in self if rec.is_registrant}

        res = super().write(vals)

        # Only publish for approved partners and field updates (not state changes handled by state_approve)
        for rec in self:
            if rec.is_registrant and rec.state == 'approved':
                old_state = old_states.get(rec.id)

                # Only publish updates if partner was already approved (not newly approved)
                if old_state == 'approved':
                    try:
                        new_vals = vals.copy()
                        new_vals["id"] = rec.id
                        event_type = "WEBSUB_GROUP_UPDATED" if rec.is_group else "WEBSUB_INDIVIDUAL_UPDATED"

                        _logger.info("Approved partner %s (ID: %s) was updated. Publishing WebSub event: %s",
                                    rec.name, rec.id, event_type)
                        self.env["g2p.datashare.config.websub"].publish_event(event_type, new_vals)

                    except Exception as e:
                        _logger.error("Failed to publish WebSub update event for partner %s: %s", rec.name, str(e))

        return res
