from django.contrib.auth.backends import BaseBackend, Permission
from .models import Customer


class AuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Customer.objects.get(email__exact=email)
        except Customer.DoesNotExist:
            return None

        if password and user.check_password(password) and user.is_active:
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None

    # def get_all_permissions(self, user_obj, obj=None):
    #     if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
    #         return set()
    #     if not hasattr(user_obj, '_perm_cache'):
    #         user_obj._perm_cache = super().get_all_permissions(user_obj)
    #     return user_obj._perm_cache
    #
    # def get_group_permissions(self, user_obj, obj=None):
    #     return True
    #
    # def _get_user_permissions(self, user_obj):
    #     return user_obj.user_permissions.all()
    #
    # def _get_permissions(self, user_obj, obj, from_name):
    #     if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
    #         return set()
    #
    #     perm_cache_name = '_%s_perm_cache' % from_name
    #     if not hasattr(user_obj, perm_cache_name):
    #         if user_obj.is_superuser:
    #             perms = Permission.objects.all()
    #         else:
    #             perms = getattr(self, '_get_%s_permissions' % from_name)(user_obj)
    #         perms = perms.values_list('content_type__app_label', 'codename').order_by()
    #         setattr(user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms})
    #     return getattr(user_obj, perm_cache_name)
    #
    # def get_user_permissions(self, user_obj, obj=None):
    #     """
    #     Return a set of permission strings the user `user_obj` has from their
    #     `user_permissions`.
    #     """
    #     return self._get_permissions(user_obj, obj, 'user')
    #
    # def has_module_perms(self, user_obj, app_label):
    #     perms = self.get_all_permissions(user_obj)
    #     return any(
    #         perm[:perm.index('.')] == app_label
    #         for perm in perms
    #     )
    #
    # def with_perm(self, perm, obj=None):
    #     users = Customer.objects.all()
    #     res = []
    #
    #     for user in users:
    #         if perm in self.get_all_permissions(user, obj):
    #             res.append(user)
    #     return res
