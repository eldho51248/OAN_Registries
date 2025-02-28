import json
from odoo import http
from odoo.http import request

class LandAPIController(http.Controller):
    @http.route('/api/land_info', type='http', auth='public', methods=['GET'], csrf=False)
    def get_national_id_info(self, land_id=None):
        if not land_id:
            return request.make_response(
                json.dumps({"error": "Missing land_id"}),
                headers=[('Content-Type', 'application/json')]
            )

        try:
            partner = request.env['res.partner'].sudo().search([('land_information_ids.land_id', '=', land_id)], limit=1)

            if not partner:
                return request.make_response(
                    json.dumps({"error": "No partner found for this land_id"}),
                    headers=[('Content-Type', 'application/json')]
                )

            national_id_info = [{"id_number": reg.id_number, "id_type": reg.id_type} for reg in partner.reg_ids]

            response_data = {
                "partner_id": partner.id,
                "national_ids": national_id_info
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api', type='http', auth='none', methods=['GET'], csrf=False)
    def get_api(self):
        return request.make_response(
            json.dumps({"message": "Welcome to the Land API"}),
            headers=[('Content-Type', 'application/json')]
        )