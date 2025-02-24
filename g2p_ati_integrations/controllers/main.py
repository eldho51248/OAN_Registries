from odoo import http
from odoo.http import request
class FarmerAPI(http.Controller):
    @http.route('/api/farmer_profile', type='http', auth='user')

    def get_farmer_profile(self, **kwargs):
        farmer_id = request.env.user.id
        print("the farmer is",farmer_id)

        farmer = request.env['res.partner'].sudo().browse(farmer_id)
        if farmer:
            return {
                'name': farmer.name,
                'land_info': [{'id': land.id, 'area': land.area} for land in farmer.land_information_ids],
            }
        return {'error': 'Farmer not found'}

class NarlisIntegrationController(http.Controller):
    @http.route('/get_narlis_url', type='json', auth='user')
    def get_narlis_url(self):
        integration = request.env['narlis.integration'].sudo().search([], limit=1)
        return {'url': integration.url if integration else ''}


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
