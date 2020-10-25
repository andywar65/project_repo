from django.test import TestCase
from django.urls import reverse

#from streamblocks.models import HomeButton
from blog.models import Article
from pages.models import TreePage, HomePage, HomeButton

class TreePageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        home = HomePage.objects.create(
            #action = '[{"unique_id":"4h5dps","model_name":"HomeButton","id":[51],"options":{}}]',
            )
        HomeButton.objects.create( home_id = home.uuid )
        TreePage.objects.create(title='Page 1', path = '0001', depth = 1,
            numchild = 1, body='Foo'
            )
        TreePage.objects.create(title='Child Page', path = '00010001',
            depth = 2,
            numchild = 0,
            slug = 'Child-Page', body='Bar'
            )
        Article.objects.create(title='Article 5',
            date = '2020-05-13')

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

    def test_tree_page_list_view_status_code(self):
        response = self.client.get(reverse('docs:page_list'))
        self.assertEqual(response.status_code, 200)

    def test_tree_page_list_view_template(self):
        response = self.client.get(reverse('docs:page_list'))
        self.assertTemplateUsed(response, 'pages/tree_page_list.html')

    def test_tree_page_list_view_context_object(self):
        page_1 = TreePage.objects.get(slug='page-1')
        child_page = TreePage.objects.get(slug='child-page')
        response = self.client.get(reverse('docs:page_list'))
        self.assertEqual(response.context['annotated_lists'],
            [[
                (page_1, {'open': True, 'close': [], 'level': 0}),
                (child_page, {'open': True, 'close': [0, 1], 'level': 1})
            ]])

    def test_tree_page_detail_view_status_code(self):
        response = self.client.get(reverse('docs:page_by_slug',
            kwargs={'slug': 'page-1'}))
        self.assertEqual(response.status_code, 200)

    def test_tree_page_detail_view_not_found(self):
        response = self.client.get(reverse('docs:page_by_slug',
            kwargs={'slug': 'not-found'}))
        self.assertEqual(response.status_code, 404)

    def test_tree_page_detail_view_template(self):
        response = self.client.get(reverse('docs:page_by_slug',
            kwargs={'slug': 'page-1'}))
        self.assertTemplateUsed(response, 'pages/tree_page.html')

    def test_tree_page_detail_view_context_object(self):
        page = TreePage.objects.get(slug='page-1')
        response = self.client.get(reverse('docs:page_by_slug',
            kwargs={'slug': 'page-1'}))
        self.assertEqual(response.context['page'], page )

    def test_tree_page_detail_view_context_adjacent(self):
        page = TreePage.objects.get(slug='child-page')
        response = self.client.get(reverse('docs:page_by_slug',
            kwargs={'slug': 'page-1'}))
        self.assertEqual(response.context['adjacent'], (None, page) )

    def test_tree_page_by_path_view_status_code(self):
        response = self.client.get('/docs/page-1/child-page/')
        self.assertEqual(response.status_code, 200)

    def test_tree_page_by_path_view_wrong_path(self):
        response = self.client.get('/docs/wrong-path/child-page/')
        self.assertEqual(response.status_code, 404)

    def test_tree_page_by_path_view_template(self):
        response = self.client.get('/docs/page-1/child-page/')
        self.assertTemplateUsed(response, 'pages/tree_page.html')

    def test_tree_page_by_path_view_context_object(self):
        page = TreePage.objects.get(slug='child-page')
        response = self.client.get('/docs/page-1/child-page/')
        self.assertEqual(response.context['page'], page )

    def test_tree_page_by_path_view_context_adjacent(self):
        page = TreePage.objects.get(slug='page-1')
        response = self.client.get('/docs/page-1/child-page/')
        self.assertEqual(response.context['adjacent'], (page, None) )
