# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PartnerApprovalWizard(models.TransientModel):
    _name = 'partner.approval.wizard'
    _description = 'Partner Approval Confirmation Wizard'

    partner_ids = fields.Many2many('res.partner', string='Partners to Approve')
    websub_status = fields.Text(string='WebSub Status', readonly=True)
    kafka_status = fields.Text(string='Kafka Status', readonly=True)
    warning_message = fields.Text(string='Warning Message', readonly=True)
    
    @api.model
    def default_get(self, fields_list):
        """Set default values including WebSub/Kafka status check"""
        res = super().default_get(fields_list)
        
        # Get partner IDs from context
        partner_ids = self.env.context.get('active_ids', [])
        if partner_ids:
            res['partner_ids'] = [(6, 0, partner_ids)]
        
        # Check WebSub and Kafka status
        websub_status, kafka_status, warning_msg = self._check_services_status()
        res['websub_status'] = websub_status
        res['kafka_status'] = kafka_status
        res['warning_message'] = warning_msg
        
        return res
    
    def _check_services_status(self):
        """Check WebSub and Kafka services status"""
        import requests
        
        websub_status = "❌ Not Configured"
        kafka_status = "❌ Not Accessible"
        warning_msg = ""
        
        # Check WebSub configurations
        websub_configs = self.env["g2p.datashare.config.websub"].search([
            ('active', '=', True)
        ])
        
        if not websub_configs:
            websub_status = "❌ No Active Configurations"
            warning_msg += "• No active WebSub configurations found\n"
        else:
            # Test WebSub connectivity
            websub_working = False
            for config in websub_configs:
                try:
                    if config.websub_base_url:
                        response = requests.get(config.websub_base_url, timeout=5)
                        if response.status_code in [200, 404]:  # 404 is OK for hub discovery
                            websub_working = True
                            break
                except Exception as e:
                    continue
            
            if websub_working:
                websub_status = f"✅ Working ({len(websub_configs)} configs)"
            else:
                websub_status = f"❌ Not Accessible ({len(websub_configs)} configs)"
                warning_msg += "• WebSub service is not accessible\n"
        
        # Check Kafka connectivity
        kafka_ui_urls = [
            "http://localhost:8081",
            "http://kafka-ui:8080", 
            "http://127.0.0.1:8081"
        ]
        
        kafka_working = False
        for kafka_url in kafka_ui_urls:
            try:
                response = requests.get(kafka_url, timeout=3)
                if response.status_code == 200:
                    kafka_working = True
                    kafka_status = f"✅ Working ({kafka_url})"
                    break
            except:
                continue
        
        if not kafka_working:
            kafka_status = "❌ Not Accessible"
            warning_msg += "• Kafka service is not accessible\n"
        
        if warning_msg:
            warning_msg = "⚠️ Issues detected:\n" + warning_msg + "\nYou can still approve partners, but WebSub events may not be published."
        else:
            warning_msg = "✅ All services are working properly. Partners will be approved and WebSub events will be published."
        
        return websub_status, kafka_status, warning_msg
    
    def action_approve_with_publishing(self):
        """Approve partners and attempt to publish WebSub events"""
        partners = self.partner_ids.filtered(lambda p: p.state != 'approved')
        
        for partner in partners:
            try:
                # Approve the partner
                partner.write({'state': 'approved'})
                
                # Try to publish WebSub event
                if partner.is_registrant:
                    event_type = "WEBSUB_GROUP_CREATED" if partner.is_group else "WEBSUB_INDIVIDUAL_CREATED"
                    data = {"id": partner.id}
                    
                    self.env["g2p.datashare.config.websub"].publish_event(event_type, data)
                    _logger.info("Partner %s approved and WebSub event published", partner.name)
                
            except Exception as e:
                _logger.error("Failed to publish WebSub event for partner %s: %s", partner.name, str(e))
                # Continue with approval even if WebSub fails
        
        return {'type': 'ir.actions.act_window_close'}
    
    def action_approve_without_publishing(self):
        """Approve partners without publishing WebSub events"""
        partners = self.partner_ids.filtered(lambda p: p.state != 'approved')
        
        for partner in partners:
            partner.write({'state': 'approved'})
            _logger.info("Partner %s approved without WebSub publishing", partner.name)
        
        return {'type': 'ir.actions.act_window_close'}
    
    def action_cancel(self):
        """Cancel the approval process"""
        return {'type': 'ir.actions.act_window_close'}
