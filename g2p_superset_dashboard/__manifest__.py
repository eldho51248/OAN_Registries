{
    "name": "G2P Superset Dashboard",
    "version": "17.0.1.2.0",
    "author": "OpenG2P",
    "summary": "G2P Superset Dashboard",
    "category": "Report",
    "website": "https://openg2p.org",
    "depends": ["base", "web", "g2p_registry_base"],
    "data": ["views/res_config_settings.xml", "views/superset_dashboard.xml"],
    "demo": [],
    "license": "Other OSI approved licence",
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            "g2p_superset_dashboard/static/src/components/**/*.js",
            "g2p_superset_dashboard/static/src/components/**/*.xml",
            "g2p_superset_dashboard/static/src/components/**/*.css",
            "g2p_superset_dashboard/static/src/components/**/*.scss",
        ],
    },
}
