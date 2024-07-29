from odoo import api, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        # Create user and manage group membership
        user = super(ResUsers, self).create(vals)
        self._sync_user_groups(user)
        return user

    def write(self, vals):
        # Update user and manage group membership
        result = super(ResUsers, self).write(vals)
        if 'groups_id' in vals:
            # Ensure the method is called only if the user’s groups are updated
            for user in self:
                self._sync_user_groups(user)
        return result

    def _sync_user_groups(self, user):
        # Define the IDs of the specific groups
        group_to_add_id = self.env.ref('g2p_ati.group').id
        group_to_remove_id = self.env.ref('your_module.group_to_remove').id

        # Check if the user is added to the specific group
        if group_to_add_id in user.groups_id.ids:
            # If the user is added to the specific group, remove them from another specific group
            if group_to_remove_id in user.groups_id.ids:
                # Remove the user from the group_to_remove_id
                user.write({'groups_id': [(3, group_to_remove_id)]})
