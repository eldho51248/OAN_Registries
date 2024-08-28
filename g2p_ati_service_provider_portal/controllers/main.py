import json
from datetime import date
from itertools import zip_longest
import base64

from odoo import http
from odoo.http import request

from odoo.addons.g2p_service_provider_beneficiary_management.controllers.main import G2PServiceProviderBeneficiaryManagement

from odoo.addons.g2p_service_provider_portal_base.controllers.main import ServiceProviderBaseContorller

import logging
_logger = logging.getLogger(__name__)



class AtiServiceProviderContorller(ServiceProviderBaseContorller):
    @http.route(["/serviceprovider/home"], type="http", auth="user", website=True)
    def portal_home(self, **kwargs):
        # domain = []
        # domain.append(("is_group", "=", True))
        households = request.env["res.partner"].sudo().search([("is_group", "=", True)])
        individuals = request.env["res.partner"].sudo().search([("is_group", "=", False),
                                                                ("is_farmer", "=", "yes")])


        return request.render(
            "g2p_ati_service_provider_portal.ati_dashboard_template",
        {"households": households,
         "individuals": individuals
         }
        )
    
    @http.route(["/serviceprovider/update/suggests"], type="http", auth="user", website=True)
    def portal_update_suggests(self, **kwargs):
        user_id = request.env.user.id
        updte_suggests = request.env["request"].sudo().search([("create_uid", "=", user_id)],  order="create_date desc")
       
       
        return request.render(
            "g2p_ati_service_provider_portal.ati_update_suggests_template",
            {"updte_suggests": updte_suggests,
            }
        )


    @http.route(["/get_notifications"], type="http", auth="user", website=True)
    def get_notifications(self, **kwargs):
        user_id = request.env.user.id
        notifications = request.env["request"].sudo().search([('seen', '=', False), ("create_uid", "=", user_id)])

        notifications_data = []
        for notif in notifications:
            
            suggester_name = notif.requester_id.name if notif.requester_id else "Unknown"
            notifications_data.append({
                'id': notif.id, 
                'message': f"{suggester_name} has suggested an update",
                'url': '/serviceprovider/update/suggests'
            })

       
        return json.dumps(notifications_data)



    @http.route(["/get_notification_count"], type="http", auth="user", website=True, csrf=False)
    def get_notification_count(self, **kwargs):
        print("")
        user_id = request.env.user.id
        notification_count = request.env["request"].sudo().search_count([('seen', '=', False), ('status', '=', 'newSuggestion'),("create_uid", "=", user_id)])
        return json.dumps([{"count": notification_count}])



    @http.route("/mark_notification_seen", type="json", auth="user", csrf=False)
    def mark_notification_seen(self):
        json_data = request.httprequest.get_json()
        notification_id = json_data.get('notification_id')
    
        print(f"Received notification_id: {notification_id} of type {type(notification_id)}")
    
                
        if not notification_id:
            
            return {"status": "error", "message": "Notification ID is missing"}

        try:
           
            notification = request.env['request'].sudo().browse(int(notification_id))
           
          
        except ValueError:
            return {"status": "error", "message": "Invalid Notification ID"}

        if notification and not notification.seen:
            notification.seen = True
            return {"status": "success"}

        return {"status": "error", "message": "Notification not found or already seen"}


    @http.route(["/set_all_notifications_seen"], type="http", auth="user", website=True, csrf=False)
    def set_all_notifications_seen(self, **kwargs):
        user_id = request.env.user.id
        notifications = request.env['request'].sudo().search([('seen', '=', False), ('create_uid', '=', user_id)])
        
        for notif in notifications:
            notif.seen = True
        
        return json.dumps({"status": "success"})

    @http.route(["/view_all_notifications"], type="http", auth="user", website=True)
    def view_all_notifications(self, **kwargs):
        user_id = request.env.user.id
        notifications = request.env['request'].sudo().search([('seen', '=', False), ('create_uid', '=', user_id)])
        
        for notif in notifications:
            notif.seen = True
        
        return json.dumps({"status": "success"})


    
    
class AtiserviceProviderBeneficiaryManagement(G2PServiceProviderBeneficiaryManagement):

    @http.route(
        ["/get_selection_name"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def get_selection(self, selectedValue=None, **kwargs):
        name = request.env["ir.model.fields.selection"].sudo().search([("id", "=", selectedValue)]).name
        return json.dumps([{"name": name}])

    @http.route(
        ["/update_zone_options"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_zone_options(self, region_id=None, **kwargs):
        zones = request.env["g2p.zone"].sudo().search([("region", "=", int(region_id))])
        zone_options = [{"id": zone.id, "name": zone.name} for zone in zones]
        return json.dumps(zone_options)

    @http.route(
        ["/update_woreda_options"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_woreda_options(self, zone_id=None, **kwargs):
        woredas = request.env["g2p.woreda"].sudo().search([("zone", "=", int(zone_id))])
        woredas_options = [{"id": woreda.id, "name": woreda.name} for woreda in woredas]
        return json.dumps(woredas_options)
    
    @http.route(
        ["/update_kebele_options"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_kebele_options(self, woreda_id=None, **kwargs):
        kebeles = request.env["g2p.kebele"].sudo().search([("woreda", "=", int(woreda_id))])
        kebeles_options = [{"id": kebele.id, "name": kebele.name} for kebele in kebeles]
        return json.dumps(kebeles_options)
   
    @http.route(
        ["/serviceprovider/group/create/"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def group_create(self, **kw):
        gender = request.env["gender.type"].sudo().search([])
        region = request.env["g2p.region"].sudo().search([])
        zone = request.env["g2p.zone"].sudo().search([])
        woreda = request.env["g2p.woreda"].sudo().search([])
        kebele = request.env["g2p.kebele"].sudo().search([])
        primary_language = request.env["g2p.lang"].sudo().search([])
        primary_cooperatives = request.env["g2p.primary.cooperative"].sudo().search([])
        cooperative_unions = request.env["g2p.cooperative.union"].sudo().search([])
        primary_commodities = request.env["g2p.primary.commodity"].sudo().search([])
        crops = request.env["g2p.crop"].sudo().search([])
        crop_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'crop')])
        crop_water_source = request.env["g2p.water.source"].sudo().search([])
        livestock_types = request.env["g2p.livestock.type"].sudo().search([])
        livestock_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'animal')])
        water_source = request.env["g2p.water.source"].sudo().search([])
        machinary_types = request.env["g2p.machinery"].sudo().search([])
        financial_access = request.env["g2p.finance.access"].sudo().search([])
        source_of_income = request.env["g2p.hh.income"].sudo().search([])
        relationship_with_hhh = request.env["g2p.group.membership.kind"].sudo().search([])

        model_id = request.env["ir.model"].sudo().search([("model", "=", "res.partner")])
        land_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.land.information")])
        crop_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.crop.information")])
        livestock_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.livestock.information")])

        ownership_type_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", land_model_id.id), ("name", "=", "ownership_type")])
            .selection_ids
        )

        crop_is_diseased_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", crop_model_id.id), ("name", "=", "is_diseased")])
            .selection_ids
        )

        livestock_is_diseased_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", livestock_model_id.id), ("name", "=", "is_diseased")])
            .selection_ids
        )

        serialized_crop_info_data = []
        serialized_livestock_info_data = []

        has_national_id = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "has_national_id")])
            .selection_ids
        )

        is_member_of_primary_cooperative = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
            .selection_ids
        )

        is_member_of_cooperative_union = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
            .selection_ids
        )

        is_member_in_farmer_cluster = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_in_farmer_cluster")])
            .selection_ids
        )

        role_in_cluster = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "role_in_farmer_cluster")])
            .selection_ids
        )

        access_to_machinery = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "access_to_machinery")])
            .selection_ids
        )

        has_finance_access = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "has_finance_access")])
            .selection_ids

        )

        marital_status = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "martial_status")])
            .selection_ids
        )

        education_level = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "education")])
            .selection_ids
        )

        farming_type = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "farming_type")])
            .selection_ids
        )

        disability_status = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_disabled")])
            .selection_ids
        )

        has_personal_phone = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "has_personal_phone")])
            .selection_ids
        )
        hh_is_household_head = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "hh_is_household_head")])
            .selection_ids
        )

        do_you_use_fertilizer = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_fertilizer")])
            .selection_ids
        )
        print(do_you_use_fertilizer)
        do_you_use_insecticide= (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_insecticide")])
            .selection_ids
        )

        do_you_use_pesticide = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_pesticide")])
            .selection_ids
        )

        do_you_use_improved_seed = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_improved_seed")])
            .selection_ids
        )

        return request.render(
            "g2p_ati_service_provider_portal.ati_create_group_form_template",
            {
                "has_national_id": has_national_id,
                "gender": gender,
                "region": region,
                "zone": zone,
                "woreda": woreda,
                "kebele": kebele,
                "hh_is_household_head": hh_is_household_head,
                "primary_language": primary_language,
                "has_personal_phone": has_personal_phone,
                "farming_type": farming_type,
                "source_of_income": source_of_income,
                "is_member_of_primary_cooperative": is_member_of_primary_cooperative,
                "is_member_of_cooperative_union": is_member_of_cooperative_union,
                "is_member_in_farmer_cluster": is_member_in_farmer_cluster,
                "primary_cooperatives": primary_cooperatives,
                "cooperative_unions": cooperative_unions,
                "primary_commodities": primary_commodities,
                "role_in_cluster": role_in_cluster,
                "serialized_crop_info_data": serialized_crop_info_data,
                "serialized_livestock_info_data": serialized_livestock_info_data,
                "crops": crops,
                "crop_illness_type": crop_illness_type,
                "crop_water_source": crop_water_source,
                "livestock_types": livestock_types,
                "livestock_illness_type": livestock_illness_type,
                "water_source": water_source,
                "do_you_use_fertilizer": do_you_use_fertilizer,
                "do_you_use_pesticide": do_you_use_pesticide,
                "do_you_use_insecticide": do_you_use_insecticide,
                "do_you_use_improved_seed": do_you_use_improved_seed,
                "access_to_machinery": access_to_machinery,
                "machinary_types": machinary_types,
                "marital_status": marital_status,
                "education_level": education_level,
                "disability_status": disability_status,
                "has_finance_access": has_finance_access,
                "financial_access": financial_access,
                "ownership_type_selections": ownership_type_selections,
                "crop_is_diseased_selections": crop_is_diseased_selections,
                "livestock_is_diseased_selections": livestock_is_diseased_selections,
                "relationship_with_hhh": relationship_with_hhh
            },
        )

    @http.route(
        ["/serviceprovider/group/create/submit"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def group_create_submit(self, **kw):

        try:
            beneficiary_id = int(kw.get("group_id"))

            beneficiary = request.env["res.partner"].sudo().browse(beneficiary_id)

            individuals_data = request.params.get('individuals', [])
            print(individuals_data)


            if not beneficiary:
                return request.render(
                    "g2p_service_provider_beneficiary_management.error_template",
                    {"error_message": "Beneficiary not found."},
                )

            for key, value in kw.items():
                if key in beneficiary:
                    beneficiary.write({key: value})
                else:
                    print(f"Ignoring invalid key: {key}")

            return request.redirect("/serviceprovider/group")

        except Exception as e:
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": "An error occurred. Please try again later."},
            )
        
    @http.route(
        ["/serviceprovider/group/update/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def group_update(self, _id, **kw):
        try:

            group = request.env["res.partner"].sudo().browse(_id)

            if not group:
                return request.render(
                    "g2p_service_provider_beneficiary_management.error_template",
                    {"error_message": "Household not found."},
                )
            
            gender = request.env["gender.type"].sudo().search([])
            region = request.env["g2p.region"].sudo().search([])
            zone = request.env["g2p.zone"].sudo().search([])
            woreda = request.env["g2p.woreda"].sudo().search([])
            kebele = request.env["g2p.kebele"].sudo().search([])
            primary_language = request.env["g2p.lang"].sudo().search([])
            primary_cooperatives = request.env["g2p.primary.cooperative"].sudo().search([])
            cooperative_unions = request.env["g2p.cooperative.union"].sudo().search([])
            primary_commodities = request.env["g2p.primary.commodity"].sudo().search([])
            crops = request.env["g2p.crop"].sudo().search([])
            crop_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'crop')])
            crop_water_source = request.env["g2p.water.source"].sudo().search([])
            livestock_types = request.env["g2p.livestock.type"].sudo().search([])
            livestock_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'animal')])
            water_source = request.env["g2p.water.source"].sudo().search([])
            machinary_types = request.env["g2p.machinery"].sudo().search([])
            financial_access = request.env["g2p.finance.access"].sudo().search([])
            source_of_income = request.env["g2p.hh.income"].sudo().search([])
            relationship_with_hhh = request.env["g2p.group.membership.kind"].sudo().search([])

            model_id = request.env["ir.model"].sudo().search([("model", "=", "res.partner")])
            land_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.land.information")])
            crop_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.crop.information")])
            livestock_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.livestock.information")])

            ownership_type_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", land_model_id.id), ("name", "=", "ownership_type")])
                .selection_ids
            )

            crop_is_diseased_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", crop_model_id.id), ("name", "=", "is_diseased")])
                .selection_ids
            )

            livestock_is_diseased_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", livestock_model_id.id), ("name", "=", "is_diseased")])
                .selection_ids
            )

            serialized_crop_info_data = []
            serialized_livestock_info_data = []

            has_national_id = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_national_id")])
                .selection_ids
            )

            is_member_of_primary_cooperative = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
                .selection_ids
            )

            is_member_of_cooperative_union = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
                .selection_ids
            )

            is_member_in_farmer_cluster = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_in_farmer_cluster")])
                .selection_ids
            )

            role_in_cluster = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "role_in_farmer_cluster")])
                .selection_ids
            )

            access_to_machinery = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "access_to_machinery")])
                .selection_ids
            )

            has_finance_access = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_finance_access")])
                .selection_ids

            )

            marital_status = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "martial_status")])
                .selection_ids
            )

            education_level = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "education")])
                .selection_ids
            )

            farming_type = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "farming_type")])
                .selection_ids
            )

            disability_status = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_disabled")])
                .selection_ids
            )

            has_personal_phone = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_personal_phone")])
                .selection_ids
            )

            do_you_use_fertilizer = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_fertilizer")])
            .selection_ids
        )
          
            do_you_use_insecticide= (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_insecticide")])
                .selection_ids
            )

            do_you_use_pesticide = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_pesticide")])
                .selection_ids
            )  

            do_you_use_improved_seed = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_improved_seed")])
                .selection_ids
            )

           
            members = group.group_membership_ids
            farmer_member_ids = []
            member_ids = []
            for ind in members.individual:
                if ind.is_farmer == 'yes':
                    farmer_member_ids.append(ind)
                else:
                    member_ids.append(ind)
            
            # for field_name, field_obj in members._fields.items():
            #     field_value = getattr(members, field_name, None)
            #     print(f"Field: {field_name}, Value: {field_value}, Type: {field_obj.type}")

            return request.render(
                "g2p_ati_service_provider_portal.ati_update_group_form_template",
                {
                    "relationship_with_hhh": relationship_with_hhh,
                    "group": group,
                    "farmer_member_ids": farmer_member_ids,
                    "member_ids": member_ids,
                    "has_national_id": has_national_id,
                    "gender": gender,
                    "region": region,
                    "zone": zone,
                    "woreda": woreda,
                    "kebele": kebele,
                    "primary_language": primary_language,
                    "has_personal_phone": has_personal_phone,
                    "farming_type": farming_type,
                    "is_member_of_primary_cooperative": is_member_of_primary_cooperative,
                    "is_member_of_cooperative_union": is_member_of_cooperative_union,
                    "is_member_in_farmer_cluster": is_member_in_farmer_cluster,
                    "primary_cooperatives": primary_cooperatives,
                    "cooperative_unions": cooperative_unions,
                    "primary_commodities": primary_commodities,
                    "role_in_cluster": role_in_cluster,
                    "serialized_crop_info_data": serialized_crop_info_data,
                    "serialized_livestock_info_data": serialized_livestock_info_data,
                    "crops": crops,
                    "crop_illness_type": crop_illness_type,
                    "crop_water_source": crop_water_source,
                    "livestock_types": livestock_types,
                    "livestock_illness_type": livestock_illness_type,
                    "water_source": water_source,
                    "do_you_use_fertilizer": do_you_use_fertilizer,
                    "do_you_use_pesticide": do_you_use_pesticide,
                    "do_you_use_insecticide": do_you_use_insecticide,
                    "do_you_use_improved_seed": do_you_use_improved_seed,

                    "access_to_machinery": access_to_machinery,
                    "machinary_types": machinary_types,
                    "marital_status": marital_status,
                    "education_level": education_level,
                    "disability_status": disability_status,
                    "has_finance_access": has_finance_access,
                    "financial_access": financial_access,
                    "source_of_income": source_of_income,
                    "ownership_type_selections": ownership_type_selections,
                    "crop_is_diseased_selections": crop_is_diseased_selections,
                    "livestock_is_diseased_selections": livestock_is_diseased_selections,
                },
            )
        except Exception as e:
            print(e)
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": e},
            )

    @http.route(
        ["/serviceprovider/group/update/submit"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def group_update_submit(self, **kw):

        try:
            group_id = int(kw.get("group_id"))

            group = request.env["res.partner"].sudo().browse(group_id)

            if not group:
                return request.render(
                    "g2p_service_provider_beneficiary_management.error_template",
                    {"error_message": "Household not found."},
                )

            for key, value in kw.items():
                if key in group:
                    group.write({key: value})
                else:
                    print(f"Ignoring invalid key: {key}")

            return request.redirect("/serviceprovider/group")

        except Exception as e:
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": "An error occurred. Please try again later."},
            )

    @http.route(
        ["/serviceprovider/individual/registrar/create/"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def individual_registrar_create(self, **kw):
        gender = request.env["gender.type"].sudo().search([])
        region = request.env["g2p.region"].sudo().search([])
        zone = request.env["g2p.zone"].sudo().search([])
        woreda = request.env["g2p.woreda"].sudo().search([])
        kebele = request.env["g2p.kebele"].sudo().search([])
        primary_language = request.env["g2p.lang"].sudo().search([])
        primary_cooperatives = request.env["g2p.primary.cooperative"].sudo().search([])
        cooperative_unions = request.env["g2p.cooperative.union"].sudo().search([])
        primary_commodities = request.env["g2p.primary.commodity"].sudo().search([])
        crops = request.env["g2p.crop"].sudo().search([])
        crop_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'crop')])
        crop_water_source = request.env["g2p.water.source"].sudo().search([])
        livestock_types = request.env["g2p.livestock.type"].sudo().search([])
        livestock_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'animal')])
        water_source = request.env["g2p.water.source"].sudo().search([])
        machinary_types = request.env["g2p.machinery"].sudo().search([])
        financial_access = request.env["g2p.finance.access"].sudo().search([])
        source_of_income = request.env["g2p.hh.income"].sudo().search([])


        model_id = request.env["ir.model"].sudo().search([("model", "=", "res.partner")])
        land_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.land.information")])
        crop_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.crop.information")])
        livestock_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.livestock.information")])

        ownership_type_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id","=",land_model_id.id), ("name","=","ownership_type")])
            .selection_ids
        )

        crop_is_diseased_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id","=",crop_model_id.id), ("name","=","is_diseased")])
            .selection_ids
        )

        livestock_is_diseased_selections = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id","=",livestock_model_id.id), ("name","=","is_diseased")])
            .selection_ids
        )
        
        serialized_crop_info_data = []
        serialized_livestock_info_data = []
        
        has_national_id = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_national_id")])
                .selection_ids
            )

        is_member_of_primary_cooperative = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
            .selection_ids
        )

        is_member_of_cooperative_union = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
            .selection_ids
        )
        
        is_member_in_farmer_cluster = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_member_in_farmer_cluster")])
            .selection_ids
        )

        role_in_cluster = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "role_in_farmer_cluster")])
            .selection_ids
        )

        do_you_use_fertilizer = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_fertilizer")])
            .selection_ids
        )
          
        do_you_use_insecticide= (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_insecticide")])
            .selection_ids
        )

        do_you_use_pesticide = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_pesticide")])
            .selection_ids
        ) 
        do_you_use_improved_seed = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_improved_seed")])
            .selection_ids
        )

        access_to_machinery = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "access_to_machinery")])
            .selection_ids
        )

        has_finance_access =(
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "has_finance_access")])
            .selection_ids

        )
    
        marital_status = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "martial_status")])
            .selection_ids
        )
    
        education_level = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "education")])
            .selection_ids
        )

        farming_type = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "farming_type")])
            .selection_ids
        )

        disability_status = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "is_disabled")])
            .selection_ids
        )

        has_personal_phone = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "has_personal_phone")])
            .selection_ids
        )

        hh_is_household_head = (
            request.env["ir.model.fields"]
            .sudo()
            .search([("model_id", "=", model_id.id), ("name", "=", "hh_is_household_head")])
            .selection_ids
        )
       

        return request.render(
            "g2p_ati_service_provider_portal.ati_individual_registrant_form_template",
            {
                "has_national_id": has_national_id,
                "gender": gender,
                "region": region,
                "zone": [],
                "woreda": [],
                "kebele": [],
                "primary_language": primary_language,
                "has_personal_phone": has_personal_phone,
                "hh_is_household_head": hh_is_household_head,
                "farming_type": farming_type,
                "is_member_of_primary_cooperative": is_member_of_primary_cooperative,
                "is_member_of_cooperative_union": is_member_of_cooperative_union,
                "is_member_in_farmer_cluster": is_member_in_farmer_cluster,
                "primary_cooperatives": primary_cooperatives,
                "cooperative_unions": cooperative_unions,
                "primary_commodities": primary_commodities,
                "role_in_cluster": role_in_cluster,
                "serialized_crop_info_data": serialized_crop_info_data,
                "serialized_livestock_info_data": serialized_livestock_info_data,
                "crops": crops,
                "crop_illness_type": crop_illness_type,
                "crop_water_source": crop_water_source,
                "livestock_types": livestock_types,
                "livestock_illness_type": livestock_illness_type,
                "water_source": water_source,
                "do_you_use_fertilizer": do_you_use_fertilizer,
                "do_you_use_pesticide": do_you_use_pesticide,
                "do_you_use_insecticide": do_you_use_insecticide,
                "do_you_use_improved_seed": do_you_use_improved_seed,

                "access_to_machinery": access_to_machinery,
                "machinary_types": machinary_types,
                "marital_status": marital_status,
                "education_level": education_level,
                "disability_status": disability_status,
                "has_finance_access": has_finance_access,
                "financial_access": financial_access,
                "source_of_income": source_of_income,
                "ownership_type_selections": ownership_type_selections,
                "crop_is_diseased_selections": crop_is_diseased_selections,
                "livestock_is_diseased_selections": livestock_is_diseased_selections
            },
        )


    @http.route(
        ["/serviceprovider/individual/beneficiary/create/submit"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def individual_create_submit(self, **kw):
        try:
            vals = {
                "is_registrant": True,
                "is_group": False,
            }
            name = ""
                     
            land_info_data = []
            crop_info_data = []
            livestock_info_data = []

            valid_keys = [key for key in kw.keys() if "{9999}" not in key]
            land_indices = set()
            crop_indices = set()
            livestock_indices = set()

            for key in valid_keys:
                if key.startswith('land_ownership_type_'):
                    try:
                        land_index = int(key.split('_')[-1])
                        land_indices.add(land_index)
                    except ValueError:
                        continue
                if key.startswith('crops_'):
                    try:
                        crop_index = int(key.split('_')[-1])
                        crop_indices.add(crop_index)
                    except ValueError:
                        continue
                if key.startswith('livestock_types_'):
                    try:
                        livestock_index = int(key.split('_')[-1])
                        livestock_indices.add(livestock_index)
                    except ValueError:
                        continue

            # NATIONAL ID
            reg_ids = []                
            has_national_id = None
            if kw.get("has_national_id"):
                has_national_id = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("has_national_id"))])
                        .value
                    )
                vals["has_national_id"] = has_national_id
            if has_national_id == "yes":
                id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "UID")], limit=1)
                vals["reg_ids"] = [
                    (0, 0, {"id_type": id_type.id, "value": kw.get("uid")}),
                ]
            elif has_national_id == "no" and kw.get("rid") and kw.get("rid").strip():
                id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "RID")], limit=1)
                vals["reg_ids"] = [
                    (0, 0, {"id_type": id_type.id, "value": kw.get("rid")}),
                ]

            # INDIVIDUAL DETAILS
            if kw.get("hh_is_household_head"):
                hh_is_household_head = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("hh_is_household_head"))])
                        .value
                    )
                vals["hh_is_household_head"] = hh_is_household_head
            if kw.get("primary_language"):
                vals["primary_Language"] = int(kw.get("primary_language"))
            if kw.get("given_name"):
                vals["given_name"] = kw.get("given_name")
                name += kw.get("given_name") + " "
            if kw.get("family_name"):
                vals["family_name"] = kw.get("family_name")
                name += kw.get("family_name") + " "
            if kw.get("gf_name_eng"):
                vals["gf_name_eng"] = kw.get("gf_name_eng")
                name += kw.get("gf_name_eng")
            if name:
                vals["name"] = name
            if kw.get("first_name_amh").strip():
                vals["first_name_amh"] = kw.get("first_name_amh")
            if kw.get("family_name_amh").strip():
                vals["family_name_amh"] = kw.get("family_name_amh")
            if kw.get("gf_name_amh").strip():
                vals["gf_name_amh"] = kw.get("gf_name_amh")
            if kw.get("first_name_other") and kw.get("first_name_other").strip():
                vals["first_name_other"] = kw.get("first_name_other")
            if kw.get("family_name_other") and kw.get("family_name_other").strip():
                vals["family_name_other"] = kw.get("family_name_other")
            if kw.get("gf_name_other") and kw.get("gf_name_other").strip():
                vals["gf_name_other"] = kw.get("gf_name_other")
            if kw.get("region"):
                vals["region"] = int(kw.get("region"))
            if kw.get("zone"):
                vals["zone"] = int(kw.get("zone"))
            if kw.get("woreda"):
                vals["woreda"] = int(kw.get("woreda"))
            if kw.get("kebele"):
                vals["kebele"] = int(kw.get("kebele"))
            if kw.get("birthdate"):
                vals["birthdate"] = kw.get("birthdate")
            if kw.get("gender"):
                vals["gender"] = kw.get("gender")
                
            has_personal_phone = None
            if kw.get("has_personal_phone"):
                has_personal_phone = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("has_personal_phone"))])
                        .value
                    )
                vals["has_personal_phone"] = has_personal_phone
            ethiopia_country_id = request.env['res.country'].sudo().search([('name', '=', 'Ethiopia')], limit=1).id
            phone_no = []
            if has_personal_phone == "yes":
                phone_no.append((0, 0, {"phone_no": kw.get("primary_phone"), "phone_type": "primary", "country": ethiopia_country_id}))
                if kw.get("secondary_phone") and kw.get("secondary_phone").strip():
                    phone_no.append((0, 0, {"phone_no": kw.get("secondary_phone"), "phone_type": "secondary", "country": ethiopia_country_id}))
            elif has_personal_phone == "no":
                phone_no.append((0, 0, {"phone_no": kw.get("other_phone"), "phone_type": "other", "country": ethiopia_country_id}))
                if kw.get("secondary_phone") and kw.get("secondary_phone").strip():
                    phone_no.append((0, 0, {"phone_no": kw.get("secondary_phone"), "phone_type": "secondary", "country": ethiopia_country_id}))
            vals["phone_number_ids"] = phone_no

            if kw.get("email") and kw.get("email").strip():
                vals["email"] = kw.get("email")
            if kw.get("is_disabled"):
                vals["is_disabled"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("is_disabled"))])
                    .value
                )
            if kw.get("farming_type"):
                vals["farming_type"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("farming_type"))])
                    .value
                )

            # SOCIO ECONOMIC DATA
            if kw.get("marital_status"):
                vals["martial_status"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("marital_status"))])
                    .value
                )
            if kw.get("education_level"):
                vals["education"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("education_level"))])
                    .value
                )
            income_source = request.httprequest.form.getlist("hh_income_type")
            if income_source:
                income_source_ids = [int(id) for id in income_source]
                vals["hh_income_type"] = [(6, 0, income_source_ids)]

            # MEMBERSHIP DETAILS
            is_member_of_primary_cooperative = False
            is_member_of_cooperative_union = False
            is_member_in_farmer_cluster = False
            if kw.get("is_member_of_primary_coop") and kw.get("is_member_of_primary_coop").strip():
                is_member_of_primary_cooperative = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("is_member_of_primary_coop"))])
                    .value
                )
                vals["is_member_of_primary_cooperative"] = is_member_of_primary_cooperative
            if is_member_of_primary_cooperative == "yes":
                if kw.get("name_of_primary_coop") and kw.get("name_of_primary_coop").strip():
                    vals["primary_cooperatives"] = int(kw.get("name_of_primary_coop"))
            if kw.get("is_member_of_coop_union") and kw.get("is_member_of_coop_union").strip():
                is_member_of_cooperative_union = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("is_member_of_coop_union"))])
                    .value
                )
                vals["is_member_of_cooperative_union"] = is_member_of_cooperative_union
            if is_member_of_cooperative_union == "yes":
                if kw.get("name_of_coop_union") and kw.get("name_of_coop_union").strip():
                    vals["cooperative_unions"] = int(kw.get("name_of_coop_union"))
            if kw.get("in_farmer_cluster") and kw.get("in_farmer_cluster").strip():
                is_member_in_farmer_cluster = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("in_farmer_cluster"))])
                    .value
                )
                vals["is_member_in_farmer_cluster"] = is_member_in_farmer_cluster
            if is_member_in_farmer_cluster == "yes":
                if kw.get("primary_commodity") and kw.get("primary_commodity").strip():
                    vals["primary_commodity"] = int(kw.get("primary_commodity"))
                if kw.get("role_in_cluster") and kw.get("role_in_cluster").strip():
                    vals["role_in_farmer_cluster"] = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("role_in_cluster"))])
                        .value
                    )

            # LAND INFORMATION
            supporting_documents_ids = []
            backend_id = (
                request.env.ref("storage_backend.default_storage_backend").id
                or request.env["storage.backend"].sudo().search([], limit=1).id
            )
            
            doc_tag = request.env["g2p.document.tag"].sudo().get_tag_by_name("Land Certificate")
            if not doc_tag:
                doc_tag = request.env["g2p.document.tag"].sudo().create({"name": "Land Certificate"})
            for index in land_indices:
                ownership_type = kw.get(f'land_ownership_type_{index}').strip()
                if not ownership_type:
                    continue
                land_id = kw.get(f'land_id_{index}')
                land_area = kw.get(f'total_land_area_{index}')
                land_ownership_type = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", ownership_type)])
                    .value
                )
                if kw.get(f'land_certificate_{index}') and (f'land_certificate_{index}').strip():
                    land_certificate = kw.get(f'land_certificate_{index}')
                    binary_content = base64.b64encode(land_certificate.read()).decode('utf-8')
                    supporting_documents_ids.append(
                        (
                            0,
                            0,  
                            {
                                "backend_id": backend_id,
                                "name": land_certificate.filename,
                                "data": binary_content,
                                "tags_ids": [(4, doc_tag.id)]
                            },
                        )
                    )
                land_info_data.append((0, 0, {
                    'ownership_type': land_ownership_type,
                    'total_land_area': land_area,
                    'land_id': land_id,
                }))
            vals["land_information_ids"] = land_info_data

            # CROP INFORMATION
            crop_ws = request.httprequest.form.getlist("crop_water_source")
            if crop_ws:
                crop_water_sources_ids = [int(id) for id in crop_ws]
                vals["crop_water_sources"] = [(6, 0, crop_water_sources_ids)]

            for index in crop_indices:
                crop_id = kw.get(f'crops_{index}').strip()
                crop_planted_id = kw.get(f'planted_date_{index}').strip()
                if not crop_id:
                    continue

                crop_info_data.append((0, 0, {
                    'crop': int(crop_id),
                    'collected_gc':crop_planted_id
                }))
            vals["crop_information_ids"] = crop_info_data

            # LIVESTOCK INFORMATION
            livestock_ws = request.httprequest.form.getlist("livestock_water_source")
            if livestock_ws:
                livestock_water_sources_ids = [int(id) for id in livestock_ws]
                vals["livestock_water_sources"] = [(6, 0, livestock_water_sources_ids)]

            for index in livestock_indices:
                livestock_type = kw.get(f'livestock_types_{index}').strip()
                if not livestock_type:
                    continue
                number_of_livestock = kw.get(f'number_of_livestock_{index}')
             
                livestock_info_data.append((0, 0, {
                    'livestock_type': int(livestock_type),
                    'number_of_livestock': number_of_livestock,
                }))
            vals["livestock_information_ids"] = livestock_info_data
            
            # AGRICULTURAL INPUT
            # if kw.get("amount_fertilizer_utilized"):
            #     amount_fertilizer_utilized = float(kw.get("amount_fertilizer_utilized"))
            # if kw.get("amount_insecticide_utilized"):
            #     amount_insecticide_utilized = float(kw.get("amount_insecticide_utilized"))
            # if kw.get("amount_pesticide_utilized"):
            #     amount_pesticide_utilized = float(kw.get("amount_pesticide_utilized"))
            # if kw.get("amount_improved_seed_utilized"):
            #     amount_improved_seed_utilized = float(kw.get("amount_improved_seed_utilized"))
            
            # ACCESS TO RESOURCE
            access_to_machinery = None
            if kw.get("access_to_machinery") and kw.get("access_to_machinery").strip():
                access_to_machinery = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("access_to_machinery"))])
                    .value
                )
                vals["access_to_machinery"] = access_to_machinery
            if access_to_machinery == 'yes':
                machinery_types = request.httprequest.form.getlist("machinery_types")
                if machinery_types:
                    machinery_types_ids = [int(id) for id in machinery_types]
                    vals["type_of_machinery"] = [(6, 0, machinery_types_ids)]
            
            # FINANCIAL SERVICE
            has_finance_access = None
            if kw.get("has_finance_access") and kw.get("has_finance_access") != " ":
                has_finance_access = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("has_finance_access"))])
                    .value
                )
                vals["has_finance_access"] = has_finance_access
            if has_finance_access == 'yes':
                access_to_finance = request.httprequest.form.getlist("finance_accesses")
                if access_to_finance:
                    access_to_finance_ids = [int(id) for id in access_to_finance]
                    vals["finance_accesses"] = [(6, 0, access_to_finance_ids)]

            # Other
            vals["is_farmer"] = "yes"

            print(vals)
            request.env["res.partner"].sudo().create(vals)
            return request.redirect("/serviceprovider/individual")
        
        except Exception as e:
            print(e)
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": f"Error while creating individual, {e}"},
            )

    @http.route(
        ["/serviceprovider/individual/update/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def indvidual_update(self, _id, **kw):
        try:
            beneficiary = request.env["res.partner"].sudo().browse(_id)

            if not beneficiary:
                return request.render(
                    "g2p_service_provider_beneficiary_management.error_template",
                    {"error_message": "Beneficiary not found."},
                )

            gender = request.env["gender.type"].sudo().search([])
            region = request.env["g2p.region"].sudo().search([])
            zone = request.env["g2p.zone"].sudo().search([("region", "=", beneficiary.region.id)])
            woreda = request.env["g2p.woreda"].sudo().search([("zone", "=", beneficiary.zone.id)])
            kebele = request.env["g2p.kebele"].sudo().search([("woreda", "=", beneficiary.woreda.id)])
            primary_language = request.env["g2p.lang"].sudo().search([])
            primary_cooperatives = request.env["g2p.primary.cooperative"].sudo().search([])
            cooperative_unions = request.env["g2p.cooperative.union"].sudo().search([])
            primary_commodities = request.env["g2p.primary.commodity"].sudo().search([])
            crops = request.env["g2p.crop"].sudo().search([])
            crop_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'crop')])
            crop_water_source = request.env["g2p.water.source"].sudo().search([])
            livestock_types = request.env["g2p.livestock.type"].sudo().search([])
            livestock_illness_type = request.env["g2p.illness.type"].sudo().search([('illness_type', '=', 'animal')])
            water_source = request.env["g2p.water.source"].sudo().search([])
            machinary_types = request.env["g2p.machinery"].sudo().search([])
            financial_access = request.env["g2p.finance.access"].sudo().search([])
            source_of_income = request.env["g2p.hh.income"].sudo().search([])

            model_id = request.env["ir.model"].sudo().search([("model", "=", "res.partner")])
            land_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.land.information")])
            crop_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.crop.information")])
            livestock_model_id = request.env["ir.model"].sudo().search([("model", "=", "g2p.livestock.information")])

            hh_is_household_head = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "hh_is_household_head")])
                .selection_ids
            )

            household_head_selection_id = False
            for choice in hh_is_household_head:
                if choice.value == beneficiary.hh_is_household_head:
                    household_head_selection_id = choice.id

            ownership_type_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id","=",land_model_id.id), ("name","=","ownership_type")])
                .selection_ids
            )

            crop_is_diseased_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id","=",crop_model_id.id), ("name","=","is_diseased")])
                .selection_ids
            )

            livestock_is_diseased_selections = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id","=",livestock_model_id.id), ("name","=","is_diseased")])
                .selection_ids
            )
            
            land_info_data = []
            land_index = 1
            for land_info in beneficiary.land_information_ids:
                ownership_selection_id = False
                for choice in ownership_type_selections:
                    if choice.value == land_info.ownership_type:
                        ownership_selection_id = choice.id
                land_info_data.append({
                    "index": land_index,
                    'id': land_info.id,
                    'total_land_area': land_info.total_land_area,
                    'land_id': land_info.land_id,
                    # 'land_certificate': land_info.land_certificate,
                    'ownership_type': land_info.ownership_type,
                    'ownership_type_selection_id': ownership_selection_id
                })
                land_index += 1
                
            crop_info_data = []
            crop_index = 1
            for crop_info in beneficiary.crop_information_ids:
                crop_is_diseased_selection_id = False
                for choice in crop_is_diseased_selections:
                    if choice.value == crop_info.is_diseased:
                        crop_is_diseased_selection_id = choice.id
                crop_info_data.append({
                    "index": crop_index,
                    'id': crop_info.id,
                    'crop': crop_info.crop,
                    'is_diseased': crop_info.is_diseased,
                    'illness_type': crop_info.illness_type,
                    'crop_is_diseased_selection_id': crop_is_diseased_selection_id   
                })
                crop_index += 1
            
            serialized_crop_info_data = []
            for crop_info in crop_info_data:
                serialized_crop_info_data.append({
                    'index': crop_info['index'],
                    'id': crop_info['id'],
                    'crop_id': crop_info['crop'].id,
                    'is_diseased': crop_info['is_diseased'],
                    'illness_type': [it.id for it in crop_info['illness_type']],
                })
                
            livestock_info_data = []
            livestock_index = 1
            for livestock_info in beneficiary.livestock_information_ids:
                livestock_is_diseased_selection_id = False
                for choice in livestock_is_diseased_selections:
                    if choice.value == livestock_info.is_diseased:
                        livestock_is_diseased_selection_id = choice.id
                livestock_info_data.append({
                    'index': livestock_index,
                    'id': livestock_info.id,
                    'livestock_type': livestock_info.livestock_type,
                    'number_of_livestock': livestock_info.number_of_livestock,
                    'is_diseased': livestock_info.is_diseased,
                    'illness_type': livestock_info.illness_type,
                    'livestock_is_diseased_selection_id': livestock_is_diseased_selection_id
                })
                livestock_index += 1
            
            serialized_livestock_info_data = []
            for livestock_info in livestock_info_data:
                serialized_livestock_info_data.append({
                    'index': livestock_info['index'],
                    'id': livestock_info['id'],
                    'livestock_type': livestock_info['livestock_type'].id,
                    'is_diseased': livestock_info['is_diseased'],
                    'illness_type': [it.id for it in livestock_info['illness_type']],
                })
                         
            has_national_id = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_national_id")])
                .selection_ids
            )
            have_national_id_selection_id = False
            for choice in has_national_id:
                if choice.value == beneficiary.has_national_id:
                    have_national_id_selection_id = choice.id

            is_member_of_primary_cooperative = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
                .selection_ids
            )

            is_member_of_primary_cooperative_selection_id = False
            for choice in is_member_of_primary_cooperative:
                if choice.value == beneficiary.is_member_of_primary_cooperative:
                    is_member_of_primary_cooperative_selection_id = choice.id

            is_member_of_cooperative_union = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_of_primary_cooperative")])
                .selection_ids
            )
            is_member_of_cooperative_union_selection_id = False
            for choice in is_member_of_cooperative_union:
                if choice.value == beneficiary.is_member_of_cooperative_union:
                    is_member_of_cooperative_union_selection_id = choice.id

            is_member_in_farmer_cluster = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_member_in_farmer_cluster")])
                .selection_ids
            )

            is_member_in_farmer_cluster_selection_id = False
            for choice in is_member_in_farmer_cluster:
                if choice.value == beneficiary.is_member_in_farmer_cluster:
                    is_member_in_farmer_cluster_selection_id = choice.id

            role_in_cluster = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "role_in_farmer_cluster")])
                .selection_ids
            )
            role_in_cluster_selection_id = False
            for choice in role_in_cluster:
                if choice.value == beneficiary.role_in_farmer_cluster:
                    role_in_cluster_selection_id = choice.id

            access_to_machinery = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "access_to_machinery")])
                .selection_ids
            )

            access_to_machinery_selection_id = False
            for choice in access_to_machinery:
                if choice.value == beneficiary.access_to_machinery:
                    access_to_machinery_selection_id = choice.id

            has_finance_access =(
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_finance_access")])
                .selection_ids

            )
            access_to_finance_selection_id = False
            for choice in has_finance_access:
                if choice.value == beneficiary.has_finance_access:
                    access_to_finance_selection_id = choice.id



            marital_status = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "martial_status")])
                .selection_ids
            )
            marital_status_selection_id = False
            for mar_status in marital_status:
                if mar_status.value == beneficiary.martial_status:
                    marital_status_selection_id = mar_status.id

            education_level = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "education")])
                .selection_ids
            )
            education_level_selection_id = False
            for ed_level in education_level:
                if ed_level.value == beneficiary.education:
                    education_level_selection_id = ed_level.id

            farming_type = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "farming_type")])
                .selection_ids
            )
            farming_type_selection_id = False
            for farming_loop in farming_type:
                if farming_loop.value == beneficiary.farming_type:
                    farming_type_selection_id = farming_loop.id

            disability_status = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "is_disabled")])
                .selection_ids
            )
            disability_status_selection_id = False
            for disability in disability_status:
                if disability.value == beneficiary.is_disabled:
                    disability_status_selection_id = disability.id

            do_you_use_fertilizer = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_fertilizer")])
                .selection_ids
            )
            do_you_use_fertilizer_selection_id = False
            for use_fertilizer in do_you_use_fertilizer:
                if use_fertilizer.value == beneficiary.do_you_use_fertilizer:
                    do_you_use_fertilizer_selection_id = use_fertilizer.id

            do_you_use_pesticide = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_pesticide")])
                .selection_ids
            )

            do_you_use_pesticide_selection_id = False
            for use_pesticide in do_you_use_pesticide:
                if use_pesticide.value == beneficiary.do_you_use_pesticide:
                    do_you_use_pesticide_selection_id = use_pesticide.id

            do_you_use_insecticide = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_insecticide")])
                .selection_ids
            )

            do_you_use_insecticide_selection_id = False
            for use_insecticide in do_you_use_insecticide:
                if use_insecticide.value == beneficiary.do_you_use_pesticide:
                    do_you_use_insecticide_selection_id = use_insecticide.id

            do_you_use_improved_seed = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "do_you_use_improved_seed")])
                .selection_ids
            )

            do_you_use_improved_seed_selection_id = False
            for use_imroved_seed in do_you_use_improved_seed:
                if use_imroved_seed.value == beneficiary.do_you_use_pesticide:
                    do_you_use_improved_seed_selection_id = use_imroved_seed.id



            has_personal_phone = (
                request.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", "has_personal_phone")])
                .selection_ids
            )
            has_personal_phone_selection_id = False
            for has_phone in has_personal_phone:
                if has_phone.value == beneficiary.has_personal_phone:
                    has_personal_phone_selection_id = has_phone.id

            primary_phone = ""
            other_phone = ""
            secondary_phone = ""
            for phone in beneficiary.phone_number_ids:
                if phone.phone_type == "primary":
                    primary_phone = phone.phone_no
                elif phone.phone_type == "secondary":
                    secondary_phone = phone.phone_no
                elif phone.phone_type == "other":
                    other_phone = phone.phone_no

            uid = ""
            rid = ""
            for reg_id in beneficiary.reg_ids:
                if beneficiary.has_national_id == "yes" and reg_id.id_type.name == "UID":
                    uid = reg_id.value
                elif beneficiary.has_national_id == "no" and reg_id.id_type.name == "RID":
                    rid = reg_id.value
            
            return request.render(
                "g2p_ati_service_provider_portal.ati_individual_registrant_update_form_template",
                {
                    "beneficiary": beneficiary,
                    "has_national_id": has_national_id,
                    "uid": uid,
                    "rid": rid,
                    "hh_is_household_head": hh_is_household_head,
                    "gender": gender,
                    "region": region,
                    "zone": zone,
                    "woreda": woreda,
                    "kebele": kebele,
                    "primary_language": primary_language,
                    "has_personal_phone": has_personal_phone,
                    "primary_phone": primary_phone,
                    "secondary_phone": secondary_phone,
                    "other_phone": other_phone,
                    "farming_type": farming_type,
                    "is_member_of_primary_cooperative": is_member_of_primary_cooperative,
                    "is_member_of_cooperative_union": is_member_of_cooperative_union,
                    "is_member_in_farmer_cluster": is_member_in_farmer_cluster,
                    "primary_cooperatives": primary_cooperatives,
                    "cooperative_unions": cooperative_unions,
                    "primary_commodities": primary_commodities,
                    "role_in_cluster": role_in_cluster,
                    "ownership_type_selections": ownership_type_selections,
                    "land_info_data": land_info_data,
                    "crop_info_data": crop_info_data,
                    "serialized_crop_info_data": serialized_crop_info_data,
                    "livestock_info_data": livestock_info_data,
                    "serialized_livestock_info_data": serialized_livestock_info_data,
                    "crops": crops,
                    "crop_illness_type": crop_illness_type,
                    "crop_water_source": crop_water_source,
                    "livestock_types": livestock_types,
                    "livestock_illness_type": livestock_illness_type,
                    "water_source": water_source,
                    "access_to_machinery": access_to_machinery,
                    "machinary_types": machinary_types,
                    "marital_status": marital_status,
                    "education_level": education_level,
                    "disability_status": disability_status,
                    "do_you_use_fertilizer": do_you_use_fertilizer,
                    "do_you_use_pesticide": do_you_use_pesticide,
                    "do_you_use_insecticide": do_you_use_insecticide,
                    "do_you_use_improved_seed": do_you_use_improved_seed,
                    "has_finance_access": has_finance_access,
                    "financial_access": financial_access,
                    "source_of_income": source_of_income,
                    "have_national_id_selection_id": have_national_id_selection_id,
                    "household_head_selection_id": household_head_selection_id,
                    "farming_type_selection_id": farming_type_selection_id,
                    "role_in_cluster_selection_id": role_in_cluster_selection_id,
                    "is_member_in_farmer_cluster_selection_id": is_member_in_farmer_cluster_selection_id,
                    "is_member_of_cooperative_union_selection_id": is_member_of_cooperative_union_selection_id,
                    "is_member_of_primary_cooperative_selection_id": is_member_of_primary_cooperative_selection_id,
                    "education_level_selection_id": education_level_selection_id,
                    "marital_status_selection_id": marital_status_selection_id,
                    "access_to_machinery_selection_id": access_to_machinery_selection_id,
                    "access_to_finance_selection_id": access_to_finance_selection_id,
                    "disability_status_selection_id": disability_status_selection_id,
                    "has_personal_phone_selection_id": has_personal_phone_selection_id,
                    "crop_is_diseased_selections": crop_is_diseased_selections,
                    "livestock_is_diseased_selections": livestock_is_diseased_selections,
                    "do_you_use_fertilizer_selection_id": do_you_use_fertilizer_selection_id,
                    "do_you_use_pesticide_selection_id": do_you_use_pesticide_selection_id,
                    "do_you_use_insecticide_selection_id": do_you_use_insecticide_selection_id,
                    "do_you_use_improved_seed_selection_id": do_you_use_improved_seed_selection_id
                },
            )

        except Exception as e:
            print(e)
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": "Invalid URL."},
            )

    @http.route(
        "/serviceprovider/individual/update/submit",
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_individual_submit(self, **kw):
        print(kw)
        try:
            member = request.env["res.partner"].sudo().browse(int(kw.get("id holder")))

            if member:
                has_national_id = member.has_national_id
                primary_Language = member.primary_Language
                hh_is_household_head = member.hh_is_household_head
                given_name = member.given_name
                family_name = member.family_name
                gf_name_eng = member.gf_name_eng
                first_name_amh = member.first_name_amh
                family_name_amh = member.family_name_amh
                gf_name_amh = member.gf_name_amh
                first_name_other = member.first_name_other
                family_name_other = member.family_name_other
                gf_name_other = member.gf_name_other
                name = ""
                region = member.region
                zone = member.zone
                woreda = member.woreda
                kebele = member.kebele
                birthdate = member.birthdate
                gender = member.gender
                has_personal_phone = member.has_personal_phone
                email = member.email
                is_disabled = member.is_disabled
                farming_type = member.farming_type
                is_member_of_primary_cooperative = member.is_member_of_primary_cooperative
                primary_cooperatives = member.primary_cooperatives
                is_member_of_cooperative_union = member.is_member_of_cooperative_union
                cooperative_unions = member.cooperative_unions
                is_member_in_farmer_cluster = member.is_member_in_farmer_cluster
                primary_commodity = member.primary_commodity
                role_in_farmer_cluster = member.role_in_farmer_cluster
                martial_status = member.martial_status
                education = member.education
                crop_water_sources = member.crop_water_sources
                livestock_water_sources = member.livestock_water_sources
                access_to_machinery = member.access_to_machinery
                type_of_machinery = member.type_of_machinery
                has_finance_access = member.has_finance_access
                finance_accesses = member.finance_accesses
                martial_status = member.martial_status
                education = member.education
                hh_income_type = member.hh_income_type
               
                land_info_data = []
                crop_info_data = []
                livestock_info_data = []

                valid_keys = [key for key in kw.keys() if "{9999}" not in key]
                land_indices = set()
                crop_indices = set()
                livestock_indices = set()

                for key in valid_keys:
                    if key.startswith('land_ownership_type_'):
                        try:
                            land_index = int(key.split('_')[-1])
                            land_indices.add(land_index)
                        except ValueError:
                            continue
                    if key.startswith('crops_'):
                        try:
                            crop_index = int(key.split('_')[-1])
                            crop_indices.add(crop_index)
                        except ValueError:
                            continue
                    if key.startswith('livestock_types_'):
                        try:
                            livestock_index = int(key.split('_')[-1])
                            livestock_indices.add(livestock_index)
                        except ValueError:
                            continue

                # NATIONAL ID
                reg_ids = []                
                if kw.get("has_national_id"):
                    has_national_id_new = (
                            request.env["ir.model.fields.selection"]
                            .sudo()
                            .search([("id", "=", kw.get("has_national_id"))])
                            .value
                        )
                    has_national_id = has_national_id_new
                if has_national_id == "yes":
                    id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "UID")], limit=1)
                    reg_ids = [
                        (0, 0, {"id_type": id_type.id, "value": kw.get("uid")}),
                    ]
                elif has_national_id == "no" and kw.get("rid") and kw.get("rid").strip():
                    id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "RID")], limit=1)
                    reg_ids = [
                        (0, 0, {"id_type": id_type.id, "value": kw.get("rid")}),
                    ]

                # INDIVIDUAL DETAILS
                if kw.get("primary_language"):
                    primary_Language = int(kw.get("primary_language"))
                if kw.get("given_name"):
                    given_name = kw.get("given_name")
                    name += kw.get("given_name") + " "
                if kw.get("family_name"):
                    family_name = kw.get("family_name")
                    name += kw.get("family_name") + " "
                if kw.get("gf_name_eng"):
                    gf_name_eng = kw.get("gf_name_eng")
                    name += kw.get("gf_name_eng")
                if kw.get("first_name_amh") and kw.get("first_name_amh").strip():
                    first_name_amh = kw.get("first_name_amh")
                if kw.get("family_name_amh") and kw.get("family_name_amh").strip():
                    family_name_amh = kw.get("family_name_amh")
                if kw.get("gf_name_amh") and kw.get("gf_name_amh").strip():
                    gf_name_amh = kw.get("gf_name_amh")
                if kw.get("first_name_other") and kw.get("first_name_other").strip():
                    first_name_other = kw.get("first_name_other")
                if kw.get("family_name_other") and kw.get("family_name_other").strip():
                    family_name_other = kw.get("family_name_other")
                if kw.get("gf_name_other") and kw.get("gf_name_other").strip():
                    gf_name_other = kw.get("gf_name_other")
                if kw.get("region"):
                    region = int(kw.get("region"))
                if kw.get("zone"):
                    zone = int(kw.get("zone"))
                if kw.get("woreda"):
                    woreda = int(kw.get("woreda"))
                if kw.get("kebele"):
                    kebele = int(kw.get("kebele"))
                if kw.get("birthdate") and kw.get("birthdate"):
                    birthdate = kw.get("birthdate")
                if kw.get("gender"):
                    gender = kw.get("gender")

                if kw.get("has_personal_phone"):
                    has_personal_phone_new = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("has_personal_phone"))])
                        .value
                    )
                    has_personal_phone = has_personal_phone_new
                ethiopia_country_id = request.env['res.country'].sudo().search([('name', '=', 'Ethiopia')], limit=1).id
                phone_number_ids = []
                if has_personal_phone == "yes":
                    phone_number_ids.append((0, 0, {"phone_no": kw.get("primary_phone"), "phone_type": "primary", "country": ethiopia_country_id}))
                    if kw.get("secondary_phone") and kw.get("secondary_phone").strip():
                        phone_number_ids.append((0, 0, {"phone_no": kw.get("secondary_phone"), "phone_type": "secondary", "country": ethiopia_country_id}))
                elif has_personal_phone == "no":
                    phone_number_ids.append((0, 0, {"phone_no": kw.get("other_phone"), "phone_type": "other", "country": ethiopia_country_id}))
                    if kw.get("secondary_phone") and kw.get("secondary_phone").strip():
                        phone_number_ids.append((0, 0, {"phone_no": kw.get("secondary_phone"), "phone_type": "secondary", "country": ethiopia_country_id}))
                
                if kw.get("email") and kw.get("email").strip():
                    email = kw.get("email")
                if kw.get("is_disabled"):
                    is_disabled = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("is_disabled"))])
                        .value
                    )
                if kw.get("farming_type"):
                    farming_type = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("farming_type"))])
                        .value
                    )
                    
                # SOCIO ECONOMIC DATA
                if kw.get("marital_status"):
                    martial_status = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("marital_status"))])
                        .value
                    )
                if kw.get("education_level"):
                    education = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("education_level"))])
                        .value
                    )
                income_source = request.httprequest.form.getlist("hh_income_type")
                if income_source:
                    income_source_ids = [int(id) for id in income_source]
                    hh_income_type = [(6, 0, income_source_ids)]

                # MEMBERSHIP DETAILS
                if kw.get("is_member_of_primary_coop") and kw.get("is_member_of_primary_coop").strip():
                    is_member_of_primary_cooperative = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("is_member_of_primary_coop"))])
                        .value
                    )
                if is_member_of_primary_cooperative == "yes":
                    if kw.get("name_of_primary_coop") and kw.get("name_of_primary_coop").strip():
                        primary_cooperatives = int(kw.get("name_of_primary_coop"))
                if kw.get("is_member_of_coop_union") and kw.get("is_member_of_coop_union").strip():
                    is_member_of_cooperative_union = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("is_member_of_coop_union"))])
                        .value
                    )
                if is_member_of_cooperative_union == "yes":
                    if kw.get("name_of_coop_union") and kw.get("name_of_coop_union").strip():
                        cooperative_unions = int(kw.get("name_of_coop_union"))
                if kw.get("in_farmer_cluster") and kw.get("in_farmer_cluster").strip():
                    is_member_in_farmer_cluster = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("in_farmer_cluster"))])
                        .value
                    )
                if is_member_in_farmer_cluster == "yes":
                    if kw.get("primary_commodity") and kw.get("primary_commodity").strip():
                        primary_commodity = int(kw.get("primary_commodity"))
                    if kw.get("role_in_cluster") and kw.get("role_in_cluster").strip():
                        role_in_farmer_cluster = (
                            request.env["ir.model.fields.selection"]
                            .sudo()
                            .search([("id", "=", kw.get("role_in_cluster"))])
                            .value
                        )

                # LAND INFORMATION
                supporting_documents_ids = []
                backend_id = (
                    request.env.ref("storage_backend.default_storage_backend").id
                    or request.env["storage.backend"].sudo().search([], limit=1).id
                )
                
                doc_tag = request.env["g2p.document.tag"].sudo().get_tag_by_name("Land Certificate")
                if not doc_tag:
                    doc_tag = request.env["g2p.document.tag"].sudo().create({"name": "Land Certificate"})
                for index in land_indices:
                    ownership_type = kw.get(f'land_ownership_type_{index}')
                    if ownership_type == " ":
                        continue
                    land_id = kw.get(f'land_id_{index}')
                    land_area = kw.get(f'total_land_area_{index}')
                    land_ownership_type = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", ownership_type)])
                        .value
                    )
                    if kw.get(f'land_certificate_{index}') and (f'land_certificate_{index}').strip():
                        land_certificate = kw.get(f'land_certificate_{index}')
                        binary_content = base64.b64encode(land_certificate.read()).decode('utf-8')
                        supporting_documents_ids.append(
                            (
                                0,
                                0,  
                                {
                                    "backend_id": backend_id,
                                    "name": land_certificate.filename,
                                    "data": binary_content,
                                    "tags_ids": [(4, doc_tag.id)]
                                },
                            )
                        )
                    land_info_data.append((0, 0, {
                        'ownership_type': land_ownership_type,
                        'total_land_area': land_area,
                        'land_id': land_id,
                    }))
                                    
                # CROP INFORMATION
                crop_ws = request.httprequest.form.getlist("crop_water_source")
                if crop_ws:
                    crop_water_sources_ids = [int(id) for id in crop_ws]
                    crop_water_sources = [(6, 0, crop_water_sources_ids)]

                for index in crop_indices:
                    crop_id = kw.get(f'crops_{index}')
                    if crop_id == " ":
                        continue

                    crop_info_data.append((0, 0, {
                        'crop': crop_id,
                    }))

                # LIVESTOCK INFORMATION
                livestock_ws = request.httprequest.form.getlist("livestock_water_source")
                if livestock_ws:
                    livestock_water_sources_ids = [int(id) for id in livestock_ws]
                    livestock_water_sources = [(6, 0, livestock_water_sources_ids)]

                for index in livestock_indices:
                    livestock_type = kw.get(f'livestock_types_{index}')
                    if livestock_type == " ":
                        continue
                    number_of_livestock = kw.get(f'number_of_livestock_{index}')

                    livestock_info_data.append((0, 0, {
                        'livestock_type': livestock_type,
                        'number_of_livestock': number_of_livestock,
                    }))
                

                
                # ACCESS TO RESOURCE
                if kw.get("access_to_machinery") and kw.get("access_to_machinery").strip():
                    access_to_machinery = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("access_to_machinery"))])
                        .value
                    )
                if access_to_machinery == 'yes':
                    machinery_types = request.httprequest.form.getlist("machinery_types")
                    if machinery_types:
                        machinery_types_ids = [int(id) for id in machinery_types]
                        type_of_machinery = [(6, 0, machinery_types_ids)]
                
                # FINANCIAL SERVICE
                if kw.get("has_finance_access") and kw.get("has_finance_access").strip():
                    has_finance_access = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("has_finance_access"))])
                        .value
                    )
                if has_finance_access == 'yes':
                    access_to_finance = request.httprequest.form.getlist("finance_accesses")
                    if access_to_finance:
                        access_to_finance_ids = [int(id) for id in access_to_finance]
                        finance_accesses = [(6, 0, access_to_finance_ids)]

                member.reg_ids.unlink()
                member.phone_number_ids.unlink()
                member.land_information_ids.unlink()
                member.crop_information_ids.unlink()
                member.livestock_information_ids.unlink()
                member.sudo().write(
                    {
                        "has_national_id": has_national_id,
                        "reg_ids": reg_ids,
                        "hh_is_household_head": hh_is_household_head,
                        "primary_Language": primary_Language,
                        "given_name": given_name,
                        "family_name": family_name,
                        "gf_name_eng": gf_name_eng,
                        "name": name,
                        "first_name_amh": first_name_amh,
                        "family_name_amh": family_name_amh,
                        "gf_name_amh": gf_name_amh,
                        "first_name_other": first_name_other,
                        "family_name_other": family_name_other,
                        "gf_name_other": gf_name_other,
                        "region": region,
                        "zone": zone,
                        "woreda": woreda,
                        "kebele": kebele,
                        "birthdate": birthdate,
                        "gender": gender,
                        "has_personal_phone": has_personal_phone,
                        "phone_number_ids": phone_number_ids,
                        "email": email,
                        "is_disabled": is_disabled,
                        "farming_type": farming_type,
                        "martial_status": martial_status,
                        "education": education,
                        "hh_income_type": hh_income_type,
                        "is_member_of_primary_cooperative": is_member_of_primary_cooperative,
                        "primary_cooperatives": primary_cooperatives,
                        "is_member_of_cooperative_union": is_member_of_cooperative_union,
                        "cooperative_unions": cooperative_unions,
                        "is_member_in_farmer_cluster": is_member_in_farmer_cluster,
                        "primary_commodity": primary_commodity,
                        "role_in_farmer_cluster": role_in_farmer_cluster,
                        "land_information_ids": land_info_data,
                        "crop_water_sources": crop_water_sources,
                        "crop_information_ids": crop_info_data,
                        "livestock_water_sources": livestock_water_sources,
                        "livestock_information_ids": livestock_info_data,
                        "access_to_machinery": access_to_machinery,
                        "type_of_machinery": type_of_machinery,
                        "has_finance_access": has_finance_access,
                        "finance_accesses": finance_accesses,
                    }
                )
                
            return request.redirect("/serviceprovider/individual")

        except Exception as e:
            print(e)
            # _logger.error("Error occurred%s" % e)
            return request.render(
                "g2p_service_provider_beneficiary_management.error_template",
                {"error_message": f"An error occurred. {e}"},
            )
        

    @http.route("/serviceprovider/individual", type="http", auth="user", website=True)
    def individual_list(self, **kw):
        individual = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    ("active", "=", True),
                    ("is_registrant", "=", True),
                    ("is_group", "=", False),
                    ("is_farmer", "=", 'yes'),
                ]
            )
        )
        region = request.env["g2p.region"].sudo().search([])
        zone = request.env["g2p.zone"].sudo().search([])
        woreda = request.env["g2p.woreda"].sudo().search([])
        kebele = request.env["g2p.kebele"].sudo().search([])
        return request.render("g2p_service_provider_beneficiary_management.individual_list", {"individual": individual, "region": region, "zone": zone, "wereda": woreda, "kebele": kebele },
    )

    @http.route("/serviceprovider/group", type="http", auth="user", website=True)
    def group_list(self, **kw):
        groups = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    ("active", "=", True),
                    ("is_registrant", "=", True),
                    ("is_group", "=", True),
                ]
            )
        )
        region = request.env["g2p.region"].sudo().search([])
        zone = request.env["g2p.zone"].sudo().search([])
        woreda = request.env["g2p.woreda"].sudo().search([])
        kebele = request.env["g2p.kebele"].sudo().search([])
        return request.render("g2p_service_provider_beneficiary_management.group_list", {"groups": groups, "region": region, "zone": zone, "wereda": woreda, "kebele": kebele },
    )

    @http.route(
        "/serviceprovider/member/update/",
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_member(self, **kw):
        member_id = kw.get("member_id")
        print("member_id issssss", member_id)
        print(kw)
        try:
            beneficiary = request.env["res.partner"].sudo().browse(int(member_id))
            # relationship_role = request.env["g2p.group.membership.kind"].sudo().search()
            # print("relationship_role",relationship_role)

            if beneficiary:
                exist_value = {
                    "given_name": beneficiary.given_name,
                    "family_name": beneficiary.family_name,
                    "gf_name_eng": beneficiary.gf_name_eng,
                    "dob": str(beneficiary.birthdate),
                    "gender": beneficiary.gender,
                    "id": beneficiary.id,
                }
                return json.dumps(exist_value)

        except Exception as e:
            print(e)
            # _logger.error("ERROR LOG IN UPDATE MEMBER%s", e)


    @http.route(
        "/serviceprovider/family_member/update/submit/",
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def update_family_member_submit(self, **kw):
        print("Hello world")
        res =  dict()
        try:
            group_id = kw.get("group_id")
            member_id = int(kw.get("member_id"))
            member = request.env["res.partner"].sudo().browse(member_id)
            if not group_id:
                return json.dumps({"error": "Group ID is required"})
            
            group_rec = request.env["res.partner"].sudo().browse(int(group_id))
            print(group_rec)
            if not group_rec.exists():
                return json.dumps({"error": "Group not found"})


            if member:
                given_name = kw.get("given_name")
                family_name = kw.get("family_name")
                gf_name_eng = kw.get("gf_name_eng")
                birthdate = kw.get("birthdate")
                gender = kw.get("gender")

                full_name = f"{given_name} {family_name} {gf_name_eng}"
               
                partner_data = {
                    "given_name": given_name,
                    "family_name": family_name,
                    "gf_name_eng": gf_name_eng,
                    "name": full_name,
                    "birthdate": str(birthdate),
                    "gender": gender,
                    "is_group": False,

                }

                

                member.sudo().write(partner_data)



                member_list = []

            

                for membership in group_rec.group_membership_ids:
                    

                    if membership.individual.is_farmer == "yes":
                        continue
                    else:
                        member_list.append({
                            "id": membership.individual.id,
                            "name": membership.individual.name,
                            "birthdate": str(membership.individual.birthdate),  # Ensure date is serialized
                            "gender": membership.individual.gender,
                            # "relationship":membership.individual.kind,
                            "active": membership.individual.active,
                            "group_id": membership.group.id,
                        })

                res["member_list"] = member_list
                print("member list is",member_list)

            

                return json.dumps(res)

        except Exception as e:
            print(e)
            # _logger.error("ERROR LOG IN INDIVIDUAL%s", e)
            return json.dumps({"error": "Failed to edit family member"})

   

    @http.route(
        "/serviceprovider/family_member/add/submit/",
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def add_family_member_submit(self, **kw):
        print("workkkkkkkkkk")
        res = dict()
        
        print(kw)
        try:
            group_id = kw.get("group_id")
            if not group_id:
                return json.dumps({"error": "Group ID is required"})
            
            group_rec = request.env["res.partner"].sudo().browse(int(group_id))
            print(group_rec)
            if not group_rec.exists():
                return json.dumps({"error": "Group not found"})

            given_name = kw.get("given_name")
            family_name = kw.get("family_name")
            gf_name_eng = kw.get("gf_name_eng")
            relationship = kw.get("relationship")

            # print("relation is ",relationship)
            

            name = f"{given_name} {family_name} {gf_name_eng}"

            partner_data = {
                "name": name,
                "given_name": given_name,
                "family_name": family_name,
                "gf_name_eng": gf_name_eng,
                "birthdate": kw.get("birthdate"),
                "gender": kw.get("gender"),
                "is_registrant": True,
                "is_group": False,
            }



            individual = request.env["res.partner"].sudo().create(partner_data)

            # if relationship.strip():
            #     membership_kind = self.get_membership_kind(relationship)

            # group_membership_vals = [(0, 0, {"individual": individual.id, "group": group_rec.id,"kind":[(4, membership_kind)]})]

            group_membership_vals = [(0, 0, {"individual": individual.id, "group": group_rec.id})]


            group_rec.write({"group_membership_ids": group_membership_vals})

            member_list = []

        

            for membership in group_rec.group_membership_ids:
                if membership.individual.is_farmer == "yes":
                    continue
                else:
                    member_list.append({
                        "id": membership.individual.id,
                        "name": membership.individual.name,
                        "birthdate": str(membership.individual.birthdate),  # Ensure date is serialized
                        "gender": membership.individual.gender,
                        # "relationship":membership.individual.kind,
                        "active": membership.individual.active,
                        "group_id": membership.group.id,
                    })

            res["member_list"] = member_list

          

            return json.dumps(res)

        except Exception as e:
            print(e)
            # _logger.error("ERROR LOG IN INDIVIDUAL%s", e)
            return json.dumps({"error": "Failed to add family member"})
        
    def get_membership_kind(self, relationship):
        if relationship == "Wife":
            relationship = "Wife - Head"
        if relationship == "Husband":
            relationship = "Husband - Head"

        membership_kind = (
            request.env["g2p.group.membership.kind"].sudo().search([("name", "=", relationship)], limit=1)
        )
        return membership_kind.id


    @http.route(
        ["/serviceprovider/individual/create/"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def individual_create(self, **kw):
        print("Creating Individual")
        res = dict()
        try:
            head_name = kw.get("given_name")
            if kw.get("region").strip():
                region = int(kw.get("region"))
            if kw.get("zone").strip():
                zone = int(kw.get("zone"))
            if kw.get("woreda").strip():
                woreda = int(kw.get("woreda"))
            if kw.get("kebele").strip():
                kebele = int(kw.get("kebele"))
            head_individual = None
            # Group creation
            if kw.get("group_id"):
                group_rec = request.env["res.partner"].sudo().browse(int(kw.get("group_id")))
            else:
                if head_name:
                    group_rec = (
                        request.env["res.partner"]
                        .sudo()
                        .create({
                            "name": head_name,
                            "region": region,
                            "zone": zone,
                            "woreda": woreda,
                            "kebele": kebele,
                            "is_registrant": True,
                            "is_group": True})
                    )
            vals = {
                "is_registrant": True,
                "is_group": False,
            }
            name = ""

            land_records = json.loads(kw.get('landRecords', '[]'))

            land_info_data = []
            supporting_documents_ids = []
            backend_id = (
                request.env.ref("storage_backend.default_storage_backend").id
                or request.env["storage.backend"].sudo().search([], limit=1).id
            )
            
            doc_tag = request.env["g2p.document.tag"].sudo().get_tag_by_name("Land Certificate")
            if not doc_tag:
                    doc_tag = request.env["g2p.document.tag"].sudo().create({"name": "Land Certificate"})
            for record in land_records:
                # Skip the record if any of its keys contain "{9999}"
                if any("{9999}" in key for key in record.keys()):
                    continue

                # Extract the index from the first key (you can choose any key that contains the index)
                for key in record.keys():
                    if "ownership_type_" in key:
                        index = key.split("_")[-1]

                        ownership_type = record.get(f'ownership_type_{index}', '').strip()
                        if not ownership_type:
                            continue

                        land_id = record.get(f'land_id_{index}')
                        land_area = record.get(f'total_land_area_{index}')

                        # Fetch land ownership type value
                        land_ownership_type = (
                            request.env["ir.model.fields.selection"]
                            .sudo()
                            .search([("id", "=", ownership_type)])
                            .value
                        )

                        land_info_dict = {
                            'ownership_type': land_ownership_type,
                            'total_land_area': land_area,
                            'land_id': land_id,
                        }

                        # Process land certificate if it exists and is not empty
                        land_certificate = record.get(f'land_certificate_{index}')
                        # print(land_certificate)
                        if land_certificate:
                            content = land_certificate.get('content')
                            binary_data = bytes(content, 'latin1') 
                            storage_file = (
                                request.env["storage.file"]
                                .sudo()
                                .create(
                                    {
                                        "backend_id": backend_id,
                                        "name": land_certificate.get('filename'),
                                        "data": binary_data,
                                        "tags_ids": [(4, doc_tag.id)],
                                    }
                                )
                            )
                            land_info_dict["land_certificate"] = storage_file.id
                            supporting_documents_ids.append((4, storage_file.id))

                        land_info_data.append((0, 0, land_info_dict))
                    break  # Exit the loop since the index is identified for this record
            # return
            print(land_info_data)
            vals["land_information_ids"] = land_info_data
            vals["supporting_documents_ids"] = supporting_documents_ids
            vals["region"] = region
            vals["zone"] = zone
            vals["woreda"] = woreda
            vals["kebele"] = kebele

            crop_records = json.loads(kw.get('cropRecords', '[]'))

            crop_info_data = []

            for record in crop_records:

                # Check for any key containing "{9999}" and skip those records
                if any("{9999}" in key for key in record.keys()):
                    continue

                # Initialize a flag to check if the record has any non-empty value
                # valid_record = False

                for key in record.keys():
                    if "crops_" in key:
                        index = key.split("_")[-1]
                        crop_id = record.get(f'crops_{index}', '').strip()  # Handle None with default ''

                        if crop_id:  # If crop_id is not empty, consider this a valid record0
                            crop_info_data.append((0, 0, {
                                'crop': int(crop_id),
                            }))
                            # valid_record = True
                            break  # Exit the loop after finding the relevant key

                # If the record had no valid (non-empty) values, it won't be added to crop_info_data

            # Assign the filtered crop_info_data to the vals dictionary
            vals["crop_information_ids"] = crop_info_data

            livestock_records = json.loads(kw.get('livestockRecord', '[]'))

            livestock_info_data = []
            for record in livestock_records:
                if any("{9999}" in key for key in record.keys()):
                    continue
                for key in record.keys():
                    if "livestock_types_" in key:
                        index = key.split("_")[-1]
                        livestock_type = record.get(f'livestock_types_{index}').strip()
                        if not livestock_type:
                            continue
                        number_of_livestock = record.get(f'number_of_livestock_{index}')

                        livestock_info_data.append((0, 0, {
                            'livestock_type': int(livestock_type),
                            'number_of_livestock': number_of_livestock,
                        }))
                        break
            vals["livestock_information_ids"] = livestock_info_data

            # # NATIONAL ID
            reg_ids = []
            has_national_id = None
            if kw.get("hasNationalId"):
                has_national_id = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("hasNationalId"))])
                    .value
                )
                vals["has_national_id"] = has_national_id

            if has_national_id == "yes":
                id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "UID")], limit=1)
                vals["reg_ids"] = [
                    (0, 0, {"id_type": id_type.id, "value": kw.get("selectedId")}),
                ]

            elif has_national_id == "no" and kw.get("rid"):
                id_type = request.env["g2p.id.type"].sudo().search([("name", "=", "RID")], limit=1)
                vals["reg_ids"] = [
                    (0, 0, {"id_type": id_type.id, "value": kw.get("rid")}),
                ]
            # INDIVIDUAL DETAILS
            if kw.get("primaryLanguage"):
                vals["primary_Language"] = int(kw.get("primaryLanguage"))

            if kw.get("given_name"):
                vals["given_name"] = kw.get("given_name")
                name += kw.get("given_name") + " "
            if kw.get("family_name"):
                vals["family_name"] = kw.get("family_name")
                name += kw.get("family_name") + " "
            if kw.get("addl_name"):
                vals["gf_name_eng"] = kw.get("addl_name")
                name += kw.get("addl_name")
            if name:
                vals["name"] = name
            if kw.get("firstNameAmh"):
                vals["first_name_amh"] = kw.get("firstNameAmh")
            if kw.get("familyNameAmh"):
                vals["family_name_amh"] = kw.get("familyNameAmh")
            if kw.get("gFNameAmh"):
                vals["gf_name_amh"] = kw.get("gFNameAmh")
            if kw.get("firstNameOther"):
                vals["first_name_other"] = kw.get("firstNameOther")
            if kw.get("familyNameOther"):
                vals["family_name_other"] = kw.get("familyNameOther")
            if kw.get("lastNameOther"):
                vals["gf_name_other"] = kw.get("lastNameOther")
            print("dat of birth")
            print(kw.get("dob"))
            if kw.get("dob"):
                vals["birthdate"] = kw.get("dob")
            print(kw.get("gender"))
            if kw.get("gender"):
                vals["gender"] = kw.get("gender")
            has_personal_phone = None

            if kw.get("isHouseholdHead"):
                is_household_head = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("isHouseholdHead"))])
                    .value
                )
                vals["hh_is_household_head"] = is_household_head

            if kw.get("havePhoneNumber"):
                has_personal_phone = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("havePhoneNumber"))])
                    .value
                )
                vals["has_personal_phone"] = has_personal_phone
            ethiopia_country_id = request.env['res.country'].sudo().search([('name', '=', 'Ethiopia')], limit=1).id
            phone_no = []

            if has_personal_phone == "yes":
                phone_no.append((0, 0, {"phone_no": kw.get("primaryPhoneNumber"), "phone_type": "primary",
                                        "country_id": ethiopia_country_id}))
                if kw.get("secondaryPhoneNumber") and kw.get("secondaryPhoneNumber").strip():
                    phone_no.append((0, 0, {"phone_no": kw.get("secondaryPhoneNumber"), "phone_type": "secondary",
                                            "country_id": ethiopia_country_id}))
            elif has_personal_phone == "no":
                phone_no.append((0, 0, {"phone_no": kw.get("otherPhoneNumber"), "phone_type": "other",
                                        "country_id": ethiopia_country_id}))
                if kw.get("secondary_phone") and kw.get("secondary_phone").strip():
                    phone_no.append((0, 0, {"phone_no": kw.get("secondary_phone"), "phone_type": "secondary",
                                            "country_id": ethiopia_country_id}))
            vals["phone_number_ids"] = phone_no

            if kw.get("email") and kw.get("email").strip():
                vals["email"] = kw.get("email")
            if kw.get("isDisabled"):
                vals["is_disabled"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("isDisabled"))])
                    .value
                )

            if kw.get("farmingType"):
                vals["farming_type"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("farmingType"))])
                    .value
                )

            # SOCIO ECONOMIC DATA
            if kw.get("maritalStatus"):
                vals["martial_status"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("maritalStatus"))])
                    .value
                )
            if kw.get("educationLevel"):
                vals["education"] = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("educationLevel"))])
                    .value
                )
            income_source = []

            incomeTyepe = json.loads(kw.get('newIncomeType', '[]'))
            if incomeTyepe:
                income_source_ids = [int(id) for id in incomeTyepe]
                vals["hh_income_type"] = [(6, 0, income_source_ids)]

            cropWaterSource = json.loads(kw.get('cropWaterSource', '[]'))
            if cropWaterSource:
                crop_water_source_ids = [int(id) for id in cropWaterSource]
                vals["crop_water_sources"] = [(6, 0, crop_water_source_ids)]

            livestockWaterSource = json.loads(kw.get('livestockWaterSource', '[]'))
            if livestockWaterSource:
                livestock_water_source_ids = [int(id) for id in livestockWaterSource]
                vals["livestock_water_sources"] = [(6, 0, livestock_water_source_ids)]

            matchinaryTypes = json.loads(kw.get('matchinaryTypes', '[]'))
            if matchinaryTypes:
                type_of_machinery_ids = [int(id) for id in matchinaryTypes]
                vals["type_of_machinery"] = [(6, 0, type_of_machinery_ids)]

            financialSectors = json.loads(kw.get('financialSectors', '[]'))
            if financialSectors:
                financial_sectors_ids = [int(id) for id in financialSectors]
                vals["finance_accesses"] = [(6, 0, financial_sectors_ids)]
            # MEMBERSHIP DETAILS
            is_member_of_primary_cooperative = False
            is_member_of_cooperative_union = False
            is_member_in_farmer_cluster = False
            if kw.get("isMemberOfPrimaryCoop") and kw.get("isMemberOfPrimaryCoop").strip():
                is_member_of_primary_cooperative = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("isMemberOfPrimaryCoop"))])
                    .value
                )
                vals["is_member_of_primary_cooperative"] = is_member_of_primary_cooperative
            if is_member_of_primary_cooperative == "yes":
                if kw.get("nameOfPrimaryCoop") and kw.get("nameOfPrimaryCoop").strip():
                    vals["primary_cooperatives"] = int(kw.get("nameOfPrimaryCoop"))
            if kw.get("isMemberOfCoopUnion") and kw.get("isMemberOfCoopUnion").strip():
                is_member_of_cooperative_union = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("isMemberOfCoopUnion"))])
                    .value
                )
                vals["is_member_of_cooperative_union"] = is_member_of_cooperative_union
            if is_member_of_cooperative_union == "yes":
                if kw.get("nameOfCoopUnion") and kw.get("nameOfCoopUnion").strip():
                    vals["cooperative_unions"] = int(kw.get("nameOfCoopUnion"))

            if kw.get("inFarmerCluster") and kw.get("inFarmerCluster").strip():
                is_member_in_farmer_cluster = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("inFarmerCluster"))])
                    .value
                )
                vals["is_member_in_farmer_cluster"] = is_member_in_farmer_cluster
            if is_member_in_farmer_cluster == "yes":
                if kw.get("primaryComodity") and kw.get("primaryComodity").strip():
                    vals["primary_commodity"] = int(kw.get("primaryComodity"))
                if kw.get("roleInCluster") and kw.get("roleInCluster").strip():
                    vals["role_in_farmer_cluster"] = (
                        request.env["ir.model.fields.selection"]
                        .sudo()
                        .search([("id", "=", kw.get("roleInCluster"))])
                        .value
                    )

            if kw.get("usedFertilizer") and kw.get("usedFertilizer").strip():
                do_you_use_fertilizer = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("usedFertilizer"))])
                    .value
                )
                vals["do_you_use_fertilizer"] = do_you_use_fertilizer

            if kw.get("usedPesticide") and kw.get("usedPesticide").strip():
                do_you_use_pesticide = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("usedPesticide"))])
                    .value
                )
                vals["do_you_use_pesticide"] = do_you_use_pesticide

            if kw.get("usedInsecticide") and kw.get("usedInsecticide").strip():
                do_you_use_insecticide = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("usedInsecticide"))])
                    .value
                )
                vals["do_you_use_insecticide"] = do_you_use_insecticide

            if kw.get("usedImprovedSeed") and kw.get("usedImprovedSeed").strip():
                do_you_use_improved_seed = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("usedInsecticide"))])
                    .value
                )
                vals["do_you_use_improved_seed"] = do_you_use_improved_seed

            # ACCESS TO RESOURCE
            access_to_machinery = None
            if kw.get("accessToMachinary") and kw.get("accessToMachinary").strip():
                access_to_machinery = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("accessToMachinary"))])
                    .value
                )
                vals["access_to_machinery"] = access_to_machinery
            if access_to_machinery == 'yes':
                machinery_types = request.httprequest.form.getlist("machinery_types")
                if machinery_types:
                    machinery_types_ids = [int(id) for id in machinery_types]
                    vals["type_of_machinery"] = [(6, 0, machinery_types_ids)]

            # FINANCIAL SERVICE
            has_finance_access = None
            if kw.get("has_finance_access") and kw.get("has_finance_access") != " ":
                has_finance_access = (
                    request.env["ir.model.fields.selection"]
                    .sudo()
                    .search([("id", "=", kw.get("has_finance_access"))])
                    .value
                )
                vals["has_finance_access"] = has_finance_access
            if has_finance_access == 'yes':
                access_to_finance = request.httprequest.form.getlist("finance_accesses")
                if access_to_finance:
                    access_to_finance_ids = [int(id) for id in access_to_finance]
                    vals["finance_accesses"] = [(6, 0, access_to_finance_ids)]

            # Other
            vals["is_farmer"] = "yes"

            # TODO: Relationship logic need to build later
            if kw.get("relationship"):
                kw.pop("relationship")
            print(vals)
            individual = request.env["res.partner"].sudo().create(vals)

            # Member creation only if head_individual is created
            group_membership_vals = [(0, 0, {"individual": individual.id, "group": group_rec.id})]

            # Add head_individual membership if created
            if head_individual:
                group_membership_vals.insert(
                    0, (0, 0, {"individual": head_individual.id, "group": group_rec.id})
                )

            group_rec.write({"group_membership_ids": group_membership_vals})

            member_list = []
            for membership in group_rec.group_membership_ids:
                member_list.append(
                    {
                        "id": membership.individual.id,
                        "name": membership.individual.name,
                        "age": membership.individual.age,
                        "gender": membership.individual.gender,
                        "active": membership.individual.active,
                        "group_id": membership.group.id,
                    }
                )

            res["member_list"] = member_list
            return json.dumps(res)

        except Exception as e:
            print("exception thrown", e)

    
    @http.route(
        ["/serviceprovider/member/create/"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def member_create(self, **kw):
        res = dict()
        try:
            head_name = kw.get("household_name")
            head_individual = None
            # Group creation
            if kw.get("group_id"):
                group_rec = request.env["res.partner"].sudo().browse(int(kw.get("group_id")))
            else:
                print("please create group first")

            given_name = kw.get("given_name")
            family_name = kw.get("family_name")
            addl_name = kw.get("addl_name")

            name = f"{given_name}, {addl_name} {family_name}"

            partner_data = {
                "name": name,
                "given_name": given_name,
                "family_name": family_name,
                "gf_name_eng": addl_name,
                "birthdate": kw.get("birthdate"),
                "gender": kw.get("gender"),
                "is_registrant": True,
                "is_group": False,
                "is_farmer": 'no',
            }

            individual = request.env["res.partner"].sudo().create(partner_data)

            def get_membership_kind(relationship):
                if relationship == "Wife":
                    relationship = "Wife - Head"
                if relationship == "Husband":
                    relationship = "Husband - Head"

                membership_kind = (
                    request.env["g2p.group.membership.kind"].sudo().search([("name", "=", relationship)], limit=1)
                )
                if not membership_kind:
                    membership_kind = request.env["g2p.group.membership.kind"].sudo().create({"name": relationship})
                return membership_kind.id
            
            if kw.get("relationship").strip():
                print(kw.get("relationship"))
                membership_kind = get_membership_kind(kw.get("relationship"))

            # Member creation only if head_individual is created
            group_membership_vals = [(0, 0, {"individual": individual.id, "group": group_rec.id, "kind": [(4, membership_kind)]})]

            # Add head_individual membership if created
            if head_individual:
                group_membership_vals.insert(
                    0, (0, 0, {"individual": head_individual.id, "group": group_rec.id})
                )

            group_rec.write({"group_membership_ids": group_membership_vals})

            member_list = []
            for membership in group_rec.group_membership_ids:
                if membership.individual.is_farmer == "no":
                    member_list.append(
                        {
                            "id": membership.individual.id,
                            "name": membership.individual.name,
                            "age": membership.individual.age,
                            "gender": membership.individual.gender,
                            "active": membership.individual.active,
                            "group_id": membership.group.id,
                        }
                    )

            res["member_list"] = member_list
            return json.dumps(res)

        except Exception as e:
            _logger.error("ERROR LOG IN INDIVIDUAL%s", e)