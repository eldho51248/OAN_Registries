# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.portal.controllers.web import Home as PortalHome
from odoo.addons.web.controllers.utils import is_user_internal
from odoo.addons.portal.controllers import portal as portal_controller


class ConsentPortalWebHome(PortalHome):
    """Redirect consent portal users to /consent/management after login."""

    def _login_redirect(self, uid, redirect=None):
        if not redirect and not is_user_internal(uid):
            user = http.request.env["res.users"].sudo().browse(uid)
            if user.consent_parent_partner_id:
                redirect = "/consent/management"
        return super()._login_redirect(uid, redirect=redirect)


class ConsentCustomerPortal(portal_controller.CustomerPortal):
    """Redirect /my and /my/home to consent management for consent portal users."""

    @http.route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        if http.request.env.user.consent_parent_partner_id:
            return http.request.redirect("/consent/management")
        return super().home(**kw)
