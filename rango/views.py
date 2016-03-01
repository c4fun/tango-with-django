from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page
from .forms import CategoryForm, PageForm
from .forms import UserForm, UserProfileForm

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Add the Top 5 most viewed pages
    pages = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = pages

    # Render the response and send it back
    return render(request, 'rango/index.html', context_dict)


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering machine.
    context_dict = {}

    # Can we find a category name slug with the given category_name_slug?
    # If YES, the .get() method will return a model instance
    # If NOT, the .get() method will return a DoesNotExist exception
    # Already change the try except logic using get_object_or_404 shortcut
    category = get_object_or_404(Category, slug=category_name_slug)
    context_dict['category_name'] = category.name

    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
    pages = Page.objects.filter(category=category)

    # Adds our results list to the template context under name pages.
    context_dict['pages'] = pages
    # Add the category object from the DB to the context dictionary.
    # We'll use this in the template to verify that the category exists.
    context_dict['category'] = category

    # Insert the category_name_slug into the dictionary so that it can be used
    # in the add_page
    # 这里必须是category_name_slug的方式，而不是category_name。因为slug还需要传给add_page.html继续使用，
    # 如果用category_name, 传入的category_name可能产生另外的slug
    context_dict['category_name_slug'] = category_name_slug

    return render(request, 'rango/category.html', context_dict)


def about(request):
    return HttpResponse('Rango says here is the about page. Duh!<br/> <a href="/rango/index">Index</a>')


def add_category(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # TODO redirect to the success URL. Rather than the /index
            return index(request)

        else:
            print(form.errors)

    else:
        # If the request was not a POST, we'll present a blank form
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # DONE BUG: 这里必须redirect，否则再次创建有问题
                return redirect('rango.views.index')
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    # Not a HTTP POST request, we render the form using two models. These forms will be blank & wait for input
    if request.method != 'POST':
        user_form = UserForm()
        profile_form = UserProfileForm()
    else:
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to DB
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Save the user profile form data to DB
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered':registered})

