$(document).ready(function () {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    const formattedDate = `${year}-${month}-${day}`;

    // Set the value of the date input
    document.getElementById("date_consent").value = formattedDate;

    // Function to toggle display and required attribute of a field
    function toggleField(selectElementId, fieldId, inputId, yesText = "yes") {
        const selectElement = document.getElementById(selectElementId);
        const field = document.getElementById(fieldId);
        const input = document.getElementById(inputId);
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();

        if (selectedOptionText === yesText.toLowerCase()) {
            field.style.display = "block";
            input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            input.removeAttribute("required");
        }
    }
    // If condition match hide section
    function selectChangeHideSection(selectElementId, fieldId, otherText = "no income") {
        const selectElement = document.getElementById(selectElementId);
        const field = document.getElementById(fieldId);
        const selectedOptionText = selectElement.options[selectElement.selectedIndex].text
            .trim()
            .toLowerCase();

        if (selectedOptionText === otherText.toLowerCase()) {
            field.style.display = "none";
        } else {
            field.style.display = "block";
        }
    }
    // If condition match hide section
    function selectChangeShowSection(
        selectElementId,
        fieldId,
        otherText = "other",
        fieldId1,
        otherText1 = "no"
    ) {
        const selectElement = document.getElementById(selectElementId);
        const fieldSelectId = document.getElementById(fieldId);
        const selectotherText = document.getElementById(otherText);
        const field1 = document.getElementById(fieldId1);
        var selectedOptionText = "";
        var selectedotherText = "";
        if (selectElement !== null) {
            selectedOptionText = selectElement.options[selectElement.selectedIndex].text.trim().toLowerCase();
        }

        if (selectotherText !== null) {
            selectedotherText = selectotherText.options[fieldSelectId.selectedIndex].text
                .trim()
                .toLowerCase();
        }
        if (selectedOptionText !== otherText1.toLowerCase() && selectedotherText !== otherText) {
            field1.style.display = "none";
        } else if (selectedOptionText == otherText1.toLowerCase()) {
            field1.style.display = "none";
        } else {
            field1.style.display = "block";
        }
    }

    // Function to handle changes in a select element
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

    // Function to handle changes in a group of checkboxes
    function handleCheckboxChange(checkboxClass, fieldId, inputId, otherText = "other") {
        const checkboxes = document.querySelectorAll(checkboxClass);
        const field = document.getElementById(fieldId);
        const input = document.getElementById(inputId);
        let isChecked = false;

        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                const label = checkbox.closest("label").textContent.trim().toLowerCase();
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
        }
    }

    // Function to update options for a select element based on an AJAX response
    function updateOptions(url, data, targetSelectId, defaultOptionText = "Select") {
        $.ajax({
            url: url,
            method: "POST",
            dataType: "json",
            data: data,
            success: function (options) {
                const selectElement = document.getElementById(targetSelectId);
                selectElement.innerHTML = "";
                const defaultOption = document.createElement("option");
                defaultOption.value = "";
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

    // Event listeners
    function handleNationalIdSelection() {
        const selectElement = document.getElementById("have-national-id-selection");
        const uidDiv = document.getElementById("uid-div");
        const ridDiv = document.getElementById("rid-div");
        const ridInput = document.getElementById("rid_input");
        const uidInput = document.getElementById("uid_input");
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
            ridInput.setAttribute("required", "required");
        } else {
            uidDiv.style.display = "none";
            uidInput.removeAttribute("required");
            ridDiv.style.display = "none";
            ridInput.removeAttribute("required");
        }
    }

    // Event listener for national ID selection change
    $("#have-national-id-selection").on("change", handleNationalIdSelection);

    $("#region_selection").on("change", function () {
        const regionId = this.value;
        updateOptions("/update_zone_options", {region_id: regionId}, "zon_selection");
    });

    $("#zon_selection").on("change", function () {
        const zoneId = this.value;
        updateOptions("/update_woreda_options", {zone_id: zoneId}, "woreda_selection");
    });

    $("#current_region_selection").on("change", function () {
        const regionId = this.value;
        updateOptions("/update_zone_options", {region_id: regionId}, "current_zon_selection");
    });

    $("#current_zon_selection").on("change", function () {
        const zoneId = this.value;
        updateOptions("/update_woreda_options", {zone_id: zoneId}, "current_woreda_selection");
    });

    $("#religion-select").on("change", function () {
        handleSelectChange("religion-select", "other-religion-field", "other_religion");
    });

    $("#marital_status-select").on("change", function () {
        handleSelectChange("marital_status-select", "other-marital-status-field", "other_marital_status");
    });

    $("#education-select").on("change", function () {
        handleSelectChange("education-select", "other-education-field", "other_education");
    });

    $("#mother-tongue-select").on("change", function () {
        handleSelectChange("mother-tongue-select", "other-language-field", "other_language");
    });

    $("#sleep_at_night-select").on("change", function () {
        handleSelectChange("sleep_at_night-select", "specify-sleep-field", "other_spend_night");
    });

    $(".homeless_reason-checkbox").on("change", function () {
        handleCheckboxChange(".homeless_reason-checkbox", "other_homeless-field", "other_homeless_reason");
    });

    $(".challenges_on_street-checkbox").on("change", function () {
        handleCheckboxChange(
            ".challenges_on_street-checkbox",
            "specify-challenge-field",
            "specify-challenge"
        );
    });

    $("#received_any_assistance").on("change", function () {
        selectChangeShowSection(
            "received_any_assistance",
            "inistitutes-selection",
            "other",
            "specify_inistitutes-field",
            "no"
        );
        toggleField(
            "received_any_assistance",
            "select-received_any_assistance-field",
            "specify_inistitutes-field"
        );
    });

    $("#inistitutes-selection").on("change", function () {
        handleSelectChange("inistitutes-selection", "specify_inistitutes-field", "specify_inistitutes");
    });

    $("#received_any_assistance-current").on("change", function () {
        selectChangeShowSection(
            "received_any_assistance-current",
            "select-received_any_assistance-field-current",
            "other",
            "specify_inistitutes-field-current",
            "no"
        );
        toggleField(
            "received_any_assistance-current",
            "select-received_any_assistance-field-current",
            "specify_inistitutes-field-current"
        );
    });

    $("#inistitutes-selection-current").on("change", function () {
        handleSelectChange(
            "inistitutes-selection-current",
            "specify_inistitutes-field-current",
            "specify_inistitutes-current"
        );
    });

    $("#are-you-disabled-select").on("change", function () {
        toggleField("are-you-disabled-select", "other-disability-field", "other_disability");
    });

    $("#disability-selection").on("change", function () {
        handleSelectChange("disability-selection", "specify-disability-field", "other_disability");
    });

    $("#source_income-selection").on("change", function () {
        selectChangeHideSection("source_income-selection", "pre-earn-per-field", "no income");
        selectChangeHideSection("source_income-selection", "pre-earn-amount-field", "no income");

        handleSelectChange("source_income-selection", "other-source-income-field", "other_source_income");
    });

    $("#source_income-selection-current").on("change", function () {
        selectChangeHideSection("source_income-selection-current", "earn-per-field", "no income");
        selectChangeHideSection("source_income-selection-current", "earn-amount-field", "no income");
        handleSelectChange(
            "source_income-selection-current",
            "other-source-income-field-current",
            "other_source_income-current"
        );
    });

    $("#additional_support-select").on("change", function () {
        toggleField(
            "additional_support-select",
            "specific_additional_support-field",
            "other_additional_support"
        );
    });

    $(".specific_support_options-checkbox").on("change", function () {
        handleCheckboxChange(
            ".specific_support_options-checkbox",
            "other_additional_support-field",
            "other_additional_support"
        );
    });

    $("#lang").on("change", function () {
        const field = document.getElementById("other-lang-field");
        const input = document.getElementById("other_lang");
        const selectedValues = Array.from(document.getElementById("lang").selectedOptions).map(
            (option) => option.value
        );
        if (selectedValues.includes("16")) {
            field.style.display = "block";
            input.setAttribute("required", "required");
        } else {
            field.style.display = "none";
            input.removeAttribute("required");
        }
    });

    // Trigger the change event on page load to handle the initial state
    $("#have-national-id-selection").trigger("change");
    $("#religion-select").trigger("change");
    $("#marital_status-select").trigger("change");
    $("#marital_status-select").trigger("change");
    $("#education-select").trigger("change");
    $("#mother-tongue-select").trigger("change");
    $("#sleep_at_night-select").trigger("change");
    $("#sleep_at_night-select").trigger("change");
    $(".homeless_reason-checkbox").trigger("change");
    $(".challenges_on_street-checkbox").trigger("change");
    $("#received_any_assistance").trigger("change");
    $("#inistitutes-selection").trigger("change");
    $("#received_any_assistance-current").trigger("change");
    $("#inistitutes-selection").trigger("change");
    $("#are-you-disabled-select").trigger("change");
    $("#disability-selection").trigger("change");
    $("#additional_support-select").trigger("change");
    $(".specific_support_options-checkbox").trigger("change");
    $("#source_income-selection-current").trigger("change");
    $("#source_income-selection").trigger("change");
    $("#lang").trigger("change");

    // Validation for vid and email

    const uidInput = document.getElementById("uid_input");
    const uidError = document.getElementById("uid_error");
    const form = document.getElementById("updategroupForm");
    const emailInput = document.getElementById("email");
    const emailError = document.createElement("div");
    emailError.classList.add("invalid-feedback");
    emailInput.parentNode.appendChild(emailError);

    uidInput.addEventListener("input", function () {
        if (uidInput.value.length !== 12 && uidInput.value.length !== 0) {
            uidInput.classList.add("is-invalid");
            uidError.style.display = "block";
        } else {
            uidInput.classList.remove("is-invalid");
            uidError.style.display = "none";
        }
    });
    function isValidEmail(email) {
        // Basic email regex pattern
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    emailInput.addEventListener("input", function () {
        if (emailInput.value.length !== 0) {
            if (!isValidEmail(emailInput.value)) {
                emailInput.classList.add("is-invalid");
                emailError.style.display = "block";
            } else {
                emailInput.classList.remove("is-invalid");
                emailError.style.display = "none";
            }
        } else {
            emailInput.classList.remove("is-invalid");
            emailError.style.display = "none";
        }
    });

    window.customvalidateForm = function (isCreateForm) {
        if (uidInput.value.length !== 12 && uidInput.value.length !== 0) {
            event.preventDefault(); // Prevent form submission if validation fails
            uidInput.classList.add("is-invalid");
            uidError.style.display = "block";
            const collapseElement = uidInput.closest(".collapse");
            if (collapseElement) {
                const accordionButton = document.querySelector(`[data-bs-target="#${collapseElement.id}"]`);
                if (accordionButton) {
                    accordionButton.click();
                }
            }
        } else if (!isValidEmail(emailInput.value) && emailInput.value.length !== 0) {
            emailInput.classList.add("is-invalid");
            emailError.style.display = "block";
            const collapseElement = emailInput.closest(".collapse");
            if (collapseElement) {
                const accordionButton = document.querySelector(`[data-bs-target="#${collapseElement.id}"]`);
                if (accordionButton) {
                    accordionButton.click();
                }
            }
        } else {
            uidInput.classList.remove("is-invalid");
            uidError.style.display = "none";
            emailInput.classList.remove("is-invalid");
            emailError.style.display = "none";
            this.validateForm(isCreateForm);
        }
    };
});
