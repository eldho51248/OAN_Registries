function checkFarmingType(farmingTypeSelection) {
    var selectedOption = farmingTypeSelection.options[farmingTypeSelection.selectedIndex];
    var selectedFarmingType = selectedOption.textContent.trim();

    const membershipRequiredFields = document.getElementsByClassName("membership_required_field");
    const membershipAstrix = document.getElementsByClassName("membership_astrix");
    const landRequiredFields = document.getElementsByClassName("land_required_field");
    const landAstrix = document.getElementsByClassName("land_astrix");

    const landNext = document.getElementById("land-next");
    const cropNext = document.getElementById("crop-next");
    const livestockNext = document.getElementById("livestock-next");
    const livestockPrev = document.getElementById("livestock-previous");
    const resourcePrev = document.getElementById("resource-previous");
    const agriPrev = document.getElementById("agricultural-previous");

    if (selectedFarmingType === "Crop Farming" || selectedFarmingType === "Mixed Farming") {
        // Membership
        Array.from(membershipAstrix).forEach((element) => {
            element.textContent = " *";
        });
        Array.from(membershipRequiredFields).forEach((element) => {
            element.setAttribute("required", "required");
        });

        // Land Information
        Array.from(landAstrix).forEach((element) => {
            element.textContent = " *";
        });
        Array.from(landRequiredFields).forEach((element) => {
            element.setAttribute("required", "required");
        });

        landNext.setAttribute("onclick", "showModalSection('crop-information', 'land-information',  'next')");
        resourcePrev.setAttribute(
            "onclick",
            "showModalSection('agricultural-input', 'access-to-resource',  'prev')"
        );
    }

    if (selectedFarmingType === "Crop Farming") {
        cropNext.setAttribute(
            "onclick",
            "showModalSection('agricultural-input', 'crop-information',  'next')"
        );
        agriPrev.setAttribute(
            "onclick",
            "showModalSection('crop-information', 'agricultural-input',  'prev')"
        );
    } else if (selectedFarmingType === "Livestock Farming") {
        // Membership
        Array.from(membershipAstrix).forEach((element) => {
            element.textContent = "";
        });
        Array.from(membershipRequiredFields).forEach((element) => {
            element.removeAttribute("required");
        });

        // Land Information
        Array.from(landAstrix).forEach((element) => {
            element.textContent = "";
        });
        Array.from(landRequiredFields).forEach((element) => {
            element.removeAttribute("required");
        });

        // Hide some sections
        landNext.setAttribute(
            "onclick",
            "showModalSection('livestock-information', 'land-information',  'next')"
        );
        livestockPrev.setAttribute(
            "onclick",
            "showModalSection('land-information', 'livestock-information',  'prev')"
        );
        livestockNext.setAttribute(
            "onclick",
            "showModalSection('access-to-resource', 'livestock-information',  'next')"
        );
        resourcePrev.setAttribute(
            "onclick",
            "showModalSection('livestock-information', 'access-to-resource',  'prev')"
        );
    } else if (selectedFarmingType === "Mixed Farming") {
        cropNext.setAttribute(
            "onclick",
            "showModalSection('livestock-information', 'crop-information',  'next')"
        );
        livestockPrev.setAttribute(
            "onclick",
            "showModalSection('crop-information', 'livestock-information',  'prev')"
        );
        livestockNext.setAttribute(
            "onclick",
            "showModalSection('agricultural-input', 'livestock-information',  'next')"
        );
        agriPrev.setAttribute(
            "onclick",
            "showModalSection('livestock-information', 'agricultural-input',  'prev')"
        );
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Initial check on page load
    const farmingTypeSelect = document.getElementById("farming-type-selection");
    checkFarmingType(farmingTypeSelect);
});
