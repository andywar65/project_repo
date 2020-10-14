from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_trusted_group(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name='Trusted')
    if created:
        permission = Permission.objects.filter(codename="add_userupload")
        grp.permissions.set(permission)

def create_editor_group(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name='Editors')
    if created:
        permissions = Permission.objects.filter(codename__in=('view_article',
         'add_article', 'change_article', 'delete_article', 'view_userupload',
         'add_userupload', 'change_userupload', 'delete_userupload'))
        grp.permissions.set(permissions)

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        post_migrate.connect(create_trusted_group, sender=self)
        post_migrate.connect(create_editor_group, sender=self)
