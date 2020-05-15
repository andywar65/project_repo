from django.test import TestCase
from django.urls import reverse

from users.models import User

class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='existing', password='P4s5W0r6',
            email='me@existing.com')

    def test_registration_view_status_code(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

    def test_registration_view_template(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_view_post_status_code(self):
        with self.settings(RECAPTCHA_TEST_MODE = True):
            response = self.client.post('/registration/', {'username':'new_guy',
                'email':'new@guy.com', 'privacy': True, })
            self.assertEqual(response.status_code, 200 )

    def test_contact_view_status_code(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_template_not_logged(self):
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'users/message.html')

    def test_contact_view_template_logged(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'users/message_log.html')

    def test_contact_view_message_logged_post_status_code(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        response = self.client.post(reverse('contacts'), {'subject': 'Foo',
            'body': 'Bar'})
        self.assertEqual(response.status_code, 302 )

    def test_contact_view_message_logged_post_status_code_subject(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        response = self.client.post('/contacts/?subject=Foo', {
            'body': 'Bar'})
        self.assertEqual(response.status_code, 200 )

    def test_contact_view_message_logged_post_status_code_recipient(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        usr = User.objects.get(username='existing')
        response = self.client.post(f'/contacts/?recipient={usr.id}', {
            'subject': 'Foo', 'body': 'Bar'})
        self.assertEqual(response.status_code, 302 )

    def test_login_view_next_logout(self):
        response = self.client.post('/accounts/login/?next=/accounts/logout/',
            {'username':'existing', 'password':'P4s5W0r6'})
        self.assertRedirects(response, '/accounts/profile/')

    def test_login_view_next_deleted(self):
        response = self.client.post('/accounts/login/?next=/accounts/profile/deleted',
            {'username':'existing', 'password':'P4s5W0r6'})
        self.assertRedirects(response, '/accounts/profile/')

    def test_login_view_next_reset(self):
        response = self.client.post('/accounts/login/?next=/accounts/password_reset/done/',
            {'username':'existing', 'password':'P4s5W0r6'})
        self.assertRedirects(response, '/accounts/profile/')

    def test_login_view_next_registration(self):
        response = self.client.post('/accounts/login/?next=/registration/',
            {'username':'existing', 'password':'P4s5W0r6'})
        self.assertRedirects(response, '/accounts/profile/')

    def test_change_profile_view_status_code(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        usr = User.objects.get(username='existing')
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': usr.id}), {'bio': 'Foo Bar'})
        self.assertEqual(response.status_code, 200)

    def test_change_profile_view_denied(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        usr = User.objects.get(username='existing')
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': 74}))
        self.assertEqual(response.status_code, 404)

    def test_delete_profile_view_status_code(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        usr = User.objects.get(username='existing')
        response = self.client.get(reverse('profile_delete',
            kwargs={'pk': usr.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_profile_view_denied(self):
        self.client.post('/accounts/login/', {'username':'existing',
            'password':'P4s5W0r6'})
        usr = User.objects.get(username='existing')
        response = self.client.get(reverse('profile_delete',
            kwargs={'pk': 74}))
        self.assertEqual(response.status_code, 404)
