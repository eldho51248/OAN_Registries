# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import logging
import base64

_logger = logging.getLogger(__name__)


class G2PDatashareConfigWebsubATI(models.Model):
    _inherit = "g2p.datashare.config.websub"

    publisher_type = fields.Selection(
        selection=[("internal", "Internal"), ("external", "External")],
        string="Publisher Type",
        required=True,
        default="internal",
        index=True,
        help=(
            "Internal: used for automatic real-time sharing from approved res.partner records. "
            "External: used for partner-specific/consent-driven sharing."
        ),
    )

    def with_delay(
        self,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
    ):
        # Prevent base WebSub hook from creating queue jobs; ATI module controls enqueueing.
        if self.env.context.get("ati_skip_base_websub_publish"):
            _logger.info("ATI WebSub Debug - with_delay bypassed for base hook context")
            return self
        return super().with_delay(
            priority=priority,
            eta=eta,
            max_retries=max_retries,
            description=description,
            channel=channel,
            identity_key=identity_key,
        )

    
    def _get_ati_farmer_data(self, record_data):
        """
        Extract ATI farmer fields from the record data and add them to the payload
        """
        ati_data = {}
        
        # Handle different data structures - check if data is wrapped in groupData
        partner_data = record_data
        if 'groupData' in record_data:
            partner_data = record_data['groupData']
            _logger.debug("ATI WebSub - Data wrapped in groupData, extracting partner data")
        
        # Get the partner record if we have an ID
        partner_id = partner_data.get('id') if partner_data else None
        if partner_id:
            _logger.debug("ATI WebSub - Extracting ATI data for partner ID: %s", partner_id)
            partner = self.env['res.partner'].browse(partner_id)
            if partner.exists():
                # Geographic Fields
                if partner.region:
                    ati_data['region'] = {    
                        'id': partner.region.id,
                        'name': partner.region.name,
                        'code': partner.region.code
                    }
                if partner.zone:
                    ati_data['zone'] = {    
                        'id': partner.zone.id,
                        'name': partner.zone.name,
                        'code': partner.zone.code
                    }
                if partner.woreda:
                    ati_data['woreda'] = {
                        'id': partner.woreda.id,
                        'name': partner.woreda.name,
                        'code': partner.woreda.code
                    }
                if partner.kebele:
                    ati_data['kebele'] = {
                        'id': partner.kebele.id,
                        'name': partner.kebele.name,
                        'code': partner.kebele.code
                    }

                # Name Fields (English)
                if partner.given_name:
                    ati_data['given_name'] = partner.given_name
                if partner.family_name:
                    ati_data['family_name'] = partner.family_name
                if partner.gf_name_eng:
                    ati_data['gf_name_eng'] = partner.gf_name_eng

                # Name Fields (Amharic)
                if partner.first_name_amh:
                    ati_data['first_name_amh'] = partner.first_name_amh
                if partner.family_name_amh:
                    ati_data['family_name_amh'] = partner.family_name_amh
                if partner.gf_name_amh:
                    ati_data['gf_name_amh'] = partner.gf_name_amh

                # Name Fields (Other Languages)
                if partner.first_name_other:
                    ati_data['first_name_other'] = partner.first_name_other
                if partner.family_name_other:
                    ati_data['family_name_other'] = partner.family_name_other
                if partner.gf_name_other:
                    ati_data['gf_name_other'] = partner.gf_name_other

                # Personal Information
                if partner.has_personal_phone:
                    ati_data['has_personal_phone'] = partner.has_personal_phone
                if partner.has_national_id:
                    ati_data['has_national_id'] = partner.has_national_id
                if partner.birthdate_ec:
                    ati_data['birthdate_ec'] = partner.birthdate_ec
                if partner.primary_Language:
                    ati_data['primary_language'] = {
                        'id': partner.primary_Language.id,
                        'name': partner.primary_Language.name,
                        'code': partner.primary_Language.code
                    }
                if partner.is_farmer:
                    ati_data['is_farmer'] = partner.is_farmer
                if partner.farming_type:
                    ati_data['farming_type'] = partner.farming_type

                # Phone Numbers
                if partner.phone_number_ids:
                    ati_data['phone_numbers'] = []
                    for phone in partner.phone_number_ids:
                        phone_data = {
                            'id': phone.id,
                            'phone_no': phone.phone_no,
                            'phone_sanitized': phone.phone_sanitized,
                            'phone_type': phone.phone_type
                        }
                        ati_data['phone_numbers'].append(phone_data)

              
                # Access to Resources
                if partner.crop_water_sources:
                    ati_data['crop_water_sources'] = [
                        {'id': ws.id, 'name': ws.name, 'code': ws.code}
                        for ws in partner.crop_water_sources
                    ]
                if partner.livestock_water_sources:
                    ati_data['livestock_water_sources'] = [
                        {'id': ws.id, 'name': ws.name, 'code': ws.code}
                        for ws in partner.livestock_water_sources
                    ]
                if partner.access_to_machinery:
                    ati_data['access_to_machinery'] = partner.access_to_machinery
                if partner.type_of_machinery:
                    ati_data['type_of_machinery'] = [
                        {'id': m.id, 'name': m.name, 'code': m.code}
                        for m in partner.type_of_machinery
                    ]
                if partner.irrigation_types:
                    ati_data['irrigation_types'] = partner.irrigation_types
                if partner.has_finance_access:
                    ati_data['has_finance_access'] = partner.has_finance_access
                if partner.finance_accesses:
                    ati_data['finance_accesses'] = [
                        {'id': fa.id, 'name': fa.name, 'code': fa.code}
                        for fa in partner.finance_accesses
                    ]
                if partner.other_farmer_in_hh:
                    ati_data['other_farmer_in_hh'] = partner.other_farmer_in_hh

                # Socio-economic Data
                if partner.martial_status:
                    ati_data['martial_status'] = partner.martial_status
                if partner.education:
                    ati_data['education'] = partner.education
                if partner.hh_is_household_head:
                    ati_data['hh_is_household_head'] = partner.hh_is_household_head
                if partner.hh_income_type:
                    ati_data['hh_income_type'] = [
                        {'id': it.id, 'name': it.name, 'code': it.code}
                        for it in partner.hh_income_type
                    ]
                if partner.size_of_family:
                    ati_data['size_of_family'] = partner.size_of_family
                if partner.number_of_children_in_family:
                    ati_data['number_of_children_in_family'] = partner.number_of_children_in_family
                if partner.number_of_males_in_family:
                    ati_data['number_of_males_in_family'] = partner.number_of_males_in_family
                if partner.number_of_females_in_family:
                    ati_data['number_of_females_in_family'] = partner.number_of_females_in_family
                if partner.other_family_member_own_land:
                    ati_data['other_family_member_own_land'] = partner.other_family_member_own_land

                # Land Information
                if partner.land_information_ids:
                    ati_data['land_information'] = []
                    for land in partner.land_information_ids:
                        land_data = {
                            'id': land.id,
                            'total_land_area': land.total_land_area,
                            'land_id': land.land_id,
                            'ownership_type': land.ownership_type,
                            'polygon_data': land.polygon_data if hasattr(land, 'polygon_data') else None,
                            'current_land_use': land.current_land_use if hasattr(land, 'current_land_use') else None,
                            'soil_fertility': land.soil_fertility if hasattr(land, 'soil_fertility') else None,
                            'means_of_acquisition': land.means_of_acquisition if hasattr(land, 'means_of_acquisition') else None,
                            'year_of_acquisition': land.year_of_acquisition.isoformat() if hasattr(land, 'year_of_acquisition') and land.year_of_acquisition else None,
                        }

                        # Add land certificate binary data if available
                        if land.land_certificate:
                            try:
                                if land.land_certificate.data:
                                    land_data['land_certificate'] = base64.b64encode(land.land_certificate.data).decode('utf-8') if isinstance(land.land_certificate.data, bytes) else land.land_certificate.data
                                else:
                                    land_data['land_certificate'] = None
                            except Exception as e:
                                _logger.warning("Could not retrieve binary data for land certificate %s: %s", land.land_certificate.id, str(e))
                                land_data['land_certificate'] = None

                      
                        ati_data['land_information'].append(land_data)

               
                # Computed Fields
                if partner.total_land_area:
                    ati_data['total_land_area'] = partner.total_land_area
                if partner.total_land_rent_area:
                    ati_data['total_land_rent_area'] = partner.total_land_rent_area
                if partner.total_land_owned_area:
                    ati_data['total_land_owned_area'] = partner.total_land_owned_area
                if partner.total_land_crop_sharing_area:
                    ati_data['total_land_crop_sharing_area'] = partner.total_land_crop_sharing_area
                if partner.land_ownership:
                    ati_data['land_ownership'] = partner.land_ownership
                if partner.age_int:
                    ati_data['age_int'] = partner.age_int
                if partner.farmer_id:
                    ati_data['farmer_id'] = partner.farmer_id

                # Add active field to the published data
                if hasattr(partner, 'active'):
                    ati_data['active'] = partner.active

        return ati_data

    def _extract_partner_id_from_payload(self, data):
        if not isinstance(data, dict):
            return None
        partner_data = data.get("groupData", data)
        if not isinstance(partner_data, dict):
            return None
        return partner_data.get("id")

    @api.model
    def publish_event(self, event_type, data: dict, condition_override=None):
        if self.env.context.get("ati_skip_base_websub_publish"):
            _logger.info(
                "ATI WebSub Debug - Skipping base hook publish_event event=%s partner_id=%s",
                event_type,
                self._extract_partner_id_from_payload(data),
            )
            return

        partner_id = self._extract_partner_id_from_payload(data)
        publishers = self.get_publishers(event_type)
        _logger.info(
            "ATI WebSub Debug - Executing publish_event event=%s partner_id=%s publisher_count=%s "
            "data_keys=%s condition_override=%s",
            event_type,
            partner_id,
            len(publishers),
            sorted(data.keys()) if isinstance(data, dict) else None,
            bool(condition_override),
        )
        if not publishers:
            _logger.warning(
                "ATI WebSub Debug - No active WebSub publishers found for event=%s partner_id=%s",
                event_type,
                partner_id,
            )
        result = super().publish_event(event_type, data, condition_override=condition_override)
        _logger.info(
            "ATI WebSub Debug - Finished publish_event event=%s partner_id=%s",
            event_type,
            partner_id,
        )
        return result

    @api.model
    def publish_event_internal(self, event_type, data: dict, condition_override=None):
        partner_id = self._extract_partner_id_from_payload(data)
        publishers = self.search(
            [
                ("event_type", "=", event_type),
                ("active", "=", True),
                ("publisher_type", "=", "internal"),
            ]
        )
        _logger.info(
            "ATI WebSub Debug - Executing publish_event_internal event=%s partner_id=%s publisher_count=%s",
            event_type,
            partner_id,
            len(publishers),
        )
        if not publishers:
            _logger.warning(
                "ATI WebSub Debug - No INTERNAL WebSub publishers found for event=%s partner_id=%s",
                event_type,
                partner_id,
            )
            return
        for publisher in publishers:
            publisher.publish_by_publisher(data, condition_override=condition_override)
        _logger.info(
            "ATI WebSub Debug - Finished publish_event_internal event=%s partner_id=%s",
            event_type,
            partner_id,
        )


    def publish_event_websub(self, data):
        """
        Override the publish_event_websub method to include ATI farmer data
        Only publish records with state = 'approved'
        """
        self.ensure_one()
        _logger.info(
            "ATI WebSub Debug - publish_event_websub start config_id=%s config_name=%s event_type=%s partner_id=%s source=%s",
            self.id,
            self.name,
            self.event_type,
            self._extract_partner_id_from_payload(data),
            data.get("source") if isinstance(data, dict) else None,
        )
        # Consent module can publish through WEBSUB_INDIVIDUAL_UPDATED. Keep that payload as-is.
        if isinstance(data, dict) and data.get("source") == "g2p_ati_consent_mgt":
            _logger.info(
                "ATI WebSub Debug - Consent payload bypassed ATI enrichment for config_id=%s",
                self.id,
            )
            return super().publish_event_websub(data)

        # Get the original data
        original_data = data.copy()
        
        _logger.info(
            "ATI WebSub - Processing data structure. Keys: %s, Has groupData: %s",
            list(original_data.keys()) if isinstance(original_data, dict) else "Not a dict",
            'groupData' in original_data if isinstance(original_data, dict) else False
        )
        
        # Check if partner is in approved state
        partner_data = original_data
        if 'groupData' in original_data:
            partner_data = original_data['groupData']
        
        partner_id = partner_data.get('id') if partner_data else None
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner.exists():
                partner_state = getattr(partner, 'state', None)
                _logger.info(
                    "ATI WebSub - Partner state check: ID=%s, State=%s, Required=approved",
                    partner_id, partner_state
                )
                
                if partner_state != 'approved':
                    _logger.info(
                        "ATI WebSub - SKIPPING PUBLISH: Partner ID %s state is '%s', not 'approved'",
                        partner_id, partner_state
                    )
                    return  # Skip publishing if not approved
                else:
                    _logger.info(
                        "ATI WebSub - PROCEEDING WITH PUBLISH: Partner ID %s is approved",
                        partner_id
                    )
            else:
                _logger.warning("ATI WebSub - Partner ID %s does not exist, skipping publish", partner_id)
                return
        
        # Add ATI farmer data to the payload
        ati_data = self._get_ati_farmer_data(original_data)
        if ati_data:
            # Merge ATI data into the original data
            if 'ati_farmer_data' not in original_data:
                original_data['ati_farmer_data'] = {}
            original_data['ati_farmer_data'].update(ati_data)
            
            _logger.info("ATI WebSub - Added ATI farmer data to WebSub payload: %s", list(ati_data.keys()))
        else:
            _logger.warning("ATI WebSub - No ATI farmer data extracted from payload")
        
        # Call the parent method with enhanced data
        try:
            result = super().publish_event_websub(original_data)
            _logger.info(
                "ATI WebSub Debug - publish_event_websub success config_id=%s event_type=%s partner_id=%s",
                self.id,
                self.event_type,
                self._extract_partner_id_from_payload(original_data),
            )
            return result
        except Exception:
            _logger.exception(
                "ATI WebSub Debug - publish_event_websub failure config_id=%s event_type=%s partner_id=%s",
                self.id,
                self.event_type,
                self._extract_partner_id_from_payload(original_data),
            )
            raise
