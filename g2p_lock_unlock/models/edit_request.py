import json

from odoo import fields, models

from ..json_encoder import CustomJSONEncoder


class ResPartner(models.Model):
    _inherit = "res.partner"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    approval_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        track_visibility="onchange",
    )

    edit_state = fields.Selection(selection=[("open", "Open"), ("locked", "Locked")], default="open")

    edit_count = fields.Integer(default=0)

    update_request_ids = fields.One2many("res.partner.change.request", "partner_id", string="Update Requests")
    edit_suggestion_ids = fields.One2many("request", "record_id", string="Edit Suggestions")

    def _filter_json_compatible(self, vals):
        """
        Filters out fields with non-JSON-serializable data and returns a message indicating the changes.
        """
        filtered_vals = {}
        change_messages = []

        # Get the current user
        current_user = self.env.user.name

        for key, new_value in vals.items():
            field = self._fields.get(key)
            if field and isinstance(field, fields.Binary):
                # Skip binary fields
                continue

            try:
                # Attempt to serialize the value to JSON to check if it's compatible
                json.dumps(new_value)
                filtered_vals[key] = new_value

                # Retrieve the old value from the record
                old_value = self[key]

                # Format both values for the message
                old_value_str = str(old_value)
                new_value_str = str(new_value)

                # Create the change message
                change_message = (
                    f"User {current_user} wants to change the field '{field.string}' "
                    f"from '{old_value_str}' to '{new_value_str}'."
                )
                change_messages.append(change_message)
            except (TypeError, ValueError):
                # If serialization fails, skip the field
                continue

        # Combine all change messages into a single string
        change_message_str = " ".join(change_messages)
        return change_message_str

    def write(self, vals):
        no_of_edits = self.env["no.of.edits"].search([])
        json_compatible_vals = self._filter_json_compatible(vals)
        user = self.env.user

        for record in self:
            if record.edit_count >= no_of_edits.edit_amount - 1:
                vals["edit_state"] = "locked"
            vals["edit_count"] = record.edit_count + 1

        if (
            self.env.context.get("bypass_write")
            or record.edit_state != "locked"
            or self.env.is_superuser()
            or user.has_group("g2p_ati.group_data_validator")
            or user.has_group("g2p_registry_base.group_g2p_admin")
        ):
            # Allow write operations if the bypass context is set
            return super().write(vals)
        else:
            # Create a change request for each record that is being updated
            for partner in self:
                self.env["res.partner.change.request"].create(
                    {
                        "partner_id": partner.id,
                        "new_values": CustomJSONEncoder.python_dict_to_json_dict(vals),
                        "update_message": json_compatible_vals,
                        "state": "pending",
                    }
                )
                # Return a meaningful value; for example, the count of records 'affected'
            return len(self)


class ResPartnerChangeRequest(models.Model):
    _name = "res.partner.change.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "partner_id"

    _description = "Update Request"

    name = fields.Char(string="Request")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    # new_values = fields.Text(string="New Values", required=True)
    requested_by = fields.Many2one("res.users", default=lambda self: self.env.user)
    validator = fields.Many2one("res.users")
    new_values = fields.Json(string="Changes", required=True)
    update_message = fields.Char(string="Message", required=True)
    new_values_display = fields.Char(string="New Values (Preview)", compute="_compute_new_values_display")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
        string="Status",
    )

    def create(self, vals):
        # Create the change request record
        change_request = super().create(vals)

        # Find the group by external ID (replace with your actual group ID)
        group = self.env.ref("g2p_ati.group_data_validator")  # Replace with the actual module and group name
        if group:
            users = group.users
            for user in users:
                # Send notification to each user in the group
                self.env["mail.activity"].create(
                    {
                        "activity_type_id": self.env.ref(
                            "mail.mail_activity_data_todo"
                        ).id,  # Todo activity type
                        "res_model_id": self.env["ir.model"]
                        .search([("model", "=", "res.partner.change.request")])
                        .id,
                        "res_id": change_request.id,  # The record ID of the res.partner.change.request
                        "user_id": user.id,
                        "date_deadline": fields.Date.context_today(self),  # Deadline in 3 days
                        "summary": "New Partner Change Request",
                        "note": "A new request has been created. Please review and approve it.",
                    }
                )

        return change_request

    def _compute_new_values_display(self):
        for record in self:
            try:
                # Convert JSON to a pretty-printed string for display
                record.new_values_display = json.dumps(record.new_values, indent=2)
            except Exception:
                record.new_values_display = "Error displaying JSON"

    def approve_changes(self):
        for request in self:
            try:
                # Safely parse the new_values string to a dictionary
                new_vals = request.new_values
                if isinstance(new_vals, dict):
                    # Apply the new values directly using the super method
                    request.partner_id.with_context(bypass_write=True).sudo().write(new_vals)
                    # Mark the request as approved
                    request.state = "approved"
                    # Add the user who validated (approved) the request
                    request.validator = self.env.user
                    # Log the applied changes for debugging
                    request.partner_id.message_post(body=f"Changes approved and applied: {new_vals}")
                else:
                    raise ValueError("Parsed new_values is not a dictionary")
            except Exception as e:
                # Handle any exceptions and log them for debugging
                request.state = "rejected"
                request.validator = self.env.user  # The user who validated (rejected)
                request.partner_id.message_post(body=f"Failed to apply changes: {str(e)}")
                # Optionally, raise the exception if you want to handle it at a higher level
                raise
        activities = self.env["mail.activity"].search(
            [
                ("res_model", "=", "res.partner.change.request"),
                ("res_id", "in", self.ids),
                ("user_id", "=", self.env.user.id),
            ]
        )

        # Mark the activities as done or unlink them (remove them)
        activities.action_done()

    def reject_changes(self):
        for request in self:
            try:
                # Safely parse the new_values string to a dictionary
                new_vals = request.new_values
                if isinstance(new_vals, dict):
                    # Mark the request as approved
                    request.state = "rejected"
                    request.validator = self.env.user  # The user who validated (rejected)
                    # Log the applied changes for debugging
                    request.partner_id.message_post(body=f"Changes Rejected Please Try again: {new_vals}")
                else:
                    raise ValueError("Parsed new_values is not a dictionary")
            except Exception as e:
                # Handle any exceptions and log them for debugging
                request.state = "rejected"
                request.validator = self.env.user  # The user who validated (rejected)
                request.partner_id.message_post(body=f"Failed to apply changes: {str(e)}")

        activities = self.env["mail.activity"].search(
            [
                ("res_model", "=", "res.partner.change.request"),
                ("res_id", "in", self.ids),
                ("user_id", "=", self.env.user.id),
            ]
        )
        # Mark the activities as done or unlink them (remove them)
        activities.action_done()
