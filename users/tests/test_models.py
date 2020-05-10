from django.test import TestCase

from users.models import User, Profile, UserMessage

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # user andywar65 with id = 1 already created in blog test suite
        User.objects.create(username='andy.war65', password='P4s5W0r6',
            first_name='Andrea', last_name='Guerra', email='andy@war.com')
        User.objects.create(username='rawydna56', password='P4s5W0r6',)
        profile = Profile.objects.get(pk=2)
        profile.avatar = 'uploads/users/avatar.jpg'
        profile.save()
        user = User.objects.get(id = 2)
        UserMessage.objects.create(user=user, subject='Foo', body='Bar')
        UserMessage.objects.create(nickname='Nick Name', email='me@example.com',
            subject='Foo', body='Bar')

    def test_user_get_full_name(self):
        user = User.objects.get(id = 2)
        self.assertEquals(user.get_full_name(), 'Andrea Guerra')

    def test_user_get_full_username(self):
        user = User.objects.get(id = 3)
        self.assertEquals(user.get_full_name(), 'rawydna56')

    def test_user_get_short_name(self):
        user = User.objects.get(id = 2)
        self.assertEquals(user.get_short_name(), 'Andrea')

    def test_user_get_short_username(self):
        user = User.objects.get(id = 3)
        self.assertEquals(user.get_short_name(), 'rawydna56')

    def test_profile_get_full_name(self):
        profile = Profile.objects.get(pk = 2)
        self.assertEquals(profile.get_full_name(), 'Andrea Guerra')

    def test_profile_get_full_username(self):
        profile = Profile.objects.get(pk = 3)
        self.assertEquals(profile.get_full_name(), 'rawydna56')

    def test_profile_str_full_name(self):
        profile = Profile.objects.get(pk = 2)
        self.assertEquals(profile.__str__(), 'Andrea Guerra')

    def test_profile_str_username(self):
        profile = Profile.objects.get(pk = 3)
        self.assertEquals(profile.__str__(), 'rawydna56')

    def test_profile_get_thumb(self):
        profile = Profile.objects.get(pk = 2)
        # here extracting path from FileObject for convenience
        self.assertEquals(profile.get_thumb().path, 'uploads/users/avatar.jpg')

    def test_profile_get_no_thumb(self):
        profile = Profile.objects.get(pk = 3)
        self.assertEquals(profile.get_thumb(), None)

    def test_user_message_get_full_name(self):
        message = UserMessage.objects.get(id = 1)
        self.assertEquals(message.get_full_name(), 'Andrea Guerra')

    def test_user_message_get_nickname(self):
        message = UserMessage.objects.get(id = 2)
        self.assertEquals(message.get_full_name(), 'Nick Name')

    def test_user_message_get_user_email(self):
        message = UserMessage.objects.get(id = 1)
        self.assertEquals(message.get_email(), 'andy@war.com')

    def test_user_message_get_nickname_email(self):
        message = UserMessage.objects.get(id = 2)
        self.assertEquals(message.get_email(), 'me@example.com')

    def test_user_message_str_method(self):
        message = UserMessage.objects.get(id = 1)
        self.assertEquals(message.__str__(), 'Messaggio - 1')
