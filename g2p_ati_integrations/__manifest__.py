{
    "name": "Integration",
    "version": "17.0.0.2",
    "summary": "Integration Module",
    "category": "tools",
    "description": "",
    "depends": ["g2p_draft_publish", "g2p_ati", "g2p_leaflet_map"],
    "data": [
        "security/rules.xml",
        "security/ir.model.access.csv",
        "views/configurations.xml",
        "data/enrichment_status.xml",
        "data/land_integration_scheduled_action.xml",
        "views/draft_records.xml",
        "views/imported_farmer_records.xml",
        "views/imported_record.xml",
        "views/show_map.xml",
        "wizards/add_followers.xml",
        "wizards/assign_records.xml",
        "wizards/change_kanban_state.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "g2p_ati_integrations/static/src/**/*.js",
            "g2p_ati_integrations/static/src/**/*.css",
            "g2p_ati_integrations/static/src/**/*.scss",
            "g2p_ati_integrations/static/src/**/*.xml"
        ]
    },
    "author": "",
    "website": "",
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": ""
}