from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

def create_app_related_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name=_('Trusted'))
    if created:
        permission = Permission.objects.filter(codename="add_userupload")
        grp.permissions.set(permission)
    grp, created = Group.objects.get_or_create(name=_('Editors'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_article',
         'add_article', 'change_article', 'delete_article', 'view_userupload',
         'add_userupload', 'change_userupload', 'delete_userupload',
         'view_galleryimage', 'add_galleryimage', 'change_galleryimage',
         'delete_galleryimage'))
        grp.permissions.set(permissions)

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        post_migrate.connect(create_app_related_groups, sender=self)
