from apps.user.models import User


class Access():
    """Authorize various access levels to datasets.
    """

    @classmethod
    def can_access_user_list(cls, self):
        """ Check if visitor is authorised to access user list."""
        return (self.request.user.role == User.COORDINATOR)


    @classmethod
    def can_access_user_detail(cls, self, id):
        """ Check if visitor is authorised to view  user details."""
        return (self.request.user.role == User.COORDINATOR) or (self.request.user.id == id)

    @classmethod
    def can_create_user(cls, self):
        """ Check if visitor is authorised to access create user."""
        return (self.request.user.role == User.COORDINATOR)

    @classmethod
    def can_update_user(cls, self, id):
        """ Check if visitor is authorised to update user."""
        return (self.request.user.role == User.COORDINATOR) or (self.request.user.id == id)

    @classmethod
    def can_delete_user(cls, self):
        """ Check if visitor is authorised to delete(make in-active) user."""
        return (self.request.user.role == User.COORDINATOR)

    @classmethod
    def can_update_user_password(cls, self, id):
        """ Check if visitor is authorised to update user password."""
        return (self.request.user.role == User.COORDINATOR) or (self.request.user.id == id)
