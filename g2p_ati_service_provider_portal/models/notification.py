from odoo import fields, models


class Notification(models.Model):
    _name = "g2p.ati.notification"
    _description = "G2p ATI Notification"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    notified_user = fields.Many2one("res.users", string="Notified User", requried=True)
    message = fields.Text(string="Message", requried=True)
    title = fields.Text(string="Title", requried=True)
    has_seen = fields.Boolean(string="has seen", default=False)