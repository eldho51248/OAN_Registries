{
    "name": "Integration",
    "version": "17.0.0.2",
    # "currency": 'EUR',
    "summary": "Integration Module",
    "category": "tools",
    "description": """ 
""",
    "depends": ['g2p_draft_publish', 'g2p_ati'],
    "data": [
             "security/rules.xml",
            "security/ir.model.access.csv",
             "views/draft_imported_records.xml",
             "views/imported_farmer_records.xml",
    
             
             ],
    
       "assets": {
        "web.assets_backend": [
            "g2p_ati_integrations/static/src/**/*.js",
            "g2p_ati_integrations/static/src/**/*.css",
            "g2p_ati_integrations/static/src/**/*.scss",
            "g2p_ati_integrations/static/src/**/*.xml",
        ],
    },
    "author": "",
    'website': "",
    "installable": True,
    "application": False,
    "auto_install": False,
    # "images": ["static/description/Banner.gif"],
    "license":'',
}