from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Render the response and send it back
    return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering machine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given category_name_slug?
        # If YES, the .get() method will return a model instance
        # If NOT, the .get() method will return a DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # Add the category object from the DB to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)



def about(request):
    return HttpResponse('Rango says here is the about page. Duh!<br/> <a href="/rango/index">Index</a>')