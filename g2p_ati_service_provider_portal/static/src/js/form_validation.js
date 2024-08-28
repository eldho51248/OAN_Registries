$(document).ready(function () {
    $("#lang").on("change", function () {
    const field = document.getElementById("other-lang-field");
    const input = document.getElementById("other_lang");
    const selectedValues = Array.from(document.getElementById("lang").selectedOptions).map(
        (option) => option.value
    );
    if (selectedValues.includes("16")) {
        field.style.display = "block";
        input.setAttribute("required", "required");
        console.log(selectedValues);
    } else {
        field.style.display = "none";
        input.removeAttribute("required");
        input.value = "";
        console.log(selectedValues);
    }
});
    $("#inistitutes-selection").on("change", function () {
    const field = document.getElementById("specify_inistitutes-field");
    const input = document.getElementById("specify_inistitutes");
    const selectElement = document.getElementById("inistitutes-selection");
    const selectedOptionStrings = Array.from(selectElement.selectedOptions).map((option) =>
        option.textContent.trim()
    );
    if (selectedOptionStrings.includes("Other")) {
        field.style.display = "block";
        input.setAttribute("required", "required");
    } else {
        field.style.display = "none";
        input.value = "";
        input.removeAttribute("required");
    }
});
$("#inistitutes-selection-current").on("change", function () {
    const field = document.getElementById("specify_inistitutes-field-current");
    const input = document.getElementById("specify_inistitutes-current");
    const selectElement = document.getElementById("inistitutes-selection-current");
    const selectedOptionStrings = Array.from(selectElement.selectedOptions).map((option) =>
        option.textContent.trim()
    );
    if (selectedOptionStrings.includes("Other") || selectedOptionStrings.includes("Other")) {
        field.style.display = "block";
        input.setAttribute("required", "required");
    } else {
        field.style.display = "none";
        input.value = "";
        input.removeAttribute("required");
    }
});
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    const formattedDate = `${year}-${month}-${day}`;

    // Set the value of the date input
    document.getElementById("enumeratorconsentDate").value = formattedDate;

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
            input.value = "";
        }
    }

    window.showSection = function (sectionId, element) {
        document.querySelectorAll(".section-container").forEach((section) => {
            section.style.display = "none";
        });
        document.getElementById(sectionId).style.display = "block";
        document.querySelectorAll(".sidebar .nav-link").forEach((link) => {
            link.classList.remove("active");
        });
        if (element) {
            element.classList.add("active");
        }
        if (sectionId == "social-status") {
            if ($("#marital_status-select").length) {
                handleSelectChange(
                    "marital_status-select",
                    "other-marital-status-field",
                    "other_marital_status"
                );
            }

            if ($("#meducation-select").length) {
                handleSelectChange("education-select", "other-education-field", "other_education");
            }

            if ($("#mother-tongue-select").length) {
                handleSelectChange("mother-tongue-select", "other-language-field", "other_language");
            }

            if ($("#sleep_at_night-select").length) {
                handleSelectChange("sleep_at_night-select", "specify-sleep-field", "other_spend_night");
            }
            if ($("#disability-selection").length) {
                const checkedRadio = document.querySelector(
                    '.form-radio-group input[name="disability_status"]:checked'
                );
                if (checkedRadio) {
                    selectedValue = checkedRadio.value;
                    showElementBasedOnRadioSelection(
                        "/get_selection_name",
                        {selectedValue: selectedValue},
                        "other-disability-field",
                        "disability-selection",
                        "specify-disability-field"
                    );
                    const field = document.getElementById("other-disability-field");
                    const input = document.getElementById("other_disability");
                    if (field.style.display == "none") {
                        input.value = "";
                    }
                }
            }

            handleCheckboxChange(
                ".homeless_reason-checkbox",
                "other_homeless-field",
                "other_homeless_reason"
            );

            handleCheckboxChange(
                ".challenges_on_street-checkbox",
                "specify-challenge-field",
                "specify-challenge"
            );
            if ($("#source_income-selection").length) {
                handleSelectChange(
                    "source_income-selection",
                    "other-source-income-field",
                    "other_source_income"
                );
            }
            if ($("source_income-selection-current").length) {
                handleSelectChange(
                    "source_income-selection-current",
                    "other-source-income-field-current",
                    "other_source_income-current"
                );
            }
        }
    };

    $("#inistitutes-selection").on("change", function () {
        const field = document.getElementById("specify_inistitutes-field");
        const input = document.getElementById("specify_inistitutes");
        const selectElement = document.getElementById("inistitutes-selection");
        const selectedOptionStrings = Array.from(selectElement.selectedOptions).map((option) =>
            option.textContent.trim()
        );
        if (selectedOptionStrings.includes("Other")) {
            field.style.display = "block";
            input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            input.value = "";
            input.removeAttribute("required");
        }
    });
    $("#inistitutes-selection-current").on("change", function () {
        const field = document.getElementById("specify_inistitutes-field-current");
        const input = document.getElementById("specify_inistitutes-current");
        const selectElement = document.getElementById("inistitutes-selection-current");
        const selectedOptionStrings = Array.from(selectElement.selectedOptions).map((option) =>
            option.textContent.trim()
        );
        if (selectedOptionStrings.includes("Other") || selectedOptionStrings.includes("Other")) {
            field.style.display = "block";
            input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            input.value = "";
            input.removeAttribute("required");
        }
    });
});

// Function to show or hide sections
function showSection(sectionId, element) {
    document.querySelectorAll(".section-container").forEach((section) => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
    document.querySelectorAll(".sidebar .nav-link").forEach((link) => {
        link.classList.remove("active");
    });
    if (element) {
        element.classList.add("active");
    }
}
function disableNav() {
    const navLinks = document.querySelectorAll(".sidebar .nav-link");
    navLinks.forEach((link, index) => {
        if (index > 0) {
            link.classList.toggle("disabled");
        }
    });
}

// Function to enable/disable navigation based on checkbox state
function toggleNav(checkbox) {
    const navLinks = document.querySelectorAll(".sidebar .nav-link");
    const nextButton = document.getElementById("nextButton");
    let activeIndex = Array.from(navLinks).findIndex((link) => link.classList.contains("active")) + 1;

    navLinks.forEach((link, index) => {
        if (index > 0) {
            link.classList.toggle("disabled", !checkbox.checked || activeIndex !== index);
        }
    });

    nextButton.classList.toggle("btn-disabled", !checkbox.checked);
    nextButton.classList.toggle("next-btn-active", !checkbox.checked);
}

// Function to show the next section
function showNextSection(nextSectionId, currentSectionId) {
    val = validateSection(currentSectionId);

    if (val) {
        var activeLink = document.querySelector(".sidebar .nav-link.active");
        var nextLink = activeLink.parentElement.nextElementSibling.querySelector(".nav-link");
        if (nextLink) {
            nextLink.classList.remove("disabled");
            showSection(nextSectionId, nextLink);
        }

        if (nextSectionId === "geo-location") {
            updateOptions(
                "/update_zone_options",
                {region_id: 0, check_permission: true},
                "current_zon_selection",
                "Select"
            );
            updateOptions(
                "/update_woreda_options",
                {zone_id: 0, check_permission: true},
                "current_woreda_selection",
                "Select"
            );
            updateOptions(
                "/update_hotspot_options",
                {woreda_id: 0, check_permission: true},
                "hot_spot",
                "Select"
            );
        }
    }
}

// Function to toggle UID and RID fields
function toggleIdFields() {
    const selectedValue = document.querySelector(".have-id-select:checked").value;
    showElementBasedOnRadioSelection(
        "/get_selection_name",
        {selectedValue},
        "uid-div",
        "uid_input",
        "rid-div",
        "rid-div",
        "rid_input"
    );
}

// Function to validate UID
function validateUID() {
    const uid = document.getElementById("uid_input");
    const uidError = document.getElementById("uidError");
    const isValid = uid.value.length === 12 && /^\d+$/.test(uid.value);
    uid.classList.toggle("is-invalid", !isValid);
    uidError.style.display = isValid ? "none" : "block";
    return isValid;
}

// Function to check all required radio buttons
function checkAllRequiredRadios() {
    let valid = true;
    document.querySelectorAll(".form-radio-group").forEach((group) => {
        const radios = group.querySelectorAll('input[type="radio"]');
        const name = radios[0].getAttribute("name");
        const checkedRadio = group.querySelector(`input[name="${name}"]:checked`);
        group.classList.toggle("border-red", !checkedRadio);
        valid = valid && !!checkedRadio;
    });
    return valid;
}

function showElementBasedOnRadioSelection(url, data, field1, input, field2, no_field = "", no_input = "") {
    $.ajax({
        url: url,
        method: "POST",
        dataType: "json",
        data: data,
        success: function (options) {
            options.forEach((option) => {
                const selectedOptionText = option.name;
                const fieldElement1 = document.getElementById(field1);
                const inputElement = document.getElementById(input);
                const fieldElement2 = document.getElementById(field2);
                if (selectedOptionText === "Yes") {
                    if (no_field != "") {
                        const nofieldElement2 = document.getElementById(no_field);
                        nofieldElement2.style.display = "none";
                        if (no_input != "") {
                            const noinput_element = document.getElementById(no_input);
                            noinput_element.removeAttribute("required", "required");
                            noinput_element.value = "";
                        }
                    }
                    fieldElement1.style.display = "block";
                    if (inputElement) {
                        inputElement.setAttribute("required", "required");
                    }
                } else {
                    fieldElement1.style.display = "none";
                    fieldElement2.style.display = "none";
                    if (inputElement) {
                        inputElement.removeAttribute("required");
                        inputElement.value = "";
                    }
                    if (field1 == "specific_additional_support-field") {
                        var checkboxes = document.querySelectorAll(".specific_support_options-checkbox");
                        checkboxes.forEach(function (checkbox) {
                            if (checkbox.type === "checkbox") {
                                checkbox.checked = false;
                            }
                        });
                    }

                    if (no_field != "") {
                        const nofieldElement2 = document.getElementById(no_field);
                        nofieldElement2.style.display = "block";
                        if (no_input != "") {
                            const noinput_element = document.getElementById(no_input);
                            noinput_element.setAttribute("required", "required");
                        }
                    }
                }
            });
        },
        error: function (error) {
            console.error("Error fetching options:", error);
        },
    });
}

function check_all_required_radio() {
    valid = true;
    const radioGroups = document.querySelectorAll(".form-radio-group");
    radioGroups.forEach((group) => {
        const radios = group.querySelectorAll('input[type="radio"]');
        const name = radios[0].getAttribute("name");
        const checkedRadio1 = group.querySelector(`input[name="${name}"]`).closest(".form-radio-group");
        const checkedRadio = group.querySelector(`input[name="${name}"]:checked`);

        if (!checkedRadio) {
            valid = false;
            checkedRadio1.classList.add("border-red");
        } else if (checkedRadio) {
            checkedRadio1.classList.remove("border-red");
        }
    });

    const checkboxes = document.querySelectorAll(".homeless_reason-checkbox");
    const checkboxes2 = document.querySelectorAll(".challenges_on_street-checkbox");
    const check_institutes = document.querySelectorAll('.inistitutes-selection');
    const check_current_institutes = document.querySelectorAll('.inistitutes-selection-current');
    const check_support = document.querySelectorAll('.specific_support_options-checkbox');
    const select_element = document.getElementById('inistitutes-selection');
    const select_element_current = document.getElementById('inistitutes-selection-current');

    let isChecked = false;
    let isChecked2= false;
    let ischecked_institutes = false;
    let ischecked_current_institutes = false;
    let ischecked_support = false;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
                isChecked = true;
        }
    });
    checkboxes2.forEach((checkbox) => {
        if (checkbox.checked) {
            isChecked2 = true;
        }
    });
    if (select_element.selectedOptions.length > 0){
        ischecked_institutes = true;
    }
    if (select_element_current.selectedOptions.length > 0){
        ischecked_current_institutes = true;
    }

    check_support.forEach((checkbox) => {
        if (checkbox.checked) {
                ischecked_support = true;
        }
    });
    if(isChecked == false){
        const checkboxIds = ['homeless_reason-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.add('border-red');
                }
            });

    }else{
        const checkboxIds = ['homeless_reason-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.remove('border-red');
                }
            });
    }

    if(isChecked2 == false){
        const checkboxIds = ['challenges_on_street-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.add('border-red');
                }
            });

    }
    else{
        const checkboxIds = ['challenges_on_street-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.remove('border-red');
                }
            });
    }
    if(ischecked_institutes == false){
        const checkboxIds = ['inistitutes-selection-div'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.add('border-red');
                }
            });

    }
    else{
        const checkboxIds = ['inistitutes-selection-div'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.remove('border-red');
                }
            });
    }
    if(ischecked_current_institutes == false){
        const checkboxIds = ['inistitutes-div-current'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.add('border-red');
                }
            });

    }
    else{
        const checkboxIds = ['inistitutes-div-current'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.remove('border-red');
                }
            });
    }
    if(ischecked_support == false){
        const checkboxIds = ['specific_support_options-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.add('border-red');
                }
                console.log("checkboxIds");
                console.log(checkboxIds);
            });

    }else{
        const checkboxIds = ['specific_support_options-checkbox'];
            checkboxIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.classList.remove('border-red');
                }
            });
    }
    return valid;
}
function validateSection(sectionId) {
    const section = document.getElementById(sectionId);
    const nextButton = document.getElementById("nextButton");
    const requiredFields = section.querySelectorAll("[required]");
    let valid = true;

    if (sectionId === "social-status") {
        valid = check_all_required_radio();
    }

    if (sectionId === "enumerator-consent") {
        const checkboxGroup = document.getElementById("consentCheckboxGroup");
        const checkboxes = document.querySelectorAll(".enumerator-consent-checkbox");
        const anyChecked = Array.from(checkboxes).some((checkbox) => checkbox.checked);

        checkboxGroup.classList.toggle("border-red", !anyChecked);
        valid = valid && anyChecked;
    }

    if (sectionId === "id-section") {
        const radioButtons = document.querySelectorAll(".have-id-select");
        const checkedRadioButton = Array.from(radioButtons).find((radioButton) => radioButton.checked);

        if (!checkedRadioButton) {
            radioButtons.forEach((radioButton) => {
                const parentGroup = radioButton.closest(".form-radio-group");
                if (parentGroup) {
                    parentGroup.classList.add("border-red");
                }
            });
            return false;
        }

        const selectedValue = checkedRadioButton.value;
        $.ajax({
            url: "/get_selection_name",
            method: "POST",
            dataType: "json",
            data: {selectedValue: selectedValue},
            async: false, // Synchronous request
            success: function (options) {
                const option = options[0]; // Assuming options has at least one element
                const selectedOptionText = option.name;

                if (!selectedOptionText) {
                    radioButtons.forEach((radioButton) => {
                        const parentGroup = radioButton.closest(".form-radio-group");
                        if (parentGroup) {
                            parentGroup.classList.add("border-red");
                        }
                    });
                    valid = false;
                } else if (selectedOptionText === "Yes") {
                    radioButtons.forEach((radioButton) => {
                        const parentGroup = radioButton.closest(".form-radio-group");
                        if (parentGroup) {
                            parentGroup.classList.remove("border-red");
                        }
                    });
                    const uid = document.getElementById("uid_input");
                    const uidError = document.getElementById("uidError");
                    const isValid = uid.value.length === 12 && /^\d+$/.test(uid.value);

                    uid.classList.toggle("is-invalid", !isValid);
                    valid = isValid;
                } else if (selectedOptionText === "No") {
                    radioButtons.forEach((radioButton) => {
                        const parentGroup = radioButton.closest(".form-radio-group");
                        if (parentGroup) {
                            parentGroup.classList.remove("border-red");
                        }
                    });
                    const ridInput = document.getElementById("rid_input").value;
                    if (!ridInput.trim()) {
                        valid = false;
                    }
                }
            },
            error: function () {
                valid = false;
            },
        });
    }

    requiredFields.forEach((field) => {
        const isFieldValid = field.value.trim();
        field.classList.toggle("is-invalid", !isFieldValid);
        nextButton.classList.toggle("btn-disabled", !isFieldValid);
        nextButton.classList.toggle("next-btn-active", !isFieldValid);

        valid = valid && isFieldValid;
    });

    return valid;
}

// Function to handle checkbox change for specific support options
function handleCheckboxChange(checkboxClass, fieldId, inputId, otherText = "other") {
    const checkboxes = document.querySelectorAll(checkboxClass);
    const field = document.getElementById(fieldId);
    const input = document.getElementById(inputId);
    let isChecked = Array.from(checkboxes).some(
        (checkbox) =>
            checkbox.checked &&
            checkbox.nextElementSibling.textContent.trim().toLowerCase() === otherText.toLowerCase()
    );

    field.style.display = isChecked ? "block" : "none";
    input.setAttribute("required", isChecked);
    if (!isChecked) input.value = "";
}

// Add event listeners for dynamic elements
document.querySelectorAll(".have-id-select").forEach((radio) => {
    radio.addEventListener("change", toggleIdFields);
});

document.querySelectorAll(".specific_support_options-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", () =>
        handleCheckboxChange(
            ".specific_support_options-checkbox",
            "other_additional_support-field",
            "other_additional_support"
        )
    );
});

// Handle region and zone selections

function updateOptions(
    url,
    data,
    targetSelectId,
    defaultOptionText = "Select",
    originalEvent = "",
    selectdropdown = ""
) {
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
                if (selectedName) {
                    defaultOptionText = selectedName;
                }
            } else if (selectElement.selectedIndex == 0 && selectedName != "Select") {
                selectedvalue = selectElement.options[selectElement.selectedIndex].value;
                if (selectedName) {
                    defaultOptionText = selectedName;
                }
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

$("#current_region_selection").on("change", function () {
    const selectedOptionText = $(this).find(":selected").text().trim();
    const label_current_zone = $("#label-current-zone");

    if (selectedOptionText === "Addis Ababa") {
        label_current_zone.text("Sub city");
    } else {
        label_current_zone.text("Zone");
    }
});

$("#region_selection").on("change", function () {
    const selectedOptionText = $(this).find(":selected").text().trim();
    const label_current_zone = $("#label-birth-zone");
    if (selectedOptionText === "Addis Ababa") {
        label_current_zone.text("Sub city");
    } else {
        label_current_zone.text("Zone");
    }
});

$("#region_selection").on("change", function (event) {
    const regionId = this.value;
    var ev = event.originalEvent;
    updateOptions("/update_zone_options", {region_id: regionId}, "zon_selection", "Select", ev, "region");
    updateOptions("/update_woreda_options", {zone_id: 0}, "woreda_selection", "Select", ev, "region");
});

$("#zon_selection").on("change", function (event) {
    const zoneId = this.value;

    var ev = event.originalEvent;
    updateOptions("/update_woreda_options", {zone_id: zoneId}, "woreda_selection", "Select", ev);
});

$("#current_region_selection").on("change", function (event) {
    const regionId = this.value;
    var ev = event.originalEvent;

    updateOptions(
        "/update_zone_options",
        {region_id: regionId, check_permission: true},
        "current_zon_selection",
        "Select",
        ev,
        "current_region"
    );
    updateOptions(
        "/update_woreda_options",
        {zone_id: 0, check_permission: true},
        "current_woreda_selection",
        "Select",
        ev,
        "current_region"
    );
    updateOptions(
        "/update_hotspot_options",
        {woreda_id: 0, check_permission: true},
        "hot_spot",
        "Select",
        ev,
        "current_region"
    );
});

$("#current_zon_selection").on("change", function (event) {
    const zoneId = this.value;

    var ev = event.originalEvent;
    updateOptions(
        "/update_woreda_options",
        {zone_id: zoneId, check_permission: true},
        "current_woreda_selection",
        "Select",
        ev
    );
    updateOptions(
        "/update_hotspot_options",
        {woreda_id: 0, check_permission: true},
        "hot_spot",
        "Select",
        ev,
        "current_region"
    );
});

$("#current_woreda_selection").on("change", function (event) {
    const woreda_id = this.value;

    var ev = event.originalEvent;
    updateOptions(
        "/update_hotspot_options",
        {woreda_id: woreda_id, check_permission: true},
        "hot_spot",
        "Select",
        ev
    );
});

// Disable navigation links on page load
// toggleNav(document.getElementById('consentCheckbox'));

// Handle dynamic radio button selections
document.querySelectorAll(".are-you-disabled-select").forEach((radioButton) => {
    radioButton.addEventListener("change", (event) => {
        const selectedValue = event.target.value;
        showElementBasedOnRadioSelection(
            "/get_selection_name",
            {selectedValue: selectedValue},
            "other-disability-field",
            "disability-selection",
            "specify-disability-field"
        );
        const field = document.getElementById("other-disability-field");
        const input = document.getElementById("other_disability");
        if (field.style.display == "none") {
            input.value = "";
        }
    });
});

// Handle select change events
function handleSelectChange(selectElementId, fieldId, inputId, otherText = "other") {
    const selectElement = document.getElementById(selectElementId);
    const field = document.getElementById(fieldId);
    const input = document.getElementById(inputId);
    const selectedOptionText = selectElement.options[selectElement.selectedIndex].text.trim().toLowerCase();
    if (selectedOptionText === otherText.toLowerCase()) {
        field.style.display = "block";
        input.setAttribute("required", "required");
    } else {
        field.style.display = "none";
        input.removeAttribute("required");
        input.value = "";
    }
}

document.getElementById("religion-select").addEventListener("change", function () {
    handleSelectChange("religion-select", "other-religion-field", "other_religion");
});

document.getElementById("marital_status-select").addEventListener("change", function () {
    handleSelectChange("marital_status-select", "other-marital-status-field", "other_marital_status");
});

document.getElementById("mother-tongue-select").addEventListener("change", function () {
    handleSelectChange("mother-tongue-select", "other-language-field", "other_language");
});

document.getElementById("education-select").addEventListener("change", function () {
    handleSelectChange("education-select", "other-education-field", "other_education");
});

document.getElementById("sleep_at_night-select").addEventListener("change", function () {
    handleSelectChange("sleep_at_night-select", "specify-sleep-field", "other_spend_night");
});

// Handle checkbox changes
function handleCheckboxChange(checkboxClass, fieldId, inputId, otherText = "other") {
    const checkboxes = document.querySelectorAll(checkboxClass);
    const field = document.getElementById(fieldId);
    const input = document.getElementById(inputId);
    let isChecked = false;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            const label = checkbox.nextElementSibling.textContent.trim().toLowerCase();
            if (label === otherText.toLowerCase()) {
                isChecked = true;
            }
        }
    });

    if (isChecked) {
        field.style.display = "block";
        input.setAttribute("required", "required");
    } else {
        field.style.display = "none";
        input.removeAttribute("required");
        input.value = "";
    }
}

document.querySelectorAll(".homeless_reason-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        handleCheckboxChange(".homeless_reason-checkbox", "other_homeless-field", "other_homeless_reason");
    });
});

document.querySelectorAll(".challenges_on_street-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        handleCheckboxChange(
            ".challenges_on_street-checkbox",
            "specify-challenge-field",
            "specify-challenge"
        );
    });
});

document.getElementById("source_income-selection").addEventListener("change", function () {
    selectChangeHideSection("source_income-selection", "pre-earn-per-field", "no income", "earn_per");
    selectChangeHideSection("source_income-selection", "pre-earn-amount-field", "no income", "amount");
    handleSelectChange("source_income-selection", "other-source-income-field", "other_source_income");
});

document.getElementById("source_income-selection-current").addEventListener("change", function () {
    selectChangeHideSection(
        "source_income-selection-current",
        "earn-per-field",
        "no income",
        "current_earn_per"
    );
    selectChangeHideSection(
        "source_income-selection-current",
        "earn-amount-field",
        "no income",
        "current_amount"
    );
    handleSelectChange(
        "source_income-selection-current",
        "other-source-income-field-current",
        "other_source_income-current"
    );
});

document.querySelectorAll(".received_any_assistance").forEach((radioButton) => {
    radioButton.addEventListener("change", (event) => {
        const selectedValue = event.target.value;
        showElementBasedOnRadioSelection(
            "/get_selection_name",
            {selectedValue: selectedValue},
            "select-received_any_assistance-field",
            "inistitutes-selection",
            "specify_inistitutes-field"
        );
        document.getElementById("inistitutes-selection").dispatchEvent(new Event("change"));
    });
});

document.querySelectorAll(".received_any_assistance").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
    document.getElementById("inistitutes-selection").dispatchEvent(new Event("change"));
});

document.querySelectorAll(".received_any_assistance-current").forEach((radioButton) => {
    radioButton.addEventListener("change", (event) => {
        const selectedValue = event.target.value;
        showElementBasedOnRadioSelection(
            "/get_selection_name",
            {selectedValue: selectedValue},
            "select-received_any_assistance-field-current",
            "inistitutes-selection-current",
            "specify_inistitutes-field-current"
        );
        document.getElementById("inistitutes-selection-current").dispatchEvent(new Event("change"));
    });
});

document.querySelectorAll(".received_any_assistance-current").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
});

document.querySelectorAll(".additional_support-select").forEach((radioButton) => {
    radioButton.addEventListener("change", (event) => {
        const selectedValue = event.target.value;
        showElementBasedOnRadioSelection(
            "/get_selection_name",
            {selectedValue: selectedValue},
            "specific_additional_support-field",
            "",
            "other_additional_support-field"
        );

        document.getElementById("specific_additional_support-checkbox").dispatchEvent(new Event("change"));
    });
});

document.querySelectorAll(".additional_support-select").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
});

function selectChangeHideSection(selectElementId, fieldId, otherText = "no income", inputId) {
    const selectElement = document.getElementById(selectElementId);
    const field = document.getElementById(fieldId);
    const input = document.getElementById(inputId);
    const selectedOptionText = selectElement.options[selectElement.selectedIndex].text.trim().toLowerCase();

    if (selectedOptionText === otherText.toLowerCase()) {
        field.style.display = "none";
        input.removeAttribute("required");
    } else {
        field.style.display = "block";
        input.setAttribute("required", "required");
    }
}
function get_id_name(url, data, uidLabel, uidInput, ridLabel, ridInput) {
    $.ajax({
        url: url,
        method: "POST",
        dataType: "json",
        data: data,
        success: function (options) {
            options.forEach((option) => {
                const selectedOptionText = option.name;
                if (selectedOptionText === "Yes") {
                    // Adjust the value according to your options
                    uidLabel.style.display = "block";
                    uidInput.style.display = "block";
                    ridLabel.style.display = "none";
                    ridInput.style.display = "none";
                } else if (selectedOptionText === "No") {
                    // Adjust the value according to your options
                    ridLabel.style.display = "block";
                    ridInput.style.display = "block";
                    uidLabel.style.display = "none";
                    uidInput.style.display = "none";
                    uidError.style.display = "none";
                }
            });
        },
    });
}

document.querySelectorAll(".have-id-select").forEach((radioButton) => {
    radioButton.addEventListener("change", (event) => {
        const selectedValue = event.target.value;
        const uidLabel = document.getElementById("uidLabel");
        const uidInput = document.getElementById("uid_input");
        const ridLabel = document.getElementById("ridLabel");
        const ridInput = document.getElementById("rid_input");
        get_id_name(
            "/get_selection_name",
            {selectedValue: selectedValue},
            uidLabel,
            uidInput,
            ridLabel,
            ridInput
        );
    });
});

document.querySelectorAll(".have-id-select").forEach((radioButton) => {
    if (radioButton.checked) {
        const selectedValue = radioButton.value;
        const uidLabel = document.getElementById("uidLabel");
        const uidInput = document.getElementById("uid_input");
        const ridLabel = document.getElementById("ridLabel");
        const ridInput = document.getElementById("rid_input");
        get_id_name(
            "/get_selection_name",
            {selectedValue: selectedValue},
            uidLabel,
            uidInput,
            ridLabel,
            ridInput
        );
    }
});

document.querySelectorAll(".specific_support_options-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        const label = checkbox.nextElementSibling.textContent.trim().toLowerCase();
        if (checkbox.checked && label === "other") {
            document.getElementById("other_additional_support-field").style.display = "block";
        } else {
            document.getElementById("other_additional_support-field").style.display = "none";
        }
    });
});

// Function to validate form section
window.customvalidateForm = function (isCreateForm) {
    if (validateSection("social-status")) {
        this.validateForm(isCreateForm);
    }
};
document.addEventListener("DOMContentLoaded", function () {
    const checkboxesByName = document.getElementsByName("consent");
    ischeckedBefore = false;
    document.getElementsByName("consent").forEach((radioButton) => {
        if (radioButton.checked) {
            ischeckedBefore = true;
        }
    });
    if (!ischeckedBefore) {
        disableNav();
    }

    checkboxesByName.forEach((checkbox) => {
        checkbox.addEventListener("click", function () {
            toggleNav(this);
        });
    });

    document.querySelectorAll(".have-id-select").forEach((radioButton) => {
        radioButton.addEventListener("change", (event) => {
            const selectedValue = event.target.value;

            const radioButtons = document.querySelectorAll(".have-id-select");
            const uidLabel = document.getElementById("uidLabel");
            const uidInput = document.getElementById("uid_input");
            const ridLabel = document.getElementById("ridLabel");
            const ridInput = document.getElementById("rid_input");

            get_id_name(
                "/get_selection_name",
                {selectedValue: selectedValue},
                uidLabel,
                uidInput,
                ridLabel,
                ridInput
            );
        });
    });
});

document.querySelectorAll(".are-you-disabled-select").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
});
$("#are-you-disabled-select").on("change", function () {
    toggleField("are-you-disabled-select", "other-disability-field", "other_disability");
});

$("#disability-selection").on("change", function () {
    handleSelectChange("disability-selection", "specify-disability-field", "other_disability");
});
document.querySelectorAll(".additional_support-select").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
});
document.querySelectorAll(".specific_support_options-checkbox").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
});

document.querySelectorAll(".received_any_assistance").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
    $("#inistitutes-selection").trigger("change");
});
document.querySelectorAll(".received_any_assistance-current").forEach((radioButton) => {
    if (radioButton.checked) {
        radioButton.dispatchEvent(new Event("change"));
    }
    $("#inistitutes-selection-current").trigger("change");
});


var today = new Date().toISOString().split('T')[0];

// Set the minimum date for the date field
document.addEventListener('DOMContentLoaded', function() {
  var birth_date = document.getElementById('dateOfBirth');
  var homeless_date = document.getElementById('livingStreets');
  birth_date.setAttribute('max', today);
  homeless_date.setAttribute('max', today);
});

$("#lang").trigger("change");
$("#inistitutes-selection").trigger("change");
$("#inistitutes-selection-current").trigger("change");
