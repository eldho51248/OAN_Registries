import base64
import json

import odoo.addons.g2p_odk_importer.models.odk_client as base_odk_client


def get_value_ids(self, model, value_list):
    ids = []
    for value in value_list:
        if value == "other":
            ids.append(value)
        record = self.env[model].search([("code", "=", value)], limit=1)
        if record:
            ids.append(record.id)

    return ids


def get_value_many2one(self, model, value):
    id_val = False
    if value:
        record = self.env[model].search([("code", "=", value)], limit=1)
        if record:
            id_val = record.id
    return id_val


def process_many2one_field(self, model_name, field_value):
    if field_value == "other":
        return field_value
    field_id = get_value_many2one(self, model_name, field_value)
    return field_id if field_id else None


def process_many2many_field(self, model_name, field_value):
    if field_value is not None:
        field_list = field_value.split(" ")
    else:
        field_list = []
    field_ids = get_value_ids(self, model_name, field_list)
    return field_ids


def process_phone_ids(self, json_data):
    # Fetch the country ID for Ethiopia
    ethiopia_country_id = self.env["res.country"].search([("name", "=", "Ethiopia")], limit=1).id
    json_data["phone_number_ids"] = [
        (
            0,
            0,
            {
                "phone_no": "+" + phone.get("phone_no"),
                "phone_type": phone.get("phone_type"),
                "country_id": ethiopia_country_id,
            },
        )
        for phone in json_data["phone_ids"]
    ]
    return json_data


def process_land_ids(self, json_data, is_member):
    land_information_ids = []
    if json_data["land_information_ids"] is not None:
        for land_info in json_data["land_information_ids"]:
            ownership_type = land_info.get(
                "hh_member_land_ownership" if is_member else "land_ownership", None
            )
            if not ownership_type:
                continue
            land_certificate = land_info.get(
                "hh_member_land_certificate" if is_member else "land_certificate", None
            )
            land_certificate_id = None
            if land_certificate and json_data.get("file_ids"):
                # link the uploaded storage.file id to the land_certificate
                # of this entry using the name of the file
                for file_id in json_data["file_ids"]:
                    if land_certificate == file_id[0]:
                        land_certificate_id = file_id[1]

            land_info_dict = {
                "ownership_type": ownership_type,
                "total_land_area": land_info.get(
                    "hh_member_total_land_area" if is_member else "total_land_area", 0
                ),
                "land_id": land_info.get("hh_member_land_id" if is_member else "land_id", 0),
            }
            if land_certificate_id:
                land_info_dict["land_certificate"] = land_certificate_id
            land_information_ids.append((0, 0, land_info_dict))

    return land_information_ids


def process_crop_ids(self, json_data, is_member):
    crop_information_ids = []
    if json_data["crop_information_ids"] is not None:
        for crop_info in json_data["crop_information_ids"]:
            crop = crop_info.get("hh_member_crop_name" if is_member else "crop_name", None)
            if not crop:
                continue
            crop_id = get_value_many2one(
                self, "g2p.crop", crop_info.get("hh_member_crop_name" if is_member else "crop_name", None)
            )
            crop_date = crop_info.get("hh_member_crop_date" if is_member else "crop_date", None)
            if crop_id:
                crop_info_dict = {"crop": crop_id, "collected_gc": crop_date}

                crop_information_ids.append((0, 0, crop_info_dict))
    return crop_information_ids


def process_livestock_ids(self, json_data, is_member):
    livestock_information_ids = []
    if json_data["livestock_information_ids"] is not None:
        for livestock_info in json_data["livestock_information_ids"]:
            live_type = livestock_info.get("hh_member_animal" if is_member else "animal", None)
            if not live_type:
                continue
            livestock_type = get_value_many2one(self, "g2p.livestock.type", live_type)
            if livestock_type:
                livestock_info_dict = {
                    "livestock_type": livestock_type,
                    "number_of_livestock": livestock_info.get(
                        "hh_member_num_animals" if is_member else "num_animals", None
                    ),
                }

                livestock_information_ids.append((0, 0, livestock_info_dict))
    return livestock_information_ids


def process_reg_ids(self, json_data, id_type_name, id_value_key):
    id_type = self.env["g2p.id.type"].sudo().search([("name", "=", id_type_name)], limit=1)

    if "reg_ids" in json_data:
        json_data["reg_ids"].append(
            (
                0,
                0,
                {
                    "id_type": id_type.id,
                    "value": json_data[id_value_key],
                },
            )
        )
    else:
        json_data["reg_ids"] = [
            (
                0,
                0,
                {
                    "id_type": id_type.id,
                    "value": json_data[id_value_key],
                },
            )
        ]
    return json_data


def patched_handle_one2many_fields(self, mapped_json):
    # skip base module logic
    return


def process_basic_information(self, individual, vals, other_json):
    if individual.get("hh_is_household_head").strip():
        vals["hh_is_household_head"] = individual.get("hh_is_household_head")

    # NATIONAL ID
    vals["has_national_id"] = individual.get("has_national_id")
    if individual.get("has_national_id") == "yes":
        individual = process_reg_ids(self, individual, "UID", "uid")
    elif individual.get("has_national_id") == "no":
        individual = process_reg_ids(self, individual, "RID", "rid")
    vals["reg_ids"] = individual.get("reg_ids")

    # BASIC INFORMATION
    region_id = process_many2one_field(self, "g2p.region", individual.get("region"))
    if region_id:
        if region_id == "other":
            other_json["region"] = individual.get("other_region")
        else:
            vals["region"] = region_id

    zone_id = process_many2one_field(self, "g2p.zone", individual.get("zone"))
    if zone_id:
        if zone_id == "other":
            other_json["zone"] = individual.get("other_zone")
        else:
            vals["zone"] = zone_id

    woreda_id = process_many2one_field(self, "g2p.woreda", individual.get("woreda"))
    if woreda_id:
        if woreda_id == "other":
            other_json["woreda"] = individual.get("other_woreda")
        else:
            vals["woreda"] = woreda_id

    kebele_id = process_many2one_field(self, "g2p.kebele", individual.get("kebele"))
    if kebele_id:
        if kebele_id == "other":
            other_json["kebele"] = individual.get("other_kebele")
        else:
            vals["kebele"] = kebele_id

    language_id = process_many2one_field(self, "g2p.lang", individual.get("primary_Language"))
    if language_id:
        vals["primary_Language"] = language_id

    vals["given_name"] = individual.get("given_name")
    vals["family_name"] = individual.get("family_name")
    vals["gf_name_eng"] = individual.get("gf_name_eng")
    vals["name"] = individual.get("name")
    vals["first_name_amh"] = individual.get("first_name_amh")
    vals["family_name_amh"] = individual.get("family_name_amh")
    vals["gf_name_amh"] = individual.get("gf_name_amh")
    vals["first_name_other"] = individual.get("first_name_other")
    vals["family_name_other"] = individual.get("family_name_other")
    vals["gf_name_other"] = individual.get("gf_name_other")
    vals["gender"] = individual.get("gender")
    vals["birthdate"] = individual.get("birthdate")

    vals["has_personal_phone"] = individual.get("has_personal_phone")
    if "phone_ids" in individual:
        individual = process_phone_ids(self, individual)
        vals["phone_number_ids"] = individual.get("phone_number_ids")

    vals["email"] = individual.get("email")
    vals["is_disabled"] = individual.get("is_disabled")
    vals["farming_type"] = individual.get("farming_type")

    vals["martial_status"] = individual.get("martial_status")
    vals["education"] = individual.get("education")
    source_of_income_ids = process_many2many_field(self, "g2p.hh.income", individual.get("hh_income_type"))
    if source_of_income_ids:
        if "other" in source_of_income_ids:
            other_json["hh_income_type"] = individual.get("other_income_type")
            source_of_income_ids.remove("other")
        vals["hh_income_type"] = [(6, 0, source_of_income_ids)]


def process_membership(self, individual, vals, other_json):
    # MEMBERSHIP
    vals["is_member_of_primary_cooperative"] = individual.get("is_member_of_primary_cooperative")
    vals["is_member_of_cooperative_union"] = individual.get("is_member_of_cooperative_union")
    primary_cooperative_id = process_many2one_field(
        self, "g2p.primary.cooperative", individual.get("primary_cooperatives")
    )
    if primary_cooperative_id:
        if primary_cooperative_id == "other":
            other_json["primary_cooperatives"] = individual.get("other_primary_cooperative")
        else:
            vals["primary_cooperatives"] = primary_cooperative_id

    cooperative_union_id = process_many2one_field(
        self, "g2p.cooperative.union", individual.get("cooperative_unions")
    )
    if cooperative_union_id:
        if cooperative_union_id == "other":
            other_json["cooperative_unions"] = individual.get("other_coop_union")
        else:
            vals["cooperative_unions"] = cooperative_union_id

    vals["is_member_in_farmer_cluster"] = individual.get("is_member_in_farmer_cluster")
    primary_commodity_id = process_many2one_field(
        self, "g2p.primary.commodity", individual.get("primary_commodity")
    )
    if primary_commodity_id:
        vals["primary_commodity"] = primary_commodity_id

    vals["role_in_farmer_cluster"] = individual.get("role_in_farmer_cluster")


def process_land_crop_livestock_information(self, individual, vals, is_member):
    # LAND INFORMATION
    if "land_information_ids" in individual:
        vals["land_information_ids"] = process_land_ids(self, individual, is_member)

    # CROP INFORMATION
    if "crop_information_ids" in individual:
        vals["crop_information_ids"] = process_crop_ids(self, individual, is_member)
    crop_water_sources_ids = process_many2many_field(
        self, "g2p.water.source", individual.get("crop_water_sources")
    )
    if crop_water_sources_ids:
        if "other" in crop_water_sources_ids:
            crop_water_sources_ids.remove("other")
        vals["crop_water_sources"] = [(6, 0, crop_water_sources_ids)]

    # LIVESTOCK INFORMATION
    if "livestock_information_ids" in individual:
        vals["livestock_information_ids"] = process_livestock_ids(self, individual, is_member)
    livestock_water_sources_ids = process_many2many_field(
        self, "g2p.water.source", individual.get("livestock_water_sources")
    )
    if livestock_water_sources_ids:
        if "other" in livestock_water_sources_ids:
            livestock_water_sources_ids.remove("other")
        vals["livestock_water_sources"] = [(6, 0, livestock_water_sources_ids)]


def process_agriculture_resource_finance(self, individual, vals):
    # AGRICULTURAL INPUT
    vals["do_you_use_fertilizer"] = individual.get("do_you_use_fertilizer")
    vals["do_you_use_pesticide"] = individual.get("do_you_use_pesticide")
    vals["do_you_use_insecticide"] = individual.get("do_you_use_insecticide")
    vals["do_you_use_improved_seed"] = individual.get("do_you_use_improved_seed")

    # ACCESS TO RESOURCE
    vals["access_to_machinery"] = individual.get("access_to_machinery")
    if individual.get("access_to_machinery") == "yes":
        type_of_machinery_ids = process_many2many_field(
            self, "g2p.machinery", individual.get("type_of_machinery")
        )
        if type_of_machinery_ids:
            if "other" in type_of_machinery_ids:
                type_of_machinery_ids.remove("other")
            vals["type_of_machinery"] = [(6, 0, type_of_machinery_ids)]

    # ACCESS TO FINANCE
    vals["has_finance_access"] = individual.get("has_finance_access")
    if individual.get("has_finance_access") == "yes":
        finance_accesses_ids = process_many2many_field(
            self, "g2p.finance.access", individual.get("finance_accesses")
        )
        if finance_accesses_ids:
            if "other" in finance_accesses_ids:
                finance_accesses_ids.remove("other")
            vals["finance_accesses"] = [(6, 0, finance_accesses_ids)]


def get_individual_data(self, individual, is_member):
    vals = {
        "is_registrant": True,
        "is_group": False,
        "is_farmer": "yes",
    }
    other_json = {}

    process_basic_information(self, individual, vals, other_json)
    process_membership(self, individual, vals, other_json)
    process_land_crop_livestock_information(self, individual, vals, is_member)
    process_agriculture_resource_finance(self, individual, vals)

    individual = process_reg_ids(self, individual, "Farmer ODK ACK ID", "odk_reference_id")
    vals["reg_ids"] = individual.get("reg_ids")

    if individual.get("member_registered") and individual.get("member_registered") == "yes":
        individual = process_reg_ids(self, individual, "Member ODK ACK ID", "member_reference_id")
        vals["reg_ids"] = individual.get("reg_ids")

    if other_json:
        vals["additional_g2p_info"] = json.dumps(other_json)

    if individual.get("farmer_location") is not None:
        vals["farmer_location_longitude"] = individual.get("farmer_location")["coordinates"][0]
        vals["farmer_location_latitude"] = individual.get("farmer_location")["coordinates"][1]

    if individual.get("supporting_documents_ids") is not None:
        vals["supporting_documents_ids"] = individual.get("supporting_documents_ids")

    return vals


def get_member_data(self, member, head):
    vals = {"is_registrant": True, "is_group": False, "is_farmer": "no", "hh_is_household_head": "no"}

    first_name, family_name, gf_name_eng = member.get("name").split()
    vals["given_name"] = first_name
    vals["family_name"] = family_name
    vals["gf_name_eng"] = gf_name_eng
    vals["name"] = member.get("name")
    if member.get("name_amharic") and member.get("name_amharic").strip():
        fn, mn, ln = member.get("name_amharic").split()
        vals["first_name_amh"] = fn
        vals["family_name_amh"] = mn
        vals["gf_name_amh"] = ln
    if member.get("name_other") and member.get("name_other").strip():
        fn, mn, ln = member.get("name_other").split()
        vals["first_name_other"] = fn
        vals["family_name_other"] = mn
        vals["gf_name_other"] = ln
    vals["gender"] = member.get("gender")
    vals["birthdate"] = member.get("birthdate")

    region_id = process_many2one_field(self, "g2p.region", head.get("region"))
    if region_id:
        if region_id != "other":
            vals["region"] = region_id

    zone_id = process_many2one_field(self, "g2p.zone", head.get("zone"))
    if zone_id:
        if zone_id != "other":
            vals["zone"] = zone_id

    woreda_id = process_many2one_field(self, "g2p.woreda", head.get("woreda"))
    if woreda_id:
        if woreda_id != "other":
            vals["woreda"] = woreda_id

    kebele_id = process_many2one_field(self, "g2p.kebele", head.get("kebele"))
    if kebele_id:
        if kebele_id != "other":
            vals["kebele"] = kebele_id

    return vals


def get_membership_kind(self, relationship):
    if relationship == "Wife":
        relationship = "Wife - Head"
    if relationship == "Husband":
        relationship = "Husband - Head"

    membership_kind = (
        self.env["g2p.group.membership.kind"].sudo().search([("name", "=", relationship)], limit=1)
    )
    if not membership_kind:
        membership_kind = self.env["g2p.group.membership.kind"].sudo().create({"name": relationship})
    return membership_kind.id


def patched_addl_data(self, mapped_json):
    # return []
    # PROCESS FLOW
    """
    hhh = household head
    1. if hhh is coming:
        we register hhh with members and give hhh the ack id
        we ask if a member of his household has already registered:
            if yes:
                take the member ack id
                link the member to the new household that is going to be created

    2. if member is coming:
         we register member and give his ack id
         we ask if the hhh has already registered:
         if yes:
             take the hhh ack id
             link the new member to the existing household of the hhh
    """

    if mapped_json["hh_is_household_head"] == "yes":
        group = {
            "is_registrant": True,
            "is_group": True,
        }
        individual_ids = []
        # Get head name for household name
        household_head_name = mapped_json.get("name")
        additional_farmers = mapped_json.get("additional_farmers")
        other_household_members = mapped_json.get("other_household_members")

        # Create household head
        individual_data = get_individual_data(self, mapped_json, False)
        household_head = self.env["res.partner"].sudo().create(individual_data)
        membership_kind = get_membership_kind(self, "Head")
        individual_ids.append((0, 0, {"individual": household_head.id, "kind": [(4, membership_kind)]}))

        # OTHER HOUSEHOLD MEMBERS WHO ARE FARMERS
        if additional_farmers is not None:
            for additional_farmer in additional_farmers:
                addl_farmer_data = get_individual_data(self, additional_farmer, True)
                addl_farmer = self.env["res.partner"].sudo().create(addl_farmer_data)
                membership_kind = get_membership_kind(self, "Member")
                individual_ids.append((0, 0, {"individual": addl_farmer.id, "kind": [(4, membership_kind)]}))

        # OTHER HOUSEHOLD MEMBERS WHO ARE NOT FARMERS
        if other_household_members is not None:
            for other_household_member in other_household_members:
                other_member_data = get_member_data(self, other_household_member, mapped_json)
                other_member = self.env["res.partner"].sudo().create(other_member_data)
                membership_kind = get_membership_kind(self, other_household_member["household_relationship"])
                individual_ids.append((0, 0, {"individual": other_member.id, "kind": [(4, membership_kind)]}))

        # LINK OTHER FARMER USING REFERENCE ID
        if mapped_json.get("member_registered") == "yes":
            member_reference_id = mapped_json.get("member_reference_id")

            # Search for the farmer that has this ID under "Farmer ODK ACK ID"
            odk_ack_id_type = (
                self.env["g2p.id.type"].sudo().search([("name", "=", "Farmer ODK ACK ID")], limit=1)
            )
            other_farmer = (
                self.env["res.partner"]
                .sudo()
                .search(
                    [
                        (
                            "reg_ids",
                            "in",
                            self.env["g2p.reg.id"]
                            .sudo()
                            .search(
                                [("id_type", "=", odk_ack_id_type.id), ("value", "=", member_reference_id)]
                            )
                            .ids,
                        )
                    ],
                    limit=1,
                )
            )

            if other_farmer:
                membership_kind = get_membership_kind(self, "Member")
                individual_ids.append((0, 0, {"individual": other_farmer.id, "kind": [(4, membership_kind)]}))
            else:
                # Filter household_head.reg_ids to find the specific ID with
                # "Member ODK ACK ID" and the member_reference_id
                head_reg_id = household_head.reg_ids.filtered(
                    lambda r: r.id_type.name == "Member ODK ACK ID" and r.value == member_reference_id
                )
                # Update the status to 'invalid' and add the description
                head_reg_id.sudo().write(
                    {"status": "invalid", "description": "Farmer with this ACK ID not found"}
                )

        group_kind = self.env["g2p.group.kind"].sudo().search([("name", "=", "Household")], limit=1)
        if not group_kind:
            group_kind = self.env["g2p.group.kind"].sudo().create({"name": "Household"})

        group["name"] = "Household - " + household_head_name
        group["kind"] = group_kind.id
        group["region"] = household_head.region.id
        group["zone"] = household_head.zone.id
        group["woreda"] = household_head.woreda.id
        group["kebele"] = household_head.kebele.id
        group["group_membership_ids"] = individual_ids

        return group
    else:
        individual_data = get_individual_data(self, mapped_json, False)
        if mapped_json.get("member_registered") == "yes":
            member_reference_id = mapped_json.get("member_reference_id")
            # Search for the head farmer that has this ID under "Farmer ODK ACK ID"
            odk_ack_id_type = (
                self.env["g2p.id.type"].sudo().search([("name", "=", "Farmer ODK ACK ID")], limit=1)
            )
            head = (
                self.env["res.partner"]
                .sudo()
                .search(
                    [
                        (
                            "reg_ids",
                            "in",
                            self.env["g2p.reg.id"]
                            .sudo()
                            .search(
                                [("id_type", "=", odk_ack_id_type.id), ("value", "=", member_reference_id)]
                            )
                            .ids,
                        )
                    ],
                    limit=1,
                )
            )

            if head:
                # Add the new individual farmer to the household the head belongs to
                group_membership_ids = head.individual_membership_ids
                household = group_membership_ids.group
                membership_kind = get_membership_kind(self, "Member")
                individual_data["individual_membership_ids"] = [
                    (0, 0, {"group": household.id, "kind": [(4, membership_kind)]})
                ]
            else:
                reg_ids = individual_data.get("reg_ids")
                # Find the ID type with the name 'Member ODK ACK ID'
                odk_member_ack_id_type = (
                    self.env["g2p.id.type"].sudo().search([("name", "=", "Member ODK ACK ID")], limit=1)
                )
                for reg_id in reg_ids:
                    # Check if the id_type.id and value match
                    if (
                        reg_id[2].get("id_type") == odk_member_ack_id_type.id
                        and reg_id[2].get("value") == member_reference_id
                    ):
                        # Add the status and description to the matching entry
                        reg_id[2].update(
                            {"status": "invalid", "description": "Head farmer with this ACK ID not found"}
                        )
                        break  # Exit the loop once the matching entry is found and updated
                individual_data["reg_ids"] = reg_ids

        return individual_data


def handle_media_import_ati(self, member, mapped_json):
    # return
    meta = member.get("meta")
    if not meta:
        return

    instance_id = meta.get("instanceID")
    if not instance_id:
        return

    exit_attachment = self.list_expected_attachments(
        self.base_url, self.project_id, self.form_id, instance_id, self.session
    )
    if not exit_attachment:
        return

    doc_tag = self.env["g2p.document.tag"].get_tag_by_name("Land Certificate")
    if not doc_tag:
        doc_tag = self.env["g2p.document.tag"].create({"name": "Land Certificate"})

    first_image_stored = False
    supporting_documents_ids = []

    # file ids to keep track of which document id is for which
    # land certificate (to map to land certificate in land information later)
    file_ids = []
    for attachment in exit_attachment:
        filename = attachment["name"]
        get_attachment = self.download_attachment(
            self.base_url, self.project_id, self.form_id, instance_id, filename, self.session
        )
        attachment_base64 = base64.b64encode(get_attachment).decode("utf-8")
        image_verify = self.is_image(filename)

        if not first_image_stored and image_verify and "image_1920" in mapped_json:
            mapped_json["image_1920"] = attachment_base64
            first_image_stored = True
        else:
            backend_id = (
                self.env.ref("storage_backend.default_storage_backend").id
                or self.env["storage.backend"].search([], limit=1).id
            )
            storage_file = (
                self.env["storage.file"]
                .sudo()
                .create(
                    {
                        "name": filename,
                        "backend_id": backend_id,
                        "data": attachment_base64,
                        "tags_ids": [(4, doc_tag.id)],
                    }
                )
            )
            if storage_file:
                supporting_documents_ids.append((4, storage_file.id))
                file_ids.append([filename, storage_file.id])

    if supporting_documents_ids:
        mapped_json["supporting_documents_ids"] = supporting_documents_ids
    mapped_json["file_ids"] = file_ids


base_odk_client.ODKClient.handle_media_import = handle_media_import_ati
base_odk_client.ODKClient.get_addl_data = patched_addl_data
base_odk_client.ODKClient.handle_one2many_fields = patched_handle_one2many_fields
