import os

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User, Profile, UserMessage

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='andy.war65', password='P4s5W0r6',
            first_name='Andrea', last_name='Guerra', email='andy@war.com')
        #next save is just for coverage purposes
        user.save()
        profile = user.profile
        profile.avatar = 'uploads/users/avatar.jpg'
        profile.save()
        User.objects.create(username='rawydna56', password='P4s5W0r6',)
        UserMessage.objects.create(id=17, user=user, subject='Foo', body='Bar',
            )
        UserMessage.objects.create(id=18, nickname='Nick Name',
            email='me@example.com', subject='Foo', body='Bar')

    def test_user_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.get_full_name(), 'Andrea Guerra')

    def test_user_get_full_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.get_full_name(), 'rawydna56')

    def test_user_get_short_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.get_short_name(), 'Andrea')

    def test_user_get_short_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.get_short_name(), 'rawydna56')

    def test_profile_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        profile = Profile.objects.get(pk=user.uuid)
        self.assertEquals(profile.get_full_name(), 'Andrea Guerra')

    def test_profile_get_full_username(self):
        user = User.objects.get(username='rawydna56')
        profile = Profile.objects.get(pk=user.uuid)
        self.assertEquals(profile.get_full_name(), 'rawydna56')

    def test_profile_str_full_name(self):
        user = User.objects.get(username='andy.war65')
        profile = Profile.objects.get(pk=user.uuid)
        self.assertEquals(profile.__str__(), 'Andrea Guerra')

    def test_profile_str_username(self):
        user = User.objects.get(username='rawydna56')
        profile = Profile.objects.get(pk=user.uuid)
        self.assertEquals(profile.__str__(), 'rawydna56')

    def test_profile_get_thumb(self):
        user = User.objects.get(username='andy.war65')
        profile = Profile.objects.get(pk=user.uuid)
        # here extracting path from FileObject for convenience
        self.assertEquals(profile.get_thumb().path, 'uploads/users/avatar.jpg')

    def test_profile_get_no_thumb(self):
        user = User.objects.get(username='rawydna56')
        profile = Profile.objects.get(pk=user.uuid)
        self.assertEquals(profile.get_thumb(), None)

    def test_user_message_get_full_name(self):
        message = UserMessage.objects.get(id = 17)
        self.assertEquals(message.get_full_name(), 'Andrea Guerra')

    def test_user_message_get_nickname(self):
        message = UserMessage.objects.get(id = 18)
        self.assertEquals(message.get_full_name(), 'Nick Name')

    def test_user_message_get_user_email(self):
        message = UserMessage.objects.get(id = 17)
        self.assertEquals(message.get_email(), 'andy@war.com')

    def test_user_message_get_nickname_email(self):
        message = UserMessage.objects.get(id = 18)
        self.assertEquals(message.get_email(), 'me@example.com')

    def test_user_message_str_method(self):
        message = UserMessage.objects.get(id = 17)
        self.assertEquals(message.__str__(), 'Messaggio - 17')

class UserMessageModelTest(TestCase):
    """Testing methods that need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='test-directory', password='P4s5W0r6',)
        UserMessage.objects.create(id=19, user=user, subject='Foo', body='Bar',
            attachment = SimpleUploadedFile('file.txt', b'Foo Bar',
            'text/plain'))

    def tearDown(self):
        """Checks existing files, then removes them"""
        list = os.listdir(os.path.join(settings.PRIVATE_STORAGE_ROOT,
            'users/test-directory'))
        for file in list:
            os.remove(os.path.join(settings.PRIVATE_STORAGE_ROOT,
                f'users/test-directory/{file}'))

    def test_user_message_directory(self):
        message = UserMessage.objects.get(id = 19)
        #first we test if the directory is correct
        self.assertEquals(str(message.attachment).split('_')[0],
            'users/test-directory/file')
        #then we test if random suffix was added
        self.assertEquals(len(str(message.attachment).split('_')[1]), 11)
