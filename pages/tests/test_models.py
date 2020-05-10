from django.test import TestCase

from pages.models import TreePage

class TreePageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        TreePage.objects.create(title='Page 1', path = '0001', depth = 1,
            numchild = 0,
            )

    def test_tree_page_str_method(self):
        page = TreePage.objects.get(id = 1)
        self.assertEquals(page.__str__(), 'Page 1')
