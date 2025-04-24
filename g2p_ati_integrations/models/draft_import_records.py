import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
import json
import logging
from typing import Dict, List
_logger = logging.getLogger(__name__)
import ast
BATCH_SIZE = 500

class G2PLandInformation(models.Model):
    _inherit = "g2p.land.information"

    polygon_data = fields.Text(string="Polygon Data")
    current_land_use = fields.Text(string="Current Land Use")
    soil_fertility = fields.Text(string="Soil Fertility")
    means_of_acquisition = fields.Text(string="Means Of Acquisition")
    year_of_acquisition = fields.Date(string="Year Of Acquisition")

    integration_status = fields.Selection([("valid", "Valid"), ("invalid", "Invalid")])


    def fetch_land_records(self):
        try:
            api_parameters = self.env["narlis.integration"].sudo().search([], limit=1)
            if not api_parameters:
                raise UserError(_("API configuration is missing. Please configure it in settings."))

            domain = ["|", ("integration_status", "=", False), ("integration_status", "=", "invalid")]

            total_records = self.env["g2p.land.information"].sudo().search_count(domain)

            for offset in range(0, total_records, BATCH_SIZE):
                land_records = self.env["g2p.land.information"].sudo().search(domain, limit=BATCH_SIZE, offset=offset)

                for land in land_records:
                    url = f"{api_parameters.host_url}{api_parameters.end_point_url}"
                    headers = {
                        "api-key": api_parameters.api_key,
                    }
                    params = {
                        "version": "v1",
                        "upid": land.land_id,
                        "data-depth": "3"
                    }

                    try:
                        response = requests.get(url, headers=headers, params=params, timeout=10)
                        response.raise_for_status()  # Raises an error for non-200 status codes

                        land_informations = response.json()

                        if not land_informations.get("parcel"):
                            land.integration_status = "invalid"
                            continue

                        # Extracting parcel data
                        parcel_data = land_informations.get("parcel", {})
                        rights_data = parcel_data.get("rights", [{}])[0]
                        party_data = rights_data.get("party", {})

                        # Updating land record fields
                        land.partner_id.is_orphan = party_data.get("isorphan", "").lower()
                        land.polygon_data = parcel_data.get("geometryWkt", "")
                        land.current_land_use = parcel_data.get("landUse", "")
                        land.total_land_area = parcel_data.get("parcelArea", 0)
                        land.integration_status = "valid"

                    except (requests.exceptions.Timeout,
                            requests.exceptions.ConnectionError,
                            requests.exceptions.RequestException,
                            ValueError):
                        land.integration_status = "invalid"
                        continue  # Skip this record and proceed with the next one

                # Commit changes to the database after processing a batch
                self.env.cr.commit()

        except UserError as e:
            raise e

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


    def update_land_id_prefix(self):
        records = self.search([])
        for record in records:
            if record.land_id.startswith("04/"):
                new_land_id = record.land_id.replace("04/", "OR/", 1)
            else:
                new_land_id = f"OR/07/06/{record.land_id}"

            record.land_id = new_land_id

        return True


class G2PDraftRecord(models.Model):
    _inherit = "draft.record"
    _order = "create_date desc"


    gf_name_eng = fields.Char(string="Last Name")
    zone = fields.Char(string="Zone")
    woreda = fields.Char(string="Woreda")
    kebele = fields.Char(string="Kebele")
    validation_status = fields.Many2one("g2p.validation.status")
    import_record_id = fields.Many2one("g2p.imported.record", string="Import Record")



    def action_change_state(self):
        return {
            "name": "Change State",
            "type": "ir.actions.act_window",
            "res_model": "change.state.wizard",
            "view_mode": "form",
            "view_id": self.env.ref("g2p_ati_integrations.change_state_wizard_view").id,
            "target": "new",
        }

    def write(self, vals):
        result = super().write(vals)

        partner_data_str = vals.get('partner_data')
        if partner_data_str:
            partner_data = json.loads(partner_data_str)

            self.given_name = partner_data.get("given_name")
            self.import_record_id.given_name = partner_data.get("given_name")
            self.family_name = partner_data.get('family_name')
            self.import_record_id.family_name = partner_data.get('family_name')
            self.gf_name_eng = partner_data.get('gf_name_eng')
            self.import_record_id.gf_name_eng = partner_data.get('gf_name_eng')
            self.gender = partner_data.get('gender')
            self.import_record_id.gender = partner_data.get('gender')
            phone_number_ids = partner_data.get("phone_number_ids", [])
            region_id = partner_data.get("region")
            zone_id = partner_data.get("zone")
            woreda_id = partner_data.get("woreda")
            keble_id = partner_data.get("kebele")


            if phone_number_ids:
                first_phone_entry = phone_number_ids[0]
                if len(first_phone_entry) > 2 and isinstance(first_phone_entry[2], dict):
                    phone_no = first_phone_entry[2].get("phone_no")
                    self.phone = phone_no
                    self.import_record_id.phone = phone_no


            if region_id and isinstance(region_id, int):
                region = self.env['g2p.region'].browse(region_id)
                if region.exists():
                    self.region = region.name
                    self.import_record_id.region = region.name

            if zone_id:
                zone = self.env['g2p.zone'].browse(woreda_id)
                if zone.exists():
                    self.zone = zone.name

            if woreda_id:
                woreda = self.env['g2p.woreda'].browse(woreda_id)
                if woreda.exists():
                    self.woreda = woreda.name

            if keble_id:
                kebele = self.env['g2p.kebele'].browse(keble_id)
                if kebele.exists():
                    self.kebele = kebele.name


        return result


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


class G2PRegIdInherit(models.Model):
    _inherit = "g2p.reg.id"

    @api.onchange('value')
    def _onchange_value(self):
        national_ids = self.env["g2p.reg.id"].sudo().search([], limit=1)

        for rec in national_ids:
            if self.value != False and self.value == rec.value and self.id_type == rec.id_type:
                raise UserError(_("Farmer With the same id exists in the system"))


