from urllib.parse import quote

from odoo import http
from odoo.http import request


class AtiServiceProviderLoginRedirect(http.Controller):
    """Route serviceprovider login through Odoo web login without external addon imports."""

    def _redirect_to_default_login(self, redirect_uri):
        redirect_uri = redirect_uri or "/serviceprovider/home"
        return request.redirect("/web/login?redirect=%s" % quote(redirect_uri, safe=""))

    def _redirect_authenticated_user(self, redirect_uri):
        user = request.env.user
        if user and user.consent_parent_partner_id:
            return request.redirect("/consent/management")
        return request.redirect(redirect_uri)

    @http.route(["/serviceprovider"], type="http", auth="public", website=True)
    def portal_root(self, **kwargs):
        redirect_uri = request.params.get("redirect") or "/serviceprovider/home"
        if request.session and request.session.uid:
            return self._redirect_authenticated_user(redirect_uri)
        return self._redirect_to_default_login(redirect_uri)

    @http.route(["/serviceprovider/login"], type="http", auth="public", website=True)
    def service_provider_login(self, **kwargs):
        redirect_uri = request.params.get("redirect") or "/serviceprovider/home"
        if request.session and request.session.uid:
            return self._redirect_authenticated_user(redirect_uri)
        return self._redirect_to_default_login(redirect_uri)
