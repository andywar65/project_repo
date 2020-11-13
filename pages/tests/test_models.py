from django.test import TestCase
from django.urls import reverse

from pages.models import TreePage

class TreePageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        TreePage.objects.create(title='Page 1', path = '0001', depth = 1,
            numchild = 2,
            body = 'Bar',
            )
        TreePage.objects.create(title='Child Page', path = '00010001',
            depth = 2,
            numchild = 0,
            slug = 'Child-Page',
            body = 'Foo Bar',
            )
        TreePage.objects.create(title='Second Child Page', path = '00010002',
            depth = 2,
            numchild = 0,
            body = 'Foo Bar Bar',
            )
        TreePage.objects.create(title='Lonely Page', path = '0002',
            depth = 1,
            numchild = 0,
            body = 'Foo Foo Bar',
            )

    def test_tree_page_str_method(self):
        page = TreePage.objects.get(slug = 'page-1')
        self.assertEquals(page.__str__(), 'Page 1')

    def test_tree_page_get_path(self):
        page = TreePage.objects.get(slug = 'page-1')
        #this test also generate unique slug
        self.assertEquals(page.get_path(), reverse('docs:page_list')+'page-1/')

    def test_child_tree_page_get_path(self):
        page = TreePage.objects.get(slug = 'child-page')
        #this test also generate unique slug
        self.assertEquals(page.get_path(), reverse('docs:page_list')+'page-1/child-page/')

    def test_tree_page_get_adjacent_pages(self):
        page = TreePage.objects.get(slug = 'page-1')
        child = TreePage.objects.get(slug = 'child-page')
        self.assertEquals(page.get_adjacent_pages(), (None, child))

    def test_tree_page_get_no_adjacent_pages(self):
        page = TreePage.objects.get(slug = 'lonely-page')
        self.assertEquals(page.get_adjacent_pages(), (None, None))

    def test_child_tree_page_get_adjacent_pages(self):
        parent = TreePage.objects.get(slug = 'page-1')
        child = TreePage.objects.get(slug = 'child-page')
        sibling = TreePage.objects.get(slug = 'second-child-page')
        self.assertEquals(child.get_adjacent_pages(), (parent, sibling))

    def test_tree_page_get_paragraphs(self):
        page = TreePage.objects.get(slug = 'page-1')
        self.assertEquals(page.get_paragraphs(), 'Bar')
