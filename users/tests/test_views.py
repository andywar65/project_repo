from django.test import TestCase
from django.urls import reverse

from users.models import User

class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='existing', password='P4s5W0r6',)

    def test_registration_view_status_code(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

    def test_registration_view_template(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_view_registration(self):
        with self.settings(RECAPTCHA_TEST_MODE = True):
            response = self.client.post('/registration/', {'username':'new_guy',
                'email':'new@guy.com', 'privacy': True, })
            self.assertRedirects(response, '/registration?submitted=True')
