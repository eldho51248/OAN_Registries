{
    "name": "G2P Change Log",
    "version": "17.0.1.1.0",
    "author": "OpenG2P",
    "license": "",
    "website": "https://github.com/OpenG2P/openg2p-odoo-commons/g2p_change_log",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/audit_db_config.xml",
        "views/g2p_change_rule_view.xml",
        "views/g2p_change_log_view.xml",
        "views/g2p_change_log_line_view.xml",
    ],
    "external_dependencies": {
        "python": ["psycopg2"],
    },
    "application": True,
    "installable": True,
}
