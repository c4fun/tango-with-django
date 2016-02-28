__author__ = 'laurichard'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_category('Python', views=128, likes=64)
    add_page(category=python_cat,
             title="Official Python Tutuorial",
             url="http://docs.python.org/2/tutorial/",
             views=64)

    add_page(category=python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/",
             views=32)

    add_page(category=python_cat,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/",
             views=32)

    django_cat = add_category("Django", views=64, likes=32)

    add_page(category=django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
             views=32)

    add_page(category=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/",
             views=16)

    add_page(category=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/",
             views=16)

    frame_cat = add_category("Other Frameworks", views=32, likes=16)

    add_page(category=frame_cat,
             title="Bottle",
             url="http://bottlepy.org/docs/dev/",
             views=16)

    add_page(category=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org",
             views=16)

    # Print out what we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(c, p))

def add_category(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    return c

def add_page(category, title, url, views=0):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

if __name__ == '__main__':
    print("Starting Rango Population script...")
    populate()