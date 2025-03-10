import requests
from odoo import models, fields, api, _
import json
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
import logging
from typing import Dict, List
_logger = logging.getLogger(__name__)
import ast


class G2PLandInformation(models.Model):
    _inherit = "g2p.land.information"

    polygon_data = fields.Text(string="Polygon Data")
    current_land_use = fields.Text(string="Current Land Use")
    soil_fertility = fields.Text(string="Soil Fertility")
    means_of_acquisition = fields.Text(string="Means Of Acquisition")
    year_of_acquisition = fields.Date(string="Year Of Acquisition")


    def fetch_land_records(self):

        try:
            api_parameters = self.env["narlis.integration"].sudo().search([], limit=1)
            land_records = self.env["g2p.land.information"].sudo().search([])
            if not api_parameters:
                raise UserError(_("API configuration is missing. Please configure in settings"))

            for land in land_records:
                url = f"{api_parameters.host_url}{api_parameters.end_point_url}"
                headers = {
                    "api-key": api_parameters.api_key,
                }
                params = {
                    "version": "v1",
                    "upid": land.land_id,
                    "data-depth": "2"
                }
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx
                land_informations = response.json()
                isorphan = land_informations.get("parcel", {}).get("rights", [{}])[0].get("party", {}).get("isorphan")
                land.partner_id.is_orphan = isorphan.lower()
                land.polygon_data = land_informations["parcel"]["geometryWkt"]
                land.current_land_use = land_informations["parcel"]["landUse"]
                land.total_land_area = land_informations["parcel"]["parcelArea"]
                # land.polygon_data = land_informations


        except requests.exceptions.RequestException as e:
            raise UserError(_("Failed to fetch land data: %s") % str(e))

    def action_open_map_view(self):

        if self.polygon_data:
            land_details = []
            polygone_data = ast.literal_eval(self.polygon_data)

            land_info = {
                'total_land_area': self.total_land_area,
                'polygon_data': polygone_data,
                'ownership_type': self.ownership_type
            }
            land_details.append(land_info)
            # List to store details of all lands

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Partner Map',
                'res_model': 'g2p.land.information',
                'view_mode': 'lmap',
                'view_id': self.env.ref('g2p_ati_integrations.action_partner_map_view').id,
                'target': 'new',
                'context': {'polygon_coords': land_details,
                            'partner_latitiude': self.partner_id.partner_latitude,
                            'partner_longitude': self.partner_id.partner_longitude
                            },  # Passing polygon data
            }
            return action
        else:
            try:
                api_parameters = self.env["narlis.integration"].sudo().search([], limit=1)
                if not api_parameters:
                    raise UserError(_("API configuration is missing. Please configure in settings"))


                url = f"{api_parameters.host_url}{api_parameters.end_point_url}"
                headers = {
                    "api-key": api_parameters.api_key,
                }
                params = {
                    "version": "v1",
                    "upid": self.land_id,
                    "data-depth": "2"
                }
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx
                land_informations = response.json()
                isorphan = land_informations.get("parcel", {}).get("rights", [{}])[0].get("party", {}).get(
                    "isorphan")
                self.partner_id.is_orphan = isorphan.lower()
                self.polygon_data = land_informations["parcel"]["geometryWkt"]
                self.current_land_use = land_informations["parcel"]["landUse"]
                self.total_land_area = land_informations["parcel"]["parcelArea"]

                action = {
                        'type': 'ir.actions.act_window',
                        'name': 'Partner Map',
                        'res_model': 'g2p.land.information',
                        'view_mode': 'lmap',
                        'view_id': self.env.ref('g2p_ati_integrations.action_partner_map_view').id,
                        'target': 'new',
                        'context': {'polygon_coords':  self.polygon_data,
                                    'partner_latitiude': self.partner_id.partner_latitude,
                                    'partner_longitude': self.partner_id.partner_longitude
                                    },  # Passing polygon data
                    }
                return action
            except requests.exceptions.RequestException as e:
                raise UserError(_( "Failed to fetch map data: %s") % str(e))




class G2PDraftRecord(models.Model):
    _inherit = "draft.record"

    gf_name_eng = fields.Char(string="Last Name")
    zone = fields.Char(string="Zone")
    woreda = fields.Char(string="Woreda")
    kebele = fields.Char(string="Kebele")
    validation_status = fields.Many2one("g2p.validation.status")
    import_record_id = fields.Many2one("g2p.imported.record", string="Import Record")


    def action_change_state(self):
        return {
            "name": "Confirm Rejection",
            "type": "ir.actions.act_window",
            "res_model": "change.state.wizard",
            "view_mode": "form",
            "view_id": self.env.ref("g2p_ati_integrations.change_state_wizard_view").id,
            "target": "new",
        }

    def action_publish(self):
        self.ensure_one()
        partner_data = json.loads(self.partner_data)
        res_partner_model = self.env['res.partner']

        # Fetch all fields metadata from res.partner
        fields_metadata = res_partner_model.fields_get()

        # Dictionary to store valid fields and values
        valid_data = {}

        given_name = partner_data.get('given_name', '')
        family_name = partner_data.get('family_name', '')
        gf_name_en = partner_data.get('gf_name_eng', '')

        for field_name, value in partner_data.items():
            if field_name in fields_metadata:
                field_info = fields_metadata[field_name]
                field_type = field_info.get('type')

                # Validation based on field type
                if field_type == 'char' and isinstance(value, str):
                    valid_data[field_name] = value
                if (field_type == 'date' or field_type =='datetime')  and isinstance(value, str):
                    valid_data[field_name] = date.fromisoformat(value)
                elif field_type == 'integer' and isinstance(value, int):
                    valid_data[field_name] = value
                elif field_type == 'float' and isinstance(value, (int, float)):
                    valid_data[field_name] = float(value)
                elif field_type == 'boolean' and isinstance(value, bool):
                    valid_data[field_name] = value
                elif field_type == 'many2one' and isinstance(value, int):
                    # Check if the referenced record exists
                    if self.env[field_info['relation']].browse(value).exists():
                        valid_data[field_name] = value
                elif field_type == 'selection':
                    selection_options = [option[0] for option in field_info.get('selection', [])]
                    if value in selection_options:
                        valid_data[field_name] = value

        # Create the res.partner record with valid data
        if valid_data:
            valid_data['db_import'] = 'yes'
            valid_data['name'] = f"{given_name} {family_name} {gf_name_en}".upper()

            new_partner = res_partner_model.create(valid_data)
            self.write({'state':'published'})
        else:
            raise ValueError("No valid data found to create a partner record.")

class G2PRespartnerIntegration(models.Model):
    _inherit = 'res.partner'

    is_orphan = fields.Selection([("yes", "Yes"), ("no", "No")])
    asigned_region = fields.Many2one("g2p.region")
    language_skills = fields.Many2many('g2p.lang', string='Languages')



    def view_all_lands(self):
        land_details = []  # List to store details of all lands
        for land in self.land_information_ids:
            if land.polygon_data:
            # Parse the string representation of the polygon data into an actual list of coordinates
                try:
                    polygon = ast.literal_eval(land.polygon_data)
                except (ValueError, SyntaxError):
                    print(f"Invalid polygon data: {land.polygon_data}")
                    continue

                # Collect all the relevant land information in a dictionary
                land_info = {
                    'total_land_area': land.total_land_area,
                    'polygon_data': polygon,
                    'ownership_type': land.ownership_type
                }

                land_details.append(land_info)
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Partner Map',
            'res_model': 'res.partner',
            'view_mode': 'lmap',
            'view_id': self.env.ref('g2p_ati_integrations.action_partner_map_view').id,
            'target': 'new',
            'context': {'polygon_coords': land_details,
                        'partner_latitiude': self.partner_latitude,
                        'partner_longitude': self.partner_longitude
                        },  # Passing polygon data
        }
        return action





