/** @odoo-module */
import {FormController} from "@web/views/form/form_controller";
import {formView} from "@web/views/form/form_view";
import {registry} from "@web/core/registry";
const {useEffect} = owl;

class ResPartnerFormOtherGroupController extends FormController {
    setup() {
        super.setup();

        useEffect(() => {
            if (!this.model.root.data.is_group && this.model.root.data.primary_Language) {
                console.log("in here");

                const containers = document.querySelectorAll(".o_horizontal_separator");

                for (const container of containers) {
                    if (container.innerText.trim().toLowerCase() === "other".toLowerCase()) {
                        console.log("in here");
                        container.innerText = this.model.root.data.primary_Language["1"];
                        break;
                    }
                }
            }
        });
    }
}

const resPartnerFormOtherGroupView = {
    ...formView,
    Controller: ResPartnerFormOtherGroupController,
};

registry.category("views").add("res_partner_other_group_string", resPartnerFormOtherGroupView);

// Class ResPartnerFormController extends FormController {
//     setup(){
//       jhfhkgfhgfhjgdgfdgdg
//         super.setup()

//         useEffect(()=>{
//             // const divElement = document.querySelector('.o_horizontal_separator.mt-4.mb-3.text-uppercase.fw-bolder.small');
//                 adsf
//             // if (divElement) {
//             //     divElement.innerText = "this.model.root.data.primary_Language[1]";
//             // }
//             this.disableForm()
//         }, ()=>[this.model.root.data.state])

//         this.onNotebookPageChange = (notebookId, page) => {
//             this.disableForm()
//         };
//     }

//     disableForm(){

//         console.log(this.model.root.data)

//         const divElement = document.querySelector('.o_horizontal_separator.mt-4.mb-3.text-uppercase.fw-bolder.small');

//         if (divElement) {
//             divElement.innerText = "this.model.root.data.primary_Language[1]";

//         // if (this.model.root.data.state == 'locked'){
//         //     if (inputs) inputs.forEach(e => e.setAttribute("disabled", 1))
//         //     if (widgets) widgets.forEach(e => e.classList.add("pe-none"))
//         //     this.canEdit = false
//         // } else {
//         //     if (inputs) inputs.forEach(e => e.removeAttribute("disabled"))
//         //     if (widgets) widgets.forEach(e => e.classList.remove("pe-none"))
//         //     this.canEdit = true
//         }
//     }

//     async beforeLeave() {
//         if (this.model.root.data.primary_Language != 'locked') return
//         super.beforeLeave()
//     }

//     async beforeUnload(ev) {
//         if (this.model.root.data.primary_Language != 'locked') return
//         super.beforeUnload(ev)
//     }
// }

// const resPartnerFormView = {
//     ...formView,
//     Controller: ResPartnerFormController,
// }

// registry.category("views").add("res_partner_form_disable", resPartnerFormView)
