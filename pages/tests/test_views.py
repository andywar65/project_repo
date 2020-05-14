from django.test import TestCase

from streamblocks.models import HomeButton
from blog.models import Article
from pages.models import TreePage, HomePage

class TreePageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        HomeButton.objects.create( id=51 )
        HomePage.objects.create(
            action = '[{"unique_id":"4h5dps","model_name":"HomeButton","id":[51],"options":{}}]',
            )
        TreePage.objects.create(title='Page 1', path = '0001', depth = 1,
            numchild = 1,
            )
        TreePage.objects.create(title='Child Page', path = '00010001',
            depth = 2,
            numchild = 0,
            slug = 'Child-Page'
            )
        Article.objects.create(title='Article 5',
            date = '2020-05-13 15:58:00+02')

    def test_home_template_view_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_template_view_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_home_template_view_article_context(self):
        all_posts = Article.objects.all()
        response = self.client.get('/')
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_home_template_view_action_context(self):
        actions = HomeButton.objects.all()
        response = self.client.get('/')
        self.assertQuerysetEqual(response.context['actions'], actions,
            transform=lambda x: x)
