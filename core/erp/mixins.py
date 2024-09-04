from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class MultiPermissionRequiredMixin(AccessMixin):
    permissions = []

    def handle_no_permission(self):
        return redirect('erp:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        for perm in self.permissions:
            if not request.user.has_perm(perm):
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
