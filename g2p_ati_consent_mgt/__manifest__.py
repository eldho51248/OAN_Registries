# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenG2P ATI Consent Management",
    "summary": "Manage consent requests, consent partners, and portal users.",
    "version": "17.0.1.0.0",
    "category": "G2P",
    "author": "OpenG2P",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "portal",
        "g2p_ati",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/consent_model_access.xml",
        "views/res_partner_views.xml",
        "views/create_portal_user_wizard_views.xml",
        "views/consent_request_views.xml",
        "views/consent_data_field_views.xml",
        "views/res_partner_consent_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
