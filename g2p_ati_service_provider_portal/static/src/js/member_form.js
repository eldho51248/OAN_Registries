// Date restriction
$(document).ready(function () {
    $(".date-picker").each(function () {
        var input = this;
        var today = new Date().toISOString().split("T")[0];
        input.setAttribute("max", today);
    });
});

// eslint-disable-next-line no-unused-vars
function validateForm(isCreateForm) {
    // Var requiredFields = document.querySelectorAll(".s_website_form_field [required]");
    // var isValid = true;

    // requiredFields.forEach(function (field) {
    //     var existingErrorMessage = field.parentNode.querySelector(".error-message");
    //     if (!field.value.trim()) {
    //         var errorMessage = document.createElement("span");
    //         errorMessage.className = "error-message";
    //         errorMessage.textContent = "This field is required";
    //         errorMessage.style.color = "red";

    //         if (existingErrorMessage) {
    //             field.parentNode.replaceChild(errorMessage, existingErrorMessage);
    //         } else {
    //             field.parentNode.insertBefore(errorMessage, field.nextSibling);
    //         }

    //         field.style.border = "1px solid red";
    //         isValid = false;
    //         const collapseElement = field.closest(".collapse");
    //         if (collapseElement) {
    //             const accordionButton = document.querySelector(`[data-bs-target="#${collapseElement.id}"]`);
    //             if (accordionButton) {
    //                 accordionButton.click();
    //             }
    //         }
    //     } else {
    //         if (existingErrorMessage) {
    //             existingErrorMessage.parentNode.removeChild(existingErrorMessage);
    //         }
    //         field.style.border = "";
    //     }
    // });
    var isValid = true;

    if (isValid && isCreateForm) {
        document.getElementById("creategroupForm").submit();
    } else if (isValid && !isCreateForm) {
        document.getElementById("updategroupForm").submit();
    }
}

// eslint-disable-next-line no-unused-vars
function validateFormGroup(isCreateForm) {
    var isValid = true;

    if (isValid && isCreateForm) {
        document.getElementById("createhouseholdForm").submit();
    } else if (isValid && !isCreateForm) {
        document.getElementById("updatehouseholdForm").submit();
    }
}

function showToast(message) {
    const toast_message = $("#memberDetailModal #toast-message");
    toast_message.text(message);
    const toast_container = $("#memberDetailModal #toast-container");
    toast_container.css("display", "block");
}

// eslint-disable-next-line no-unused-vars
function hideToast() {
    const toast_container = $("#memberDetailModal #toast-container");
    toast_container.css("display", "none");
}

function resetFormFields() {
    // Reset text inputs, email, and password fields
    $(
        "#farmerDetailModal input[type='text'], #farmerDetailModal input[type='email'], #farmerDetailModal input[type='password']"
    ).val("");

    // Uncheck checkboxes and radio buttons
    $("#farmerDetailModal input[type='checkbox'], #farmerDetailModal input[type='radio']").prop(
        "checked",
        false
    );

    // Reset select dropdowns to the first option
    $("#farmerDetailModal select").prop("selectedIndex", 0).trigger("change");

    // Clear multi-select fields
    $("#farmerDetailModal select[multiple]").val([]).trigger("change");

    // Reset number and date fields to their default state
    $("#farmerDetailModal input[type='number'], #farmerDetailModal input[type='date']").val("");
}

// eslint-disable-next-line no-unused-vars
function resetFormFieldsMember() {
    $("#familyMemberModal input, #familyMemberModal select").val("");
}

// Replace button
$('[data-bs-target="#memberDetailModal"]').on("click", function () {
    $("#update-member-btn").replaceWith(
        '<div id="member_submit" type="button" class="btn btn-primary create-new">Add</div>'
    );
    resetFormFields();
});

$(document).on("click", "#member_submit", async function () {
    console.log("Add memberrrrrr clicked");

    var additional_info = {};

    var group = $("input[name='group_id']").val();
    
    var region = document.getElementById("region_selection").value;
    var zone = document.getElementById("zon_selection").value;
    console.log(zone);
    var woreda = document.getElementById("woreda_selection").value;

    var kebele = document.getElementById("kebele_selection").value;

    var other_woreda = "";
    var other_kebele = "";

    var woredaText = $("#woreda_selection option:selected").text().trim().toLowerCase();

    var kebeleText = $("#kebele_selection option:selected").text().trim().toLowerCase();

    // Check for "other" or "others" in the text of primary_coop and coop_union
    if (woredaText === "other" || woredaText === "others") {
        other_woreda = $("#other_woreda").val();
        additional_info.Woreda = other_woreda;
    }

    if (kebeleText === "other" || kebeleText === "others") {
        other_kebele = $("#other_kebele").val();
        additional_info.Kebele = other_kebele;
    }

    var isHouseholdHead = document.getElementById("hh_is_household_head_id").value;
    var hasNationalId = document.getElementById("have-national-id-selection").value;
    var hasNationalIdCheck = document.getElementById("have-national-id-selection");
    const selectedIDOptionText = hasNationalIdCheck.options[hasNationalIdCheck.selectedIndex].text
        .trim()
        .toLowerCase();
    var uid = document.getElementById("uid_input").value;
    var rid = document.getElementById("rid_input").value;
    var selectedId = null;

    if (selectedIDOptionText === "yes") {
        selectedId = uid;
    } else if (selectedIDOptionText === "no") {
        selectedId = rid;
    }
    var primaryLanguage = document.getElementById("primary_language").value;
    var firstName = $("#farmerDetailModal #given_name").val();
    var middleName = $("#farmerDetailModal #family_name").val();
    var lastName = $("#farmerDetailModal #gf_name_eng").val();
    var firstNameAmh = $("#farmerDetailModal #first_name_amh").val();
    var familyNameAmh = $("#farmerDetailModal #family_name_amh").val();
    var gFNameAmh = $("#farmerDetailModal #gf_name_amh").val();
    var firstNameOther = $("#farmerDetailModal #first_name_other").val();
    var familyNameOther = $("#farmerDetailModal #family_name_other").val();
    var lastNameOther = $("#farmerDetailModal #gf_name_other").val();
    var dob = $("#farmerDetailModal #birthdate").val();
    var gender = document.querySelector('input[name="farmer_gender"]:checked').value;
    console.log(gender);

    var havePhoneNumber = document.getElementById("have-phone-no-selection").value;

    var primaryPhoneNumber = document.getElementById("primary_phone").value;
    var secondaryPhoneNumber = document.getElementById("secondary_phone").value;
    var otherPhoneNumber = document.getElementById("other_phone").value;
    var email = document.getElementById("email").value;
    var isDisabled = document.getElementById("is_disabled").value;
    var farmingType = document.getElementById("farming-type-selection").value;
    var maritalStatus = document.getElementById("marital-status-selection").value;
    var educationLevel = document.getElementById("education-level-selection").value;
    var isMemberOfPrimaryCoop = document.getElementById("is_member_of_primary_coop").value;
    var nameOfPrimaryCoop = document.getElementById("name_of_primary_coop").value;
    var isMemberOfCoopUnion = $("#farmerDetailModal #is_member_of_coop_union").val();
    var nameOfCoopUnion = document.getElementById("name_of_coop_union").value;
    var inFarmerCluster = document.getElementById("in_farmer_cluster").value;
    var primaryComodity = document.getElementById("primary_commodity").value;
    var roleInCluster = document.getElementById("role_in_cluster").value;


    
    var usedFertilizer = document.getElementById("have-used-fertilizer-selection").value;
    var usedInsecticide = document.getElementById("have-used-insecticide-selection").value;
    var usedPesticide = document.getElementById("have-used-pesticide-selection").value;
    var usedImprovedSeed = document.getElementById("have-used-improved-seed-selection").value;

    var accessToMachinary = document.getElementById("access-to-machinery-selection").value;
    var matchinaryTypes = $("#farmerDetailModal #machinery-types-select").val();

   

    var accessToFinance = document.getElementById("access-to-finance-selection").value;
    var financialSectors = $("#farmerDetailModal #finance-selection").val();

    var incomeType = $("#farmerDetailModal #hh_income_type").val();

    var other_income_type = "";
    var incomeTypeText = $("#farmerDetailModal #hh_income_type option:selected")
        .map(function () {
            return $(this).text().trim();
        })
        .get();

    if (incomeTypeText.some((type) => type.toLowerCase() === "other" || type.toLowerCase() === "others")) {
        other_income_type = $("#farmerDetailModal #other_modal_income").val();
        additional_info["Household Income"] = other_income_type;
    }

    var other_primary_coop = "";
    var other_coop_union = "";

    var primaryCoopText = $("#farmerDetailModal #name_of_primary_coop option:selected")
        .text()
        .trim()
        .toLowerCase();
    var coopUnionText = $("#farmerDetailModal #name_of_coop_union option:selected")
        .text()
        .trim()
        .toLowerCase();

    // Check for "other" or "others" in the text of primary_coop and coop_union
    if (primaryCoopText === "other" || primaryCoopText === "others") {
        other_primary_coop = $("#farmerDetailModal #other_primary_coop").val();
        additional_info["Primary Cooperative"] = other_primary_coop;
    }

    if (coopUnionText === "other" || coopUnionText === "others") {
        other_coop_union = $("#farmerDetailModal #other_coop_union").val();
        additional_info["Cooperative Union"] = other_coop_union;
    }

    var cropWaterSource = $("#farmerDetailModal #crop_water_source").val();
    var livestockWaterSource = $("#farmerDetailModal #livestock_water_source").val();
    // Var isValid = true;
    var modal = $("#farmerDetailModal");

    // Function to read file as Base64 string
    function readFileAsBase64(input) {
        return new Promise((resolve, reject) => {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    const base64String = event.target.result.split(",")[1];
                    resolve(base64String);
                };
                reader.onerror = function (error) {
                    reject(error);
                };
                reader.readAsDataURL(file);
            } else {
                resolve(null);
            }
        });
    }

    async function collectLandRecords() {
        const landRecords = [];
        const landSections = $(".land-section-wrapper");

        for (let i = 0; i < landSections.length; i++) {
            const section = landSections[i];
            const record = {};
            const index = $(section).data("index");

            record[`ownership_type_${index}`] = $(section)
                .find(`select[name="land_ownership_type_${index}"]`)
                .val();
            record[`total_land_area_${index}`] = $(section)
                .find(`input[name="total_land_area_${index}"]`)
                .val();
            record[`land_id_${index}`] = $(section).find(`input[name="land_id_${index}"]`).val();

            const landCertificateInput = $(section).find(`input[name="land_certificate_${index}"]`)[0];

            // Wait for the file to be read and then add it to the record
            try {
                const landCertificate = await readFileAsBase64(landCertificateInput);
                if (landCertificate) {
                    record[`land_certificate_${index}`] = {
                        filename: landCertificateInput.files[0].name,
                        content: landCertificate,
                    };
                }
            } catch (error) {
                console.error("Error reading file:", error);
            }

            landRecords.push(record);
        }

        return landRecords;
    }

    // Invoke the async function to collect land records
    var landRecords = await collectLandRecords();
    console.log(landRecords);

    const cropRecords = [];

    $(".crop-section-wrapper").each(function () {
        const record = {};
        const index = $(this).data("index");

        record[`crops_${index}`] = $(this).find(`select[name="crops_${index}"]`).val();
        // For file inputs, you can either send the file directly or handle it differently if neede
        cropRecords.push(record);
    });

    const livestockRecord = [];

    $(".livestock-section-wrapper").each(function () {
        const record = {};
        const index = $(this).data("index");

        record[`livestock_types_${index}`] = $(this).find(`select[name="livestock_types_${index}"]`).val();
        record[`number_of_livestock_${index}`] = $(this)
            .find(`input[name="number_of_livestock_${index}"]`)
            .val();
        // For file inputs, you can either send the file directly or handle it differently if neede
        // if (Object.keys(record).length > 0 && record.constructor === Object) {
        //     livestockRecord.push(record);
        // }
        livestockRecord.push(record);
    });
    // Console.log("LIVESTOCK", livestockRecord);
    //    Var landRecords = JSON.stringify(landRecords)

    $(".form-control, .form-select").removeClass("is-invalid");

    console.log(`here is the group: ${group}`)



    $.ajax({
        url: "/serviceprovider/individual/create/",
        method: "POST",
        data: {
            landRecords: JSON.stringify(landRecords),
            cropRecords: JSON.stringify(cropRecords),
            livestockRecord: JSON.stringify(livestockRecord),
            newIncomeType: JSON.stringify(incomeType),
            cropWaterSource: JSON.stringify(cropWaterSource),
            livestockWaterSource: JSON.stringify(livestockWaterSource),
            matchinaryTypes: JSON.stringify(matchinaryTypes),
            financialSectors: JSON.stringify(financialSectors),
            additional_info: JSON.stringify(additional_info),
            group_id: group,
            region: region,
            zone: zone,
            woreda: woreda,
            kebele: kebele,
            isHouseholdHead: isHouseholdHead,
            hasNationalId: hasNationalId,
            selectedId: selectedId,
            primaryLanguage: primaryLanguage,
            given_name: firstName,
            family_name: middleName,
            gf_name_eng: lastName,
            firstNameAmh: firstNameAmh,
            familyNameAmh: familyNameAmh,
            gFNameAmh: gFNameAmh,
            firstNameOther: firstNameOther,
            familyNameOther: familyNameOther,
            lastNameOther: lastNameOther,
            dob: dob,
            gender: gender,
            havePhoneNumber: havePhoneNumber,
            primaryPhoneNumber: primaryPhoneNumber,
            secondaryPhoneNumber: secondaryPhoneNumber,
            otherPhoneNumber: otherPhoneNumber,
            email: email,
            isDisabled: isDisabled,
            farmingType: farmingType,
            maritalStatus: maritalStatus,
            educationLevel: educationLevel,
            isMemberOfPrimaryCoop: isMemberOfPrimaryCoop,
            nameOfPrimaryCoop: nameOfPrimaryCoop,
            isMemberOfCoopUnion: isMemberOfCoopUnion,
            nameOfCoopUnion: nameOfCoopUnion,
            inFarmerCluster: inFarmerCluster,
            primaryComodity: primaryComodity,
            roleInCluster: roleInCluster,
            usedFertilizer: usedFertilizer,
            usedInsecticide: usedInsecticide,
            usedPesticide: usedPesticide,
            usedImprovedSeed: usedImprovedSeed,
            accessToMachinary: accessToMachinary,
            accessToFinance: accessToFinance,
        },
        dataType: "json",
        success: function (response) {
            console.log("Ajax request successful");
            console.log("Response:", response);
            if (response.member_list) {
                var member_list = response.member_list;
                if (member_list) {
                    resetFormFields();
                    modal.modal("hide");
                    console.log("member_list[0].group_id :", member_list[0].group_id);
                    $("input[name='group_id']").val(member_list[0].group_id);
                    $(".no_list").css("display", "none");

                    var tableBody = $("#memberlist tbody");
                    tableBody.empty();
                    $(".old-list").css("display", "none");

                    member_list.forEach(function (member, index) {
                        $(".mem-list").css("display", "block");
                        var serialNumber = index + 1;
                        var newRowHtml = `
                            <tr data-member-id="${member.id}">
                            <td>${serialNumber}</td>
                            <td style="color:#704880; font: normal normal 600 13px/16px Inter;">${member.name}</td>
                            <td>${member.age}</td>
                            <td>${member.gender}</td>
                            <td>${member.relationship}</td>

                            <td>
                                 <a href="/serviceprovider/individual/update/${member.id}" class="btn btn-icon rounded-0 edit-btn" title="Edit">
                                    <i class="fa fa-pencil"></i>
                                </a>
                                <button type="button" class="btn btn-outline-secondary btn-sm my-3" onclick="deleteMember(this)">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </td>
                            </tr>
                            `;
                        tableBody.append(newRowHtml);
                    });
                }
            } else {
                console.error("Failed to create individual");
            }
        },
        error: function (error) {
            console.error("request failed");
            console.error("Error:", error);
        },
    });
});

// Edit Icon
$(document).on("click", "#mem-update", function () {
    var memberId = $(this).attr("store");
    var modal = $("#memberDetailModal");
    $.ajax({
        url: "/serviceprovider/member/update/",
        method: "POST",
        data: {
            member_id: memberId,
        },
        dataType: "json",
        success: function (response) {
            modal.find("#given_name").val(response.given_name);
            modal.find("#addl_name").val(response.addl_name);
            modal.find("#family_name").val(response.family_name);
            modal.find("#birthdate").val(response.dob);
            modal.find('select[name="gender"]').val(response.gender);

            $("#member_submit").replaceWith(
                '<div id="update-member-btn" store="' +
                    memberId +
                    '" class="btn btn-primary create-new">Update</div>'
            );

            modal.modal("show");
        },
        error: function (error) {
            console.error("Ajax request failed");
            console.error("Error:", error);
        },
    });
});

$(document).on("click", "#update-member-btn", function () {
    // Get the member ID
    var memberId = $(this).attr("store");

    var group = $("input[name='group_id']").val();
    var firstName = $("#memberDetailModal #given_name").val();
    var middleName = $("#memberDetailModal #addl_name").val();
    var lastName = $("#memberDetailModal #family_name").val();
    var dob = $("#memberDetailModal #birthdate").val();
    var gender = $('#memberDetailModal select[name="gender"]').val();
    var isValid = true;

    $(".form-control, .form-select").removeClass("is-invalid");

    if (!firstName || !lastName || !gender) {
        isValid = false;
        $("#memberDetailModal .form-control, #memberDetailModal .form-select").each(function () {
            if (!$(this).val().trim()) {
                $(this).addClass("is-invalid");
            }
        });
    }

    if (!isValid) {
        showToast("Please fill out all required fields.");
        return;
    }

    $.ajax({
        url: "/serviceprovider/member/update/submit/",
        method: "POST",
        data: {
            group_id: group,
            member_id: memberId,
            given_name: firstName,
            addl_name: middleName,
            family_name: lastName,
            birthdate: dob,
            gender: gender,
        },
        dataType: "json",
        success: function (response) {
            if (response && response.member_list) {
                var member_list = response.member_list;
                $("#memberDetailModal").modal("hide");

                var tableBody = $("#memberlist tbody");
                tableBody.empty();

                member_list.forEach(function (member, index) {
                    var serialNumber = index + 1;
                    var newRowHtml =
                        "<tr>" +
                        "<td>" +
                        serialNumber +
                        "</td>" +
                        '<td style="color:#704880; font: normal normal 600 13px/16px Inter;">' +
                        member.name +
                        "</td>" +
                        "<td>" +
                        member.age +
                        "</td>" +
                        "<td>" +
                        member.gender +
                        "</td>" +
                        "<td>" +
                        "dependent" +
                        "</td>" +
                        "<td>" +
                        '<div class="active-button">' +
                        (member.active ? "Active" : "Inactive") +
                        "</div>" +
                        "</td>" +
                        "<td>" +
                        '<button class="btn btn-icon rounded-0" id="mem-update" store="' +
                        member.id +
                        '" title="Edit">' +
                        '<i class="fa fa-pencil"></i>' +
                        "</button>" +
                        "</td>" +
                        "</tr>";
                    tableBody.append(newRowHtml);
                });
            } else {
                console.error("FINAL Member list not found in the response.");
            }
        },

        error: function (error) {
            console.error("Error:", error);
        },
    });
});

document.addEventListener("DOMContentLoaded", function () {
    function checkOthersOption(selectElementId, otherFieldId) {
        const selectElement = document.getElementById(selectElementId);
        const otherField = document.getElementById(otherFieldId);

        if (!selectElement || !otherField) {
            console.error(`Element with ID ${selectElementId} or ${otherFieldId} not found.`);
            return;
        }

        function toggleOtherField() {
            const selectedOptions = Array.from(selectElement.selectedOptions);
            const hasOthers = selectedOptions.some((option) => {
                const optionText = option.textContent.trim().toLowerCase();
                return optionText === "other" || optionText === "others";
            });

            if (hasOthers) {
                otherField.style.display = "block";
            } else {
                otherField.style.display = "none";
                // Clear the input field when hidden
                const input = otherField.querySelector("input");
                if (input) input.value = "";
            }
        }

        selectElement.addEventListener("change", toggleOtherField);
        // Initial check on page load
        toggleOtherField();
    }

    function hideFieldOnNo(radioButtonsName, fieldId, selectElementId) {
        const radioButtons = document.querySelectorAll(`input[name="${radioButtonsName}"]`);
        const field = document.getElementById(fieldId);
        const selectElement = document.getElementById(selectElementId);

        if (!radioButtons || !field || !selectElement) {
            console.error(
                `Element with name ${radioButtonsName}, ID ${fieldId}, or select ${selectElementId} not found.`
            );
            return;
        }

        function handleToggle() {
            const selectedRadio = Array.from(radioButtons).find((radioButton) => radioButton.checked);
            if (selectedRadio && selectedRadio.dataset.text === "No") {
                field.style.display = "none";
                selectElement.style.display = "none";

                // Clear the field values when "No" is selected
                field.querySelectorAll("input").forEach((input) => (input.value = ""));
                selectElement.querySelector("select").selectedIndex = 0; // Reset the select field
            } else {
                field.style.display = "block";
                selectElement.style.display = "block";
                // Call checkOthersOption if the field is displayed
                checkOthersOption("name_of_primary_coop", "otherPrimaryCoopField");
                checkOthersOption("name_of_coop_union", "otherCoopUnionField");
            }
        }

        // Initial check on page load
        handleToggle();

        // Add event listeners for change
        radioButtons.forEach(function (radioButton) {
            radioButton.addEventListener("change", handleToggle);
        });
    }

    // For primary cooperative and cooperative union handling both "No" and "Other" logic
    hideFieldOnNo("is_member_of_primary_coop", "otherPrimaryCoopField", "primary-coop-field");
    hideFieldOnNo("is_member_of_coop_union", "otherCoopUnionField", "coop-union-field");

    // For other fields that need the "other" option handling
    checkOthersOption("name_of_primary_coop", "otherPrimaryCoopField");
    checkOthersOption("name_of_coop_union", "otherCoopUnionField");
    checkOthersOption("incomeTypeSelect", "otherIncomeField");
    checkOthersOption("woreda_selection", "otherWoredaField");
    checkOthersOption("kebele_selection", "otherKebeleField");
});

// Modal other fields
document.addEventListener("DOMContentLoaded", function () {
    // Function to handle the display of the 'Other' field for Woreda and Kebele

    function handleOtherFields(selectElementId, otherFieldId) {
        const selectElement = document.getElementById(selectElementId);
        const otherField = document.getElementById(otherFieldId);
        const hasOthers = Array.from(selectElement.selectedOptions).some(
            (option) =>
                option.textContent.trim().toLowerCase() === "other" ||
                option.textContent.trim().toLowerCase() === "others"
        );
        if (!selectElement) {
            console.error(`Element with ID ${selectElementId} not found.`);
            return;
        }

        if (!otherField) {
            console.error(`Other field with ID ${otherFieldId} not found.`);
            return;
        }

        if (hasOthers) {
            otherField.style.display = "block";
        } else {
            console.log("hiiii");
            otherField.style.display = "none";
        }
    }

    // Event listener for each select element change
    document.getElementById("woreda_selection").addEventListener("change", function () {
        handleOtherFields("woreda_selection", "otherModalWoredaField");
    });

    document.getElementById("kebele_selection").addEventListener("change", function () {
        handleOtherFields("kebele_selection", "otherModalKebeleField");
    });

    document.getElementById("hh_income_type").addEventListener("change", function () {
        handleOtherFields("hh_income_type", "otherModalIncomeField");
    });

    document.getElementById("name_of_primary_coop").addEventListener("change", function () {
        handleOtherFields("name_of_primary_coop", "otherModalPrimaryCoopField");
    });

    document.getElementById("name_of_coop_union").addEventListener("change", function () {
        handleOtherFields("name_of_coop_union", "otherModalCoopUnionField");
    });

    handleOtherFields("woreda_selection", "otherModalWoredaField");
    handleOtherFields("kebele_selection", "otherModalKebeleField");

    // Initial check when the modal is shown
    $("#farmerDetailModal").on("shown.bs.modal", function () {
        handleOtherFields("hh_income_type", "otherModalIncomeField");
        handleOtherFields("name_of_primary_coop", "otherModalPrimaryCoopField");
        handleOtherFields("name_of_coop_union", "otherModalCoopUnionField");
    });
});

// $(document).on("click", "#family_member_submit", function () {
//     var group = $("input[name='group_id']").val();

//     var group_id = $("input[name='group_id']").val();
//     var firstName = $("#mamber_given_name").val();
//     var middleName = $("#member_fathers_name").val();
//     var lastName = $("#member_grandfathers_name").val();
//     var dob = $("#member-birthdate").val();
//     var gender = $("input[name='gender']:checked").val();
//     var gender = $("#familyMemberModal input[name='gender']:checked").val();
//     var relationship =$("select[name='relation_with_household_head_add']").val();

//     console.log(relationship);
//     // var firstName = $("#familyMemberModal #mamber_given_name").val();
//     // var middleName = $("#familyMemberModal #addl_name").val();
//     // var lastName = $("#familyMemberModal #family_name").val();
//     // var dob = $("#familyMemberModal #birthdate").val();
//     // var gender = $('#familyMemberModal select[name="gender"]').val();
//     // var relationship = $('#familyMemberModal select[name="relationship"]').val();
//     var isValid = true;
//     var modal = $("#familyMemberModal");

//     $(".form-control, .form-select").removeClass("is-invalid");

//     if (!firstName || !lastName || !gender || !dob) {
//         console.log("empty");
//         isValid = false;
//         $("#memberDetailModal .form-control[required], #memberDetailModal .form-select[required]").each(
//             function () {
//                 if (!$(this).val()) {
//                     $(this).addClass("is-invalid");
//                 }
//             }
//         );
//     }

//     if (!isValid) {
//         showToast("Please fill out all required fields.");
//         return;
//     }

//      if (!group) {
//         showToast("Please Create The Farmer First");
//         return;
//     }

//     $.ajax({
//         url: "/serviceprovider/member/create/",
//         method: "POST",
//         data: {
//             group_id: group,
//             given_name: firstName,
//             family_name: middleName,
//             addl_name: lastName,
//             dob: dob,
//             gender: gender,
//             relationship: relationship,
//         },
//         dataType: "json",
//         success: function (response) {
//             console.log("Ajax request successful");
//             console.log("Response:", response);
//             if (response.member_list) {
//                 var member_list = response.member_list;
//                 if (member_list) {
//                     resetFormFieldsMember();
//                     modal.modal("hide");
//                     console.log("member_list[0].group_id :", member_list[0].group_id);
//                     $("input[name='group_id']").val(member_list[0].group_id);
//                     $(".no_list").css("display", "none");

//                     var tableBody = $("#familylist tbody");
//                     tableBody.empty();
//                     $(".old-list").css("display", "none");

//                     member_list.forEach(function (member, index) {
//                         $(".mem-list").css("display", "block");
//                         var serialNumber = index + 1;
//                         var newRowHtml =
//                             "<tr>" +
//                             "<td>" +
//                             serialNumber +
//                             "</td>" +
//                             '<td style="color:#704880; font: normal normal 600 13px/16px Inter;">' +
//                             member.name +
//                             "</td>" +
//                             "<td>" +
//                             member.age +
//                             "</td>" +
//                             "<td>" +
//                             member.gender +
//                             "</td>" +
//                             "<td>" +
//                             "dependent" +
//                             "</td>" +
//                             "<td>" +
//                             '<div class="active-button">' +
//                             (member.active ? "Active" : "Inactive") +
//                             "</div>" +
//                             "</td>" +
//                             "<td>" +
//                             '<button class="btn btn-icon rounded-0" id="mem-update" store="' +
//                             member.id +
//                             '" title="Edit">' +
//                             '<i class="fa fa-pencil"></i>' +
//                             "</button>" +
//                             "</td>" +
//                             "</tr>";

//                         tableBody.append(newRowHtml);
//                     });
//                 }
//             } else {
//                 console.error("Failed to create individual");
//             }
//         },
//         error: function (error) {
//             console.error("request failed");
//             console.error("Error:", error);
//         },
//     });
// });
