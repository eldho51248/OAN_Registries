$(document).ready(function () {
    window.customvalidateFormGroup = function (isCreateFrom) {
        console.log("customvalidateFormGroup");
        const locationDetailsSection = document.querySelector("#location-details");
        const requiredFields = locationDetailsSection.querySelectorAll("[required]");
        console.log(requiredFields);
        
    }
});


let memberCount = 0;

function addFamilyMember() {
    const givenName = document.getElementById('mamber_given_name').value;
    const fathersName = document.getElementById('member_fathers_name').value;
    const grandfathersName = document.getElementById('member_grandfathers_name').value;
    const birthdate = document.getElementById('member-birthdate').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;

    if (givenName && fathersName && grandfathersName && birthdate && gender) {
        const table = document.getElementById('familylist').getElementsByTagName('tbody')[0];

        const newRow = table.insertRow();
        newRow.innerHTML = `
            <td><input type="hidden" name="member_given_name_${memberCount}" value="${givenName}">${givenName}</td>
            <td><input type="hidden" name="member_fathers_name_${memberCount}" value="${fathersName}">${fathersName}</td>
            <td><input type="hidden" name="member_grandfathers_name_${memberCount}" value="${grandfathersName}">${grandfathersName}</td>
            <td><input type="hidden" name="member_birthdate_${memberCount}" value="${birthdate}">${birthdate}</td>
            <td><input type="hidden" name="gender_${memberCount}" value="${gender}">${gender}</td>
            <td><button type="button" class="btn btn-outline-secondary btn-sm" onclick="deleteMember(this)"><i class="fas fa-trash-alt"></i></button></td>
        `;

        memberCount++;

        // Clear the form fields
        document.getElementById('mamber_given_name').value = '';
        document.getElementById('member_fathers_name').value = '';
        document.getElementById('member_grandfathers_name').value = '';
        document.getElementById('member-birthdate').value = '';
        document.querySelectorAll('input[name="gender"]').forEach((el) => { el.checked = false; });

        $('#familyMemberModal').modal('hide');
    } else {
        alert('Please fill all the required fields');
    }
}

function deleteMember(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

let farmerCount = 0;

function addFarmerMember() {
    const givenName = document.getElementById('mamber_given_name').value;
    const fathersName = document.getElementById('member_fathers_name').value;
    const grandfathersName = document.getElementById('member_grandfathers_name').value;
    const birthdate = document.getElementById('member-birthdate').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;

    if (givenName && fathersName && grandfathersName && birthdate && gender) {
        const table = document.getElementById('familylist').getElementsByTagName('tbody')[0];

        const newRow = table.insertRow();
        newRow.innerHTML = `
            <td><input type="hidden" name="member_given_name_${farmerCount}" value="${givenName}">${givenName}</td>
            <td><input type="hidden" name="member_fathers_name_${farmerCount}" value="${fathersName}">${fathersName}</td>
            <td><input type="hidden" name="member_grandfathers_name_${farmerCount}" value="${grandfathersName}">${grandfathersName}</td>
            <td><input type="hidden" name="member_birthdate_${farmerCount}" value="${birthdate}">${birthdate}</td>
            <td><input type="hidden" name="gender_${farmerCount}" value="${gender}">${gender}</td>
            <td><button type="button" class="btn btn-outline-secondary btn-sm" onclick="deleteMember(this)"><i class="fas fa-trash-alt"></i></button></td>
        `;

        memberCount++;

        // Clear the form fields
        document.getElementById('mamber_given_name').value = '';
        document.getElementById('member_fathers_name').value = '';
        document.getElementById('member_grandfathers_name').value = '';
        document.getElementById('member-birthdate').value = '';
        document.querySelectorAll('input[name="gender"]').forEach((el) => { el.checked = false; });

        $('#familyMemberModal').modal('hide');
    } else {
        alert('Please fill all the required fields');
    }
}

function populateEditModal(id, givenName, fathersName, grandfathersName, birthdate, gender) {
    console.log("populate");
    // $('#editFamilyMemberModal').modal('show');

    // console.log('populateEditModal called with:', id, givenName, fathersName, grandfathersName, birthdate, gender);

    // document.getElementById('edit_given_name').value = givenName;
    // document.getElementById('edit_fathers_name').value = fathersName;
    // document.getElementById('edit_grandfathers_name').value = grandfathersName;
    // document.getElementById('edit_birthdate').value = birthdate;

    // const genderRadio = document.querySelector(`input[name="edit_gender"][value="${gender}"]`);
    // if (genderRadio) {
    //     genderRadio.checked = true;
    // } else {
    //     console.error('Gender radio button not found');
    // }

    // document.getElementById('update_member').setAttribute('data-id', id);
}



// function updateFamilyMember() {
//     const id = document.getElementById('update_member').getAttribute('data-id');
//     const givenName = document.getElementById('edit_given_name').value;
//     const fathersName = document.getElementById('edit_fathers_name').value;
//     const grandfathersName = document.getElementById('edit_grandfathers_name').value;
//     const birthdate = document.getElementById('edit_birthdate').value;
//     const gender = document.querySelector('input[name="edit_gender"]:checked').value;

//     if (givenName && fathersName && grandfathersName && birthdate    && gender) {
//         // Handle updating logic here, e.g., AJAX request to update data
//         console.log(`Updating member ${id}: ${givenName}, ${fathersName}, ${grandfathersName}, ${birthdate}, ${gender}`);

//         $('#editFamilyMemberModal').modal('hide');
//     } else {
//         alert('Please fill all the required fields');
//     }
// }





//this is to populate the data for editing family member

$(document).on("click", "#hh_member_update", function () {
    // console.log('populateEditModal called');
    var memberId = $(this).attr("store");
    var modal = $("#editFamilyMemberModal");
    console.log("Click edit", memberId);
    $.ajax({
        url: "/serviceprovider/member/update/",
        method: "POST",
        data: {
            member_id: memberId,
        },
        dataType: "json",
        success: function (response) {
            modal.find("#edit_given_name").val(response.given_name);
            modal.find("#edit_fathers_name").val(response.family_name);
            modal.find("#edit_grandfathers_name").val(response.gf_name_eng);
            modal.find("#edit_birthdate").val(response.dob);
            if (response.gender == "male") {
                modal.find("#edit_gender_male").prop('checked', true);
            }
            else if (response.gender == "female") {
                modal.find("#edit_gender_female").prop('checked', true);
            }

            console.log();
            var ele = document.getElementById("update-member-btn")
            ele.setAttribute("store", memberId);
            // ele.setAttribute("id", "update-member-btn");


            // $("#update_member").replaceWith(
            //     '<div id="update-member-btn" store="' +
            //         memberId +
            //         '" class="btn btn-primary create-new">Update</div>'
            // );

            modal.modal("show");
            // $("#update_member").replaceWith(
            //                 '<div id="update-member-btn" store="' +
            //                     memberId +
            //                     '" class="btn btn-primary create-new">Updatee</div>'
            //             );
            
        },
        error: function (error) {
            console.error("Ajax request failed");
            console.error("Error:", error);
        },
    }); 
});



$(document).on("click", "#update-member-btn", function () {
    // console.log("HERE this is for editing");

    var ele = document.getElementById("update-member-btn");
    var modal = $("#editFamilyMemberModal");
    var memberId = ele.getAttribute('store');

    var group_id = $("input[name='group_id']").val();
    // console.log(memberId)

    var data = {
        group_id: group_id,
        member_id: memberId,
        given_name: modal.find("#edit_given_name").val(),
        family_name: modal.find("#edit_fathers_name").val(),
        gf_name_eng: modal.find("#edit_grandfathers_name").val(),
        birthdate: modal.find("#edit_birthdate").val(),
        gender: modal.find("input[name='gender']:checked").val(),
        // relationship: modal.find("select[name='relationship']").val() 
    };

    // console.log("Sending data:", data);
    console.log("Click update", memberId);

    $.ajax({
        url: "/serviceprovider/family_member/update/submit/",
        method: "POST",
        data: data,
        dataType: "json",
        success: function (response) {
            // console.log("Ajax request successful");
            // console.log("Response:", response);
            if (response.member_list) {
                // Update the table with the new member list
                var tableBody = $("#familylist tbody");
                tableBody.empty();
                response.member_list.forEach(function (member, index) {
                    var newRowHtml = `
                        <tr>
                            <td>${member.name}</td>
                            <td>${member.gender}</td>
                            <td>${member.birthdate}</td>
                        

                            <td>${member.active ? "Active" : "Inactive"}</td>
                            <td>
                                <button type="button" class="btn btn-icon rounded-0" id="hh_member_update" store="${member.id}" title="Edit" data-bs-toggle="modal" data-bs-target="#editFamilyMemberModal">
                                    <i class="fa fa-pencil"></i>
                                </button>
                                <button type="button" class="btn btn-outline-secondary btn-sm my-3" onclick="deleteMember(this)">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                    tableBody.append(newRowHtml);
                });
    
                // Hide the modal after successful submission
                $("#editFamilyMemberModal").modal("hide");
               
            } else {
                console.error("Failed to edit family member");
            }
        },
        
        error: function (error) {
            console.error("Ajax request failed");
            console.error("Error:", error);
        }
    });
});


/// Add button
$(document).on("click", "#family_member_submit", function () {
    console.log("Add button in update household")
    var group_id = $("input[name='group_id']").val();
    var given_name = $("#mamber_given_name").val();
    var family_name = $("#member_fathers_name").val();
    var gf_name_eng = $("#member_grandfathers_name").val();
    var birthdate = $("#member-birthdate").val();
    var gender = $("input[name='gender']:checked").val();  // Use :checked to get the selected radio button
    // var relationship =$("select[name='relation_with_household_head_add']").val(); 

    
    var isValid = true;
    $(".form-control, .form-check-input").removeClass("is-invalid");
    
    if (!given_name || !family_name || !gf_name_eng || !birthdate || !gender ) {
        isValid = false;
        $("#family-member-template .form-control[required], #family-member-template .form-check-input[required]").each(function () {
            if (!$(this).val()) {
                $(this).addClass("is-invalid");
            }
        });
    }
    
    if (!isValid) {
        showToast("Please fill out all required fields.");
        return;
    }
    
    // Proceed with the AJAX request if the form is valid
    $.ajax({
        url: "/serviceprovider/family_member/add/submit/",
        method: "POST",
        data: {
            group_id: group_id,
            given_name: given_name,
            family_name: family_name,
            gf_name_eng: gf_name_eng,
            birthdate: birthdate,
            gender: gender,
            // relationship:relationship
        },
        dataType: "json",
        success: function (response) {
            console.log("Ajax request successful");
            console.log("Response:", response);
            if (response.member_list) {
                // Update the table with the new member list
                var tableBody = $("#familylist tbody");
                tableBody.empty();
                response.member_list.forEach(function (member, index) {
                    var newRowHtml = `
                        <tr>
                            <td>${member.name}</td>
                            <td>${member.gender}</td>
                            <td>${member.birthdate}</td>
                        

                            <td>${member.active ? "Active" : "Inactive"}</td>
                            <td>
                                <button type="button" class="btn btn-icon rounded-0" id="hh_member_update" store="${member.id}" title="Edit">
                                    <i class="fa fa-pencil"></i>
                                </button>
                                <button type="button" class="btn btn-outline-secondary btn-sm my-3" onclick="deleteMember(this)">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                    tableBody.append(newRowHtml);
                });
    
                // Hide the modal after successful submission
                $("#familyMemberModal").modal("hide");
            } else {
                console.error("Failed to add family member");
            }
        },
        error: function (error) {
            console.error("request failed");
            console.error("Error:", error);
        }
    });
    
});
    

function showNextModal(nextSectionId, currentSectionId) {

    val = true

    if (val) {
        var activeLink = document.querySelector(".sidebar .nav-link.active");

        var nextLink = activeLink.parentElement.nextElementSibling.querySelector(".nav-link");
        if (nextLink) {
            nextLink.classList.remove("disabled");
            showSection(nextSectionId, nextLink, true);
        }
    }
}

function showFamilyModal(nextSectionId, currentSectionId) {

    val = true

    if (val) {
        var activeLink = document.querySelector(".sidebar .nav-link.active");

        var nextLink = activeLink.parentElement.nextElementSibling.querySelector(".nav-link");
        if (nextLink) {
            nextLink.classList.remove("disabled");
            showSectionFamily(nextSectionId, nextLink, true);
        }
    }
}


function showModalSection(nextSectionId, currentSectionId, direction) {
        console.log("Show Modal Section")
    val = true;

    if (val) {
        var activeLink = document.querySelector(".sidebar .nav-link.active");
        // console.log(activeLink);
        // var targetLink = false;
        // if (direction === 'next') {
        //     targetLink = activeLink.parentElement.nextElementSibling?.querySelector(".nav-link");
        // } else if (direction === 'prev') {
        //     targetLink = activeLink.parentElement.previousElementSibling?.querySelector(".nav-link");
        // }

        // if (targetLink) {
        //     targetLink.classList.remove("disabled");
        // }
        showSection(nextSectionId, activeLink, true);
    }
}
