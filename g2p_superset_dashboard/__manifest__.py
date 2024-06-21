# -*- coding: utf-8 -*-
{
    'name' : 'G2P Superset Dashboard',
    'version' : '1.0',
    'summary': 'G2P Superset Dashboard',
    'description': """G2P Superset Custom Dashboard""",
    'category': 'Report',
    'depends' : ['base', 'web', 'g2p_registry_base'],
    'data': [
        'views/res_config_settings.xml',
        'views/superset_dashboard.xml'        
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'g2p_superset_dashboard/static/src/components/**/*.js',
            'g2p_superset_dashboard/static/src/components/**/*.xml',
            'g2p_superset_dashboard/static/src/components/**/*.css',
            'g2p_superset_dashboard/static/src/components/**/*.scss',
        ],
    },
}
