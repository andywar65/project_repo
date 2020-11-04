from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import gettext as _

from imap_tools import MailBox, AND
from filebrowser.base import FileObject

from blog.models import Article
from pages.models import GalleryImage
from users.models import User

def do_command():

    if not settings.FETCH_EMAILS:
        return

    HOST = settings.IMAP_HOST
    USER = settings.IMAP_USER
    PASSWORD = settings.IMAP_PWD
    PORT = settings.IMAP_PORT
    FROM = settings.IMAP_FROM

    with MailBox(HOST).login(USER, PASSWORD, 'INBOX') as mailbox:
        for message in mailbox.fetch(AND(seen=False, subject=_('articles'), ),
            mark_seen=True):
            try:
                usr = User.objects.get(email=message.from_)
                if not usr.has_perm('blog.add_article'):
                    continue
            except:
                continue
            msg = message.text
            d = {'title': _('TITLE['), 'intro': _('DESCRIPTION['),
                'body': _('TEXT['), 'date': _('DATE['),
                'tags': _('CATEGORIES['), 'notice': _('SPAM[')}
            for key, value in d.items():
                msg = msg.replace(value, '')
                d[key] = msg.split(']', 1)[0].replace('\r\n', '')
                msg = msg.split(']', 1)[1]
            try:
                d['date'] = datetime.strptime(d['date'], '%d/%m/%y')
            except:
                d['date'] = now()
            post = Article(title=d['title'], intro=d['intro'], body=d['body'],
                date=d['date'], tags=d['tags'], author=usr, notice=d['notice'] )
            try:
                post.save()
            except:
                continue
            for att in message.attachments:  # list: [Attachment objects]
                file = SimpleUploadedFile(att.filename, att.payload,
                    att.content_type)
                position = att.filename.split('-', 1)[0]
                caption = att.filename.split('-', 1)[1]
                caption = caption.rsplit('.', 1)[0]
                instance = GalleryImage(post_id=post.uuid, image=file,
                    position=position, caption=caption)
                #save the instance and upload the file
                instance.save()
                #update the filebrowse field
                instance.fb_image = FileObject(str(instance.image))
                instance.save()

class Command(BaseCommand):

    def handle(self, *args, **options):
        do_command()
