from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

def create_app_related_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name=_('User Manager'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_user',
         'add_user', 'change_user', 'view_usermessage', 'change_usermessage',
         'delete_usermessage'))
        grp.permissions.set(permissions)
    grp, created = Group.objects.get_or_create(name=_('Profile Manager'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_profile',
            'change_profile', 'view_usermessage', 'change_usermessage',
            'delete_usermessage'))
        grp.permissions.set(permissions)

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        post_migrate.connect(create_app_related_groups, sender=self)
