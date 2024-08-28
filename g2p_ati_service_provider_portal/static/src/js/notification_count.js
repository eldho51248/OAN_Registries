document.addEventListener("DOMContentLoaded", function () {
    var toggleButton = document.getElementById("send_request_button");
    const approve = document.getElementById("approved_by");
    const reason = document.getElementById("reason");
    window.EditAcessForm = function () {
        if (reason.value.trim() != "") {
            var button = document.getElementById("send_request_buttonclick");
            button.click();
            return true;
        }
    };
});
