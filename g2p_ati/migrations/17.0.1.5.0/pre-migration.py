import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if version == "17.0.1.3.0":
        env = api.Environment(cr, SUPERUSER_ID, {})

        cr.execute("""
        SELECT id FROM g2p_document_tag WHERE name = 'Profile Image'
            """)
                   
        profile_image_tag = cr.fetchone()

        if profile_image_tag:
            profile_image_id = profile_image_tag[0]

            cr.execute(""" SELECT id, res_id FROM ir_model_data WHERE model = 'g2p.document.tag' AND module = 'g2p_profile_image' AND name = 'document_tag_profile_image'
                """)
            ir_model_data_entry = cr.fetchone()
            
            if ir_model_data_entry:
                ir_model_data_id, res_id = ir_model_data_entry

                if res_id != profile_image_id:
                    cr.execute("""
                        UPDATE ir_model_data SET res_id = %s WHERE id = %s
                    """, (profile_image_id, ir_model_data_id))

            else:
                    env['ir.model.data'].create({
                        'module': 'g2p_profile_image',
                        'name': 'document_tag_profile_image',
                        'model': 'g2p.document.tag',
                        'res_id': profile_image_id,
                    })

        