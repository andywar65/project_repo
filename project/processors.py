from django.conf import settings

def get_global_settings(request):
    website = {'name': settings.WEBSITE_NAME,
        'acro': settings.WEBSITE_ACRO,
        'facebook': settings.FB_LINK,
        'insta': settings.INSTA_LINK,
        'linked': settings.IN_LINK,
        'github': settings.GITHUB_LINK,
        'external': settings.EXT_LINK,
        }
    return {'website': website, }
