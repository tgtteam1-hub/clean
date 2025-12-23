from apps.user.models import User
from apps.incident.models import Incident


class Access():
    """Authorize various access levels to datasets.
    """

    @classmethod
    def can_access_incident_list(cls, self):
        """ Check if visitor is authorised to access user list."""
        return True


    @classmethod
    def can_access_incident_detail(cls, self, id):
        """ Check if visitor is authorised to view  user details."""
        return (
            (self.request.user.role in [User.COORDINATOR, User.MANAGER] ) or
            (self.request.user.id == id)
        )

    @classmethod
    def can_create_incident(cls, self):
        """ Check if visitor is authorised to access create user."""
        # return (self.request.user.role == User.COORDINATOR)
        return True

    @classmethod
    def can_update_incident(cls, self, id, approval):
        """ Check if visitor is authorised to update user."""
        return (
            (self.request.user.role == User.COORDINATOR) or
            ((self.request.user.id == id) and (2 == approval))
        )

    @classmethod
    def can_delete_incident(cls, self, id):
        """ Check if visitor is authorised to delete(make in-active) user."""
        return (
            (self.request.user.role == User.COORDINATOR) # or
            # (self.request.user.id == id)
        )
