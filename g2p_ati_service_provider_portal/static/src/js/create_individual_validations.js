$(document).ready(function () {
    // $('.selectpicker').selectpicker();

    // Determine starting index based on existing crop_info_data
    var cropMaxIndex = 0;
    $(".crop-section-wrapper").each(function () {
        var cropIndex = parseInt($(this).attr("data-index"), 10);
        if (!isNaN(cropIndex)) {
            cropMaxIndex = Math.max(cropMaxIndex, cropIndex);
        }
    });
    var cropIndex = cropMaxIndex + 1;

    var livestockMaxIndex = 0;
    $(".livestock-section-wrapper").each(function () {
        var livestockIndex = parseInt($(this).attr("data-index"), 10);
        if (!isNaN(livestockIndex)) {
            livestockMaxIndex = Math.max(livestockMaxIndex, livestockIndex);
        }
    });
    var livestockIndex = livestockMaxIndex + 1;

    var landMaxIndex = 0;
    $(".land-section-wrapper").each(function () {
        var landIndex = parseInt($(this).attr("data-index"), 10);
        if (!isNaN(landIndex)) {
            landMaxIndex = Math.max(landMaxIndex, landIndex);
        }
    });
    var landIndex = landMaxIndex + 1;

    // Console.log(incomeSourceData);
    // VirtualSelect.init({
    //     ele: `#hh_income_type`,
    //     options: incomeSourceData,
    //     search: true,
    //     multiple: true,
    //     additionalClasses: 'custom-multi-select',
    // });

    // if (cropInfoData && cropInfoData.length > 0) {
    //     cropInfoData.forEach(function(cropInfo) {
    //         VirtualSelect.init({
    //             ele: `#crop_illness_types_${cropInfo['index']}`,
    //             options: cropIllnessType,
    //             search: true,
    //             multiple: true,
    //             selectedValue: cropInfo.illness_type,
    //         });
    //     });
    // }
    // else {
    //     VirtualSelect.init({
    //         ele: `#crop_illness_types_0`,
    //         options: cropIllnessType,
    //         search: true,
    //         multiple: true,
    //     });
    // }

    // if (livestockInfoData && livestockInfoData.length > 0) {
    //     livestockInfoData.forEach(function(livestockInfo) {
    //         VirtualSelect.init({
    //             ele: `#livestock_illness_types_${livestockInfo['index']}`,
    //             options: livestockIllnessType,
    //             search: true,
    //             multiple: true,
    //             selectedValue: livestockInfo.illness_type,
    //         });
    //     });
    // }
    // else {
    //     VirtualSelect.init({
    //         ele: `#livestock_illness_types_0`,
    //         options: livestockIllnessType,
    //         search: true,
    //         multiple: true,
    //     });
    // }

    $("#add-crop-info").click(function () {
        var $template = $("#crop-hidden-template").html();
        var $formContainer = $("#section-content-crop");

        // Use jQuery to replace {cropIndex} placeholder in the template
        var newLineHtml = $template.replace(/\{9999\}/g, cropIndex);
        var $newLine = $(newLineHtml);
        $formContainer.append($newLine);

        // Var newSelectIdIllness = `crop_illness_types_${cropIndex}`;
        //     VirtualSelect.init({
        //         ele: `#${newSelectIdIllness}`,
        //         options: cropIllnessType,
        //         search: true,
        //         multiple: true,
        //     });
        cropIndex++;
    });

    $("#add-livestock-info").click(function () {
        var $template = $("#livestock-hidden-template").html();
        var $formContainer = $("#section-content-livestock");

        // Use jQuery to replace {cropIndex} placeholder in the template
        var newLineHtml = $template.replace(/\{9999\}/g, livestockIndex);
        var $newLine = $(newLineHtml);
        $formContainer.append($newLine);

        // Var newSelectIdIllness = `livestock_illness_types_${livestockIndex}`;
        //     VirtualSelect.init({
        //         ele: `#${newSelectIdIllness}`,
        //         options: livestockIllnessType,
        //         search: true,
        //         multiple: true,
        //     });
        livestockIndex++;
    });

    $("#add-land-info").click(function () {
        var $template = $("#land-hidden-template").html();
        var $formContainer = $("#section-content-land");

        // Use jQuery to replace {cropIndex} placeholder in the template
        var newLineHtml = $template.replace(/\{9999\}/g, landIndex);
        var $newLine = $(newLineHtml);
        $formContainer.append($newLine);

        landIndex++;
    });

    // Function to toggle display and required attribute of a field
    function toggleField(selectElementId, fieldId, inputId, yesText = "yes") {
        const selectElement = document.getElementById(selectElementId);
        const field = document.getElementById(fieldId);
        // Const input = document.getElementById(inputId);
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();

        if (selectedOptionText === yesText.toLowerCase()) {
            field.style.display = "block";
            // Input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            // Input.removeAttribute("required");
        }
    }

    // Function to handle changes in a select element
    // eslint-disable-next-line no-unused-vars
    function handleSelectChange(selectElementId, fieldId, inputId, otherText = "other") {
        const selectElement = document.getElementById(selectElementId);
        const field = document.getElementById(fieldId);
        const input = document.getElementById(inputId);
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();
        if (selectedOptionText === otherText.toLowerCase()) {
            field.style.display = "block";
            input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            input.removeAttribute("required");
        }
    }

    function formatInputWithSpaces(inputElement) {
        inputElement.addEventListener("input", function () {
            const value = inputElement.value.replace(/\s+/g, ""); // Remove any existing spaces
            const formattedValue = value.match(/.{1,4}/g)?.join(" ") || ""; // Add space after every 4 digits
            inputElement.value = formattedValue;
        });
    }

    // Apply the function to both UID and RID inputs

    const ridInput = document.getElementById("rid_input");
    const uidInput = document.getElementById("uid_input");
    const uidError = document.getElementById("uid_error");
    const ridError = document.getElementById("rid_error");

    formatInputWithSpaces(uidInput);
    formatInputWithSpaces(ridInput);

    uidInput.addEventListener("input", function () {
        const sanitizedValue = uidInput.value.replace(/\s+/g, ""); // Remove all spaces

        if (sanitizedValue.length !== 12 && sanitizedValue.length !== 0) {
            uidInput.classList.add("uid_error");
            uidError.style.display = "block";
        } else {
            uidInput.classList.remove("uid_error");
            uidError.style.display = "none";
        }
    });

    ridInput.addEventListener("input", function () {
        const sanitizedValue = ridInput.value.replace(/\s+/g, ""); // Remove all spaces

        if (sanitizedValue.length !== 29 && sanitizedValue.length !== 0) {
            ridInput.classList.add("rid_error");
            ridError.style.display = "block";
        } else {
            ridInput.classList.remove("rid_error");
            ridError.style.display = "none";
        }
    });

    // Event listeners
    function handleNationalIdSelection() {
        const selectElement = document.getElementById("have-national-id-selection");
        const uidDiv = document.getElementById("uid-div");
        const ridDiv = document.getElementById("rid-div");
        const ridInput = document.getElementById("rid_input");
        // Const uidInput = document.getElementById("uid_input");
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();

        if (selectedOptionText === "yes") {
            uidDiv.style.display = "block";
            uidInput.setAttribute("required", "required");
            ridDiv.style.display = "none";
            ridInput.removeAttribute("required");
        } else if (selectedOptionText === "no") {
            uidDiv.style.display = "none";
            uidInput.removeAttribute("required");
            ridDiv.style.display = "block";
            // RidInput.setAttribute("required", "required");
        } else {
            uidDiv.style.display = "none";
            uidInput.removeAttribute("required");
            ridDiv.style.display = "none";
            ridInput.removeAttribute("required");
        }
        uidError.style.display = "none";
    }

    function handlePhoneNumberSelection() {
        const selectElement = document.getElementById("have-phone-no-selection");
        const primaryPhoneDiv = document.getElementById("primary-div");
        const otherPhoneDiv = document.getElementById("other-div");
        const primaryPhone = document.getElementById("primary_phone");
        const otherPhone = document.getElementById("other_phone");
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();

        if (selectedOptionText === "yes") {
            primaryPhoneDiv.style.display = "block";
            primaryPhone.setAttribute("required", "required");
            otherPhoneDiv.style.display = "none";
            otherPhone.removeAttribute("required");
        } else if (selectedOptionText === "no") {
            primaryPhoneDiv.style.display = "none";
            primaryPhone.removeAttribute("required");
            otherPhoneDiv.style.display = "block";
            otherPhone.setAttribute("required", "required");
        } else {
            primaryPhoneDiv.style.display = "none";
            primaryPhone.removeAttribute("required");
            otherPhoneDiv.style.display = "none";
            otherPhone.removeAttribute("required");
        }
    }

    // Function to update options for a select element based on an AJAX response
    function updateOptions(
        url,
        data,
        targetSelectId,
        defaultOptionText = "Select",
        originalEvent = "",
        selectdropdown = ""
    ) {
        console.log(data);
        $.ajax({
            url: url,
            method: "POST",
            dataType: "json",
            data: data,
            success: function (options) {
                var selectedvalue = " ";
                const selectElement = document.getElementById(targetSelectId);
                const selectedName = selectElement.options[selectElement.selectedIndex].text;
                if (
                    originalEvent !== "" &&
                    (selectdropdown === "current_region" || selectdropdown === "region")
                ) {
                    selectedvalue = " ";
                } else if (originalEvent !== "") {
                    selectedvalue = " ";
                } else if (selectElement.selectedIndex > 0) {
                    selectedvalue = selectElement.options[selectElement.selectedIndex].value;
                    // If (selectedName) {
                    //     defaultOptionText = selectedName;
                    // }
                } else if (selectElement.selectedIndex === 0 && selectedName !== "Select") {
                    selectedvalue = selectElement.options[selectElement.selectedIndex].value;
                    // If (selectedName) {
                    //     defaultOptionText = selectedName;
                    // }
                }

                selectElement.innerHTML = "";
                const defaultOption = document.createElement("option");
                defaultOption.value = selectedvalue;
                defaultOption.textContent = defaultOptionText;
                selectElement.appendChild(defaultOption);

                options.forEach((option) => {
                    const opt = document.createElement("option");
                    opt.value = option.id;
                    opt.textContent = option.name;
                    selectElement.appendChild(opt);
                });
            },
            error: function (error) {
                console.error("Error fetching options:", error);
            },
        });
    }

    // Event listener for national ID selection change
    $("#have-national-id-selection").on("change", handleNationalIdSelection);
    // Event listener for phone number selection change
    $("#have-phone-no-selection").on("change", handlePhoneNumberSelection);

    $("#access-to-machinery-selection").on("change", function () {
        toggleField("access-to-machinery-selection", "machinery-field", "machinery-types-select");
    });

    $("#access-to-finance-selection").on("change", function () {
        toggleField("access-to-finance-selection", "finance-field", "finance-selection");
    });

    $("#region_selection").on("change", function (event) {
        console.log("HERE");
        const regionId = this.value;
        var ev = event.originalEvent;
        updateOptions("/update_zone_options", {region_id: regionId}, "zon_selection", "Select", ev, "region");
        updateOptions("/update_woreda_options", {zone_id: 0}, "woreda_selection", "Select", ev, "region");
        updateOptions("/update_kebele_options", {woreda_id: 0}, "kebele_selection", "Select", ev, "region");
    });

    $("#zon_selection").on("change", function (event) {
        const zoneId = this.value;
        var ev = event.originalEvent;
        updateOptions("/update_woreda_options", {zone_id: zoneId}, "woreda_selection", "Select", ev);
        updateOptions("/update_kebele_options", {woreda_id: 0}, "kebele_selection", "Select", ev);
    });

    $("#woreda_selection").on("change", function (event) {
        const woredaId = this.value;
        var ev = event.originalEvent;
        updateOptions("/update_kebele_options", {woreda_id: woredaId}, "kebele_selection", "Select", ev);
    });

    // Trigger the change event on page load to handle the initial state
    $("#have-national-id-selection").trigger("change");
    $("#have-phone-no-selection").trigger("change");
    $("#access-to-machinery-selection").trigger("change");
    $("#access-to-finance-selection").trigger("change");

    // Validation for email
    const emailInput = document.getElementById("email");

    function isValidEmail(email) {
        // Basic email regex pattern
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    emailInput.addEventListener("input", function () {
        if (emailInput.value.length === 0) {
            emailInput.classList.remove("is-invalid");
            // EmailError.style.display = "none";
        } else if (isValidEmail(emailInput.value)) {
            emailInput.classList.remove("is-invalid");
            // EmailError.style.display = "none";
        } else {
            emailInput.classList.add("is-invalid");
            // EmailError.style.display = "block";
        }
    });

    function expandSection(sectionId) {
        var consentSection = document.getElementById(sectionId);
        consentSection.classList.add("show");
    }
    // Function hideSection(sectionId) {
    //     var consentSection = document.getElementById(sectionId);
    //     consentSection.classList.add("hide");
    // }

    window.customvalidateForm = function (isCreateForm) {
        console.log("Here");
        const requiredFields = document.querySelectorAll("[required]");
        var valid = true;

        for (let i = 0; i < requiredFields.length; i++) {
            const field = requiredFields[i];
            const isFieldValid = field.value.trim();
            const fieldName = field.getAttribute("name");

            if (fieldName.includes("{9999}")) {
                continue;
            }

            valid = valid && isFieldValid;

            if (!valid) {
                field.classList.toggle("is-invalid", !isFieldValid);
                const parentDiv = field.closest(".section-container");
                if (parentDiv) {
                    var sectionRequiredFields = parentDiv.querySelectorAll("[required]");
                    sectionRequiredFields.forEach((sectionField) => {
                        const isSectionFieldValid = sectionField.value.trim();
                        sectionField.classList.toggle("is-invalid", !isSectionFieldValid);
                    });

                    const navId = parentDiv.id + "-link";
                    var navLink = document.getElementById(navId);
                    expandSection(parentDiv.id);
                    navLink.click();
                }

                break;
            }
        }

        if (valid) {
            this.validateForm(isCreateForm);
        }
    };
});

function validateSelect(selectElement) {
    const value = selectElement.value;
    const defaultValue = selectElement.options[0].value;
    if (value !== defaultValue && value !== "") {
        selectElement.classList.remove("is-invalid");
    }
}

function validateInput(inputElement) {
    const value = inputElement.value;
    if (value.trim() !== "") {
        inputElement.classList.remove("is-invalid");
    }
}

// eslint-disable-next-line no-unused-vars
function validateElement(element) {
    // Check if the element is a select or an input field
    if (element.tagName === "SELECT") {
        validateSelect(element);
    } else if (element.tagName === "INPUT") {
        validateInput(element);
    }
}

function validateUID() {
    const uid = document.getElementById("uid_input");
    const uidError = document.getElementById("uid_error");
    const isValid = uid.value.length === 12 && /^\d+$/.test(uid.value);
    uid.classList.toggle("is-invalid", !isValid);
    uidError.style.display = isValid ? "none" : "block";
    return isValid;
}

function validateSection(sectionId) {
    const section = document.getElementById(sectionId);
    const requiredFields = section.querySelectorAll("[required]");
    let valid = true;

    requiredFields.forEach((field) => {
        const isFieldValid = field.value.trim();
        var fieldName = field.getAttribute("name");
        if (fieldName.includes("{9999}")) {
            return;
        }

        field.classList.toggle("is-invalid", !isFieldValid);
        valid = valid && isFieldValid;
        if (sectionId === "id-section" && fieldName === "uid") {
            valid = valid && validateUID();
        }
    });

    return valid;
}

// Let previousSection = "id-section";

function showSection(sectionId, element, fromGroup = false) {
    // Val = validateSection(previousSection);
    var val = true;

    if (val) {
        if (fromGroup) {
            document.querySelectorAll(".section-container-group").forEach((section) => {
                section.style.display = "none";
            });
        } else {
            document.querySelectorAll(".section-container").forEach((section) => {
                if (
                    sectionId === "family-members" ||
                    sectionId === "location-details" ||
                    sectionId === "family-member-template"
                ) {
                    console.log("yes it is");
                    section.style.display = "none";
                } else {
                    section.style.display = "none";
                    const farmerDetailSection = document.getElementById("farmer-details");
                    if (farmerDetailSection) {
                        console.log("Farmer Detail Secion is");
                        console.log(farmerDetailSection);

                        farmerDetailSection.style.display = "block";
                    }
                }
            });
        }
        document.getElementById(sectionId).style.display = "block";
        // PreviousSection = sectionId;
        // If (!fromGroup) {
        document.querySelectorAll(".sidebar .nav-link").forEach((link) => {
            link.classList.remove("active");
        });
        // }
        if (element) {
            element.classList.add("active");
        }
    }
}

// eslint-disable-next-line no-unused-vars
function showNextSection(nextSectionId, currentSectionId, fromGroup = false) {
    var val = validateSection(currentSectionId);
    // Val = true

    if (val) {
        var activeLink = document.querySelector(".sidebar .nav-link.active");
        // Console.log(activeLink);
        var nextLink = activeLink.parentElement.nextElementSibling.querySelector(".nav-link");
        if (nextLink) {
            nextLink.classList.remove("disabled");
            showSection(nextSectionId, nextLink, fromGroup);
        }
    }
}
function checkRequired() {
    // Const farmingType = document.getElementById('farming-type-selection');
    // const selectedOptionText = farmingType.options[farmingType.selectedIndex].text
    //     .trim()
    //     // .toLowerCase();
    // console.log(selectedOptionText);
    // if (selectedOptionText === 'Agro-Pastoral' || selectedOptionText === 'Mixed Far4ming' ) {
    //     // field2.setAttribute('required', 'required');
    // }
}

function toggleFieldBasedOnRadio(inputName, fieldIdToToggle, toggleValue = "Yes") {
    const radios = document.querySelectorAll(`input[name="${inputName}"]`);
    let shouldShowField = false;

    radios.forEach((radio) => {
        if (radio.checked && radio.dataset.text === toggleValue) {
            shouldShowField = true;
        }
    });

    const fieldToToggle = document.getElementById(fieldIdToToggle);
    fieldToToggle.style.display = shouldShowField ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", function () {
    // Initial check on page load
    checkRequired();
    toggleFieldBasedOnRadio("is_member_of_primary_coop", "primary-coop-field");
    toggleFieldBasedOnRadio("is_member_of_coop_union", "coop-union-field");
    toggleFieldBasedOnRadio("in_farmer_cluster", "primary-commodity-field");
    toggleFieldBasedOnRadio("in_farmer_cluster", "role-in-cluster-field");

    // Attach event listeners to the radio buttons
    const primaryCoopRadios = document.querySelectorAll('input[name="is_member_of_primary_coop"]');
    primaryCoopRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            toggleFieldBasedOnRadio("is_member_of_primary_coop", "primary-coop-field");
        });
    });

    const coopUnionRadios = document.querySelectorAll('input[name="is_member_of_coop_union"]');
    coopUnionRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            toggleFieldBasedOnRadio("is_member_of_coop_union", "coop-union-field");
        });
    });

    const isMemberRadios = document.querySelectorAll('input[name="in_farmer_cluster"]');
    isMemberRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            toggleFieldBasedOnRadio("in_farmer_cluster", "primary-commodity-field");
            toggleFieldBasedOnRadio("in_farmer_cluster", "role-in-cluster-field");
        });
    });
});
