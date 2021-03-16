from django.contrib.auth.mixins import PermissionRequiredMixin


class PositionMixin(PermissionRequiredMixin):
    permission_groups = []

    def has_permission(self):
        if self.request.user.position in self.permission_groups \
                or self.request.user.is_superuser:
            return True
        return False
