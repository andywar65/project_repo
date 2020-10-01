from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_trusted_group(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    obj, created = Group.objects.get_or_create(name='Trusted')
    pass

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        post_migrate.connect(create_trusted_group, sender=self)
