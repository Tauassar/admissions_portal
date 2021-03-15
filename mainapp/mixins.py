from django.contrib.auth.mixins import PermissionRequiredMixin


class PositionMixin(PermissionRequiredMixin):
    permission_groups = []

    def has_permission(self):
        if self.request.user.position in self.permission_groups:
            return True
        return False
