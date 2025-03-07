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

                url = f"{api_parameters.host_url}{api_parameters.end_point_url}={self.land_id}&data-depth=2"
                headers = {
                    "api-key": api_parameters.api_key,
                    "Host": api_parameters.host_url,
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx
                polygon_coords = response.json()

                if not polygon_coords:
                    raise UserError(_("No data received from the API."))
                self.polygon_data = polygon_coords
                polygone_data = ast.literal_eval(self.polygon_data)

                action = {
                        'type': 'ir.actions.act_window',
                        'name': 'Partner Map',
                        'res_model': 'g2p.land.information',
                        'view_mode': 'lmap',
                        'view_id': self.env.ref('g2p_ati_integrations.action_partner_map_view').id,
                        'target': 'new',
                        'context': {'polygon_coords':  polygone_data,
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


    def action_open_wizard(self):

        self.ensure_one()
        active_id = self.id

        if not self.partner_data:
            raise UserError("No partner data available to edit.")
        try:
            json_data = json.loads(self.partner_data)

        except json.JSONDecodeError:
            raise UserError("Invalid JSON data in partner_data.")

        partner_model_fields = self.env['res.partner']._fields
        _logger.info("the set of fields")
        _logger.info(self.env['res.partner']._fields)
        _logger.info("the set of the json")
        _logger.info(json_data.items())
        additional_g2p_info = {}
        context_data = {}

        # excluded = ["land_information_ids", "crop_information_ids", "livestock_information_ids", "phone_number_ids", "reg_ids"]

        for field_name, field_value in json_data.items():

            if field_name not in partner_model_fields:
                additional_g2p_info[field_name] = field_value
                continue


            field = partner_model_fields[field_name]

            if field.type == 'datetime' and isinstance(field_value, str):
                _logger.info(f"the datetime field {field_name}")
                try:
                    field_value = datetime.fromisoformat(field_value)
                    context_data[f"default_{field_name}"] = field_value
                except ValueError:
                    pass

            elif field.type == 'date' and isinstance(field_value, str):
                try:
                    field_value = date.fromisoformat(field_value)
                    context_data[f"default_{field_name}"] = field_value
                except ValueError:
                    pass  # If it's not a valid date string, leave it as is

            elif field.type == 'many2one':
                # _logger.info(f"the many2one field 01 {field_name}")

                    if isinstance(field_value, int):
                        field_value = int(field_value)
                        context_data[f"default_{field_name}"] = json_data[field_name]
                        _logger.info(f"the many2one field {field_name}")

                    if not isinstance(field_value, int):
                        additional_g2p_info[field_name] = field_value

            elif field.type == 'many2many':
                # _logger.info(f"the field {field_name}")
                if isinstance(field_value, list):
                    if all(isinstance(val, int) for val in field_value):
                        # If field_value is a list of IDs (int), update the many2many field
                        context_data[f"default_{field_name}"] = [(6, 0, field_value)]
                    elif all(hasattr(val, 'id') for val in field_value):
                        # If field_value is a list of records, extract their IDs
                        context_data[f"default_{field_name}"] = [(6, 0, [val.id for val in field_value])]
                    else:
                        additional_g2p_info[field_name] = field_value
                elif hasattr(field_value, 'id'):  # If field_value is a single record
                    # If field_value is a single record, update it as a list with one record
                    context_data[f"default_{field_name}"] = [(6, 0, [field_value.id])]
                else:
                    additional_g2p_info[field_name] = field_value


            elif field.type == 'selection':
                _logger.info(f"the field {field_name}")
                selection_values = field.get_values(env=self.env)
                if field_value in selection_values:
                    context_data[f"default_{field_name}"] = field_value
                if field_value not in selection_values:
                    additional_g2p_info[field_name] = field_value

            else:
                context_data[f"default_{field_name}"] = field_value


        if 'phone' in json_data and json_data['phone']:
            _logger.info("in phon condition1")
            if not 'phone_number_ids' in json_data:
                _logger.info("in phon condition")
                json_data['phone_number_ids'] = [[0, "virtual_01", {"phone_no": json_data['phone'], 'phone_type': 'primary'}]]
                self.partner_data = json.dumps(json_data)

        context_data['active_id'] = active_id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Farmer Data',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'view_id': self.env.ref('g2p_ati_integrations.g2p_validation_farmer_form_view').id,
            'target': 'new',
            # 'target': 'current',
            'context': {**context_data, 'default_is_farmer': 'yes', 'default_additional_g2p_info': json.dumps(additional_g2p_info),
                        'in_enrichment' : 'yes',
                        'default_land_information_ids': json_data.get('land_information_ids', []),
                        'default_crop_information_ids': json_data.get('crop_information_ids', []),
                        'default_livestock_information_ids': json_data.get('livestock_information_ids', []),
                        'default_phone_number_ids': json_data.get('phone_number_ids', []),
                        'default_reg_ids': json_data.get('reg_ids', [])
                        },
        }


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


    def action_save_to_draft(self,vals):

        context = self.env.context
        model_name = context.get('active_model')
        record_id = context.get('active_id')
        active_record = self.env[model_name].browse(record_id)
        partner_data = json.loads(active_record.partner_data) or {}

        m2m_fields = {
                    'hh_income_type': 'source_of_income',
                    'crop_water_sources': 'crop_water_source',
                    'livestock_water_sources': 'livestock_water_sources',
                    'type_of_machinery': 'type_of_machinery',
                    'finance_accesses': 'finance_accesses',
                    }

        processed_m2m_fields = {}
        for field, key in m2m_fields.items():
            processed_m2m_fields[field] = [item[1] for item in vals.get(field, [])]


        dynamic_fields = {
            'is_farmer': 'yes',
            'is_company': False,
            'is_group': False,
            'is_registrant': True,
            'db_import': 'yes',
            **processed_m2m_fields
        }

        static_fields = [
            'given_name', 'family_name', 'gf_name_eng', 'first_name_amh', 'family_name_amh',
            'gf_name_amh', 'has_national_id', 'birthdate', 'birthdate_ec', 'region', 'zone',
            'woreda', 'kebele', 'email', 'has_personal_phone', 'gender', 'primary_Language',
            'hh_is_household_head', 'farming_type', 'is_member_of_primary_cooperative',
            'is_member_of_cooperative_union', 'is_member_in_farmer_cluster', 'primary_cooperatives',
            'cooperative_unions', 'primary_commodity', 'role_in_farmer_cluster',
            'do_you_use_fertilizer', 'do_you_use_pesticide', 'do_you_use_insecticide',
            'do_you_use_improved_seed', 'access_to_machinery', 'martial_status', 'education',
            'is_disabled', 'has_finance_access', 'phone_number_ids', 'reg_ids', 'land_information_ids',
            'crop_information_ids', 'livestock_information_ids', 'additional_g2p_info'
        ]


        _logger.info("here is the vals of the save")
        _logger.info(f" region { vals.get('region')}, zone { vals.get('zone')}, woreda { vals.get('woreda')}, kebele { vals.get('kebele')} ")

        draft_record = {}

        draft_record.update(dynamic_fields)

        for field in static_fields:
            if field in self.env[model_name]._fields:
                draft_record[field] = vals.get(field) or partner_data.get(field)
            else:
                if vals.get(field):
                    draft_record[field] = vals[field]

        if vals.get('given_name') or vals.get('family_name') or vals.get('gf_name_eng'):
            draft_record['name'] = f"{vals.get('given_name', '').upper()} {vals.get('family_name', '').upper()} {vals.get('gf_name_eng', '').upper()}".strip()


        active_record.write({
            'partner_data': json.dumps(draft_record)
        })







