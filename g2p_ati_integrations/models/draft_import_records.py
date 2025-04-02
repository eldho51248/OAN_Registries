import logging

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
import ast


class G2PLandInformation(models.Model):
    _inherit = "g2p.land.information"

    polygon_data = fields.Text()
    current_land_use = fields.Text()
    soil_fertility = fields.Text()
    means_of_acquisition = fields.Text()
    year_of_acquisition = fields.Date()

    def fetch_land_records(self):
        try:
            api_parameters = self.env["narlis.integration"].sudo().search([], limit=1)
            land_records = self.env["g2p.land.information"].sudo().search([])

            if not api_parameters:
                raise UserError(_("API configuration is missing. Please configure it in settings."))

            for land in land_records:
                url = f"{api_parameters.host_url}{api_parameters.end_point_url}"
                headers = {
                    "api-key": api_parameters.api_key,
                }
                params = {"version": "v1", "upid": land.land_id, "data-depth": "2"}

                response = requests.get(url, headers=headers, params=params, timeout=10)

                if response.status_code != 200:
                    raise UserError(
                        _("Failed to fetch data from NARLIS API. Status Code: %s, Response: %s")
                        % (response.status_code, response.text)
                    )

                try:
                    land_informations = response.json()
                except ValueError:
                    raise UserError(_("Invalid JSON response from NARLIS API."))

                parcel_data = land_informations.get("parcel", {})
                rights_data = parcel_data.get("rights", [{}])[0]
                party_data = rights_data.get("party", {})

                land.partner_id.is_orphan = party_data.get("isorphan", "").lower()
                land.polygon_data = parcel_data.get("geometryWkt", "")
                land.current_land_use = parcel_data.get("landUse", "")
                land.total_land_area = parcel_data.get("parcelArea", 0)

        except requests.exceptions.Timeout:
            raise UserError(_("The request to the NARLIS API timed out. Please try again later."))
        except requests.exceptions.ConnectionError:
            raise UserError(_("Could not connect to the NARLIS API. Please check your network connection."))
        except requests.exceptions.RequestException as e:
            raise UserError(_("An error occurred while communicating with the NARLIS API: %s") % str(e))

    def action_open_map_view(self):
        if self.polygon_data:
            land_details = []
            polygone_data = ast.literal_eval(self.polygon_data)

            land_info = {
                "total_land_area": self.total_land_area,
                "polygon_data": polygone_data,
                "ownership_type": self.ownership_type,
            }
            land_details.append(land_info)
            # List to store details of all lands

            action = {
                "type": "ir.actions.act_window",
                "name": "Partner Map",
                "res_model": "g2p.land.information",
                "view_mode": "lmap",
                "view_id": self.env.ref("g2p_ati_integrations.action_partner_map_view").id,
                "target": "new",
                "context": {
                    "polygon_coords": land_details,
                    "partner_latitiude": self.partner_id.partner_latitude,
                    "partner_longitude": self.partner_id.partner_longitude,
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
                params = {"version": "v1", "upid": self.land_id, "data-depth": "2"}
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx
                land_informations = response.json()
                isorphan = (
                    land_informations.get("parcel", {})
                    .get("rights", [{}])[0]
                    .get("party", {})
                    .get("isorphan")
                )
                self.partner_id.is_orphan = isorphan.lower()
                self.polygon_data = land_informations["parcel"]["geometryWkt"]
                self.current_land_use = land_informations["parcel"]["landUse"]
                self.total_land_area = land_informations["parcel"]["parcelArea"]

                action = {
                    "type": "ir.actions.act_window",
                    "name": "Partner Map",
                    "res_model": "g2p.land.information",
                    "view_mode": "lmap",
                    "view_id": self.env.ref("g2p_ati_integrations.action_partner_map_view").id,
                    "target": "new",
                    "context": {
                        "polygon_coords": self.polygon_data,
                        "partner_latitiude": self.partner_id.partner_latitude,
                        "partner_longitude": self.partner_id.partner_longitude,
                    },  # Passing polygon data
                }
                return action
            except requests.exceptions.RequestException as e:
                raise UserError(_("Failed to fetch map data: %s") % str(e))


class G2PDraftRecord(models.Model):
    _inherit = "draft.record"

    gf_name_eng = fields.Char(string="Last Name")
    zone = fields.Char()
    woreda = fields.Char()
    kebele = fields.Char()
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


class G2PRespartnerIntegration(models.Model):
    _inherit = "res.partner"

    is_orphan = fields.Selection([("yes", "Yes"), ("no", "No")])
    asigned_region = fields.Many2one("g2p.region")
    language_skills = fields.Many2many("g2p.lang", string="Languages")

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
                    "total_land_area": land.total_land_area,
                    "polygon_data": polygon,
                    "ownership_type": land.ownership_type,
                }

                land_details.append(land_info)
        action = {
            "type": "ir.actions.act_window",
            "name": "Partner Map",
            "res_model": "res.partner",
            "view_mode": "lmap",
            "view_id": self.env.ref("g2p_ati_integrations.action_partner_map_view").id,
            "target": "new",
            "context": {
                "polygon_coords": land_details,
                "partner_latitiude": self.partner_latitude,
                "partner_longitude": self.partner_longitude,
            },  # Passing polygon data
        }
        return action
