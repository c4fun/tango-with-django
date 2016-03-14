from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        """
        category.view number is zero or positive, it shall never be negative
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        When adding a category, a proper slug line is created.
        i.e. "Random Category String" -> "random-cateogry-string"
        :return:
        """

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

    def test_index_view_with_no_categories(self):
        """
        If no categories exist, an appropriate message should be present
        :return:
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories to present.")
        self.assertQuerysetEqual(response.context['categories'], [])