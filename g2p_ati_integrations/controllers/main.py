from odoo import http
from odoo.http import request

class LandAPIController(http.Controller):

    @http.route('/api/land_info', type='json', auth='public', methods=['POST'], csrf=False)
    def get_national_id_info(self, land_id):
        if not land_id:
            return {"error": "Missing land_id"}

        partner = request.env['res.partner'].sudo().search([('land_information_ids.land_id', '=', land_id)], limit=1)

        if not partner:
            return {"error": "No partner found for this land_id"}

        national_id_info = [{"id_number": reg.id_number, "id_type": reg.id_type} for reg in partner.reg_ids]

        return {"partner_id": partner.id, "national_ids": national_id_info}
