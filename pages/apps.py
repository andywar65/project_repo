from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

def create_app_related_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name=_('Page Makers'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_homepage',
         'add_homepage', 'change_homepage', 'delete_homepage', 'view_treepage',
         'add_treepage', 'change_treepage', 'delete_treepage',
         'view_galleryimage', 'add_galleryimage', 'change_galleryimage',
         'delete_galleryimage'))
        grp.permissions.set(permissions)

class PagesConfig(AppConfig):
    name = 'pages'

    def ready(self):
        post_migrate.connect(create_app_related_groups, sender=self)
