# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenG2P ATI: WebSub Integration",
    "category": "G2P",
    "version": "17.0.1.5.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": [
        "g2p_registry_datashare_websub",
        "g2p_ati",
    ],
    "external_dependencies": {},
    "data": [
        "security/ir.model.access.csv",
        "views/datashare_config_websub_ati.xml",
        "wizard/partner_approval_wizard.xml",
    ],
    "assets": {
        "web.assets_backend": [],
    },
    "demo": [],
    "images": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}
