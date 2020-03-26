from django.conf import settings

def get_global_settings(request):
    website = {'name': settings.WEBSITE_NAME,
        'acro': settings.WEBSITE_ACRO, }
    return {'website': website, }
