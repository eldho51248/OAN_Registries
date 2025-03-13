import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info('Starting post-migration for version 17.0-1.5.0')
    
    env.cr.execute("""
        UPDATE res_partner
        SET farming_type = CASE
            WHEN farming_type = 'crop_farming' THEN 'crop_farming'
            WHEN farming_type = 'livestock_farming' THEN 'livestock_farming'
            WHEN farming_type = 'mixed_farming' THEN 'mixed_farming'
            ELSE farming_type
        END
    """)
    
    _logger.info('Completed post-migration for version 17.0-1.5.0')