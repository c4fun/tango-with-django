from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta

from rango.models import Category, Page

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
        """

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

    def test_index_view_with_no_categories(self):
        """
        If no categories exist, an appropriate message should be present
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories to present.")
        self.assertQuerysetEqual(response.context['categories'], [])


class IndexViewTests(TestCase):

    def test_index_view_with_categories(self):
        """
        If no question exist, an appropriate message will be displayed.
        If yes, then display the categories.
        """
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)


class PageMethodTests(TestCase):

    def test_visit_not_in_the_future(self):
        """
        visit_not_in_the_future should return False if last_visit or first_visit of Page is in future.
        """
        cat = add_cat('test_cat', 1, 1)
        page = add_page(cat, "test_page", "http://example.com", 0)
        self.assertEqual(page.first_visit < timezone.now(), True)
        self.assertEqual(page.last_visit < timezone.now(), True)



def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(cat, title, url, views):
    page = Page.objects.create(title=title,
                               category=cat,
                               url=url,
                               views=views,
                               first_visit=timezone.now()+timedelta(days=30),
                               last_visit=timezone.now()+timedelta(days=30))
    return page