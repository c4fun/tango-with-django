from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Category, Page
from .forms import CategoryForm, PageForm
from .forms import UserForm, UserProfileForm
from datetime import datetime
from django.utils import timezone
from .bing_search import run_query
from .helper import get_category_list

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

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() -last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True

    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    # Render the response and send it back
    response = render(request, 'rango/index.html', context_dict)
    return response


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering machine.
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query
    # Can we find a category name slug with the given category_name_slug?
    # If YES, the .get() method will return a model instance
    # If NOT, the .get() method will return a DoesNotExist exception
    # Already change the try except logic using get_object_or_404 shortcut
    category = get_object_or_404(Category, slug=category_name_slug)
    context_dict['category_name'] = category.name

    # Increment the category's views property
    category.views += 1
    category.save()

    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
    pages = Page.objects.filter(category=category).order_by('-views')

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

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    return render(request, 'rango/about.html', {'visits': count})

@login_required
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

@login_required
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
                page.first_visit = timezone.now()
                page.last_visit = timezone.now()
                page.save()
                # DONE BUG: 这里必须redirect，否则再次创建有问题
                # return redirect('rango.views.index')
                return redirect('/rango/index/')
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

# def register(request):
#     registered = False
#
#     # Not a HTTP POST request, we render the form using two models. These forms will be blank & wait for input
#     if request.method != 'POST':
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     else:
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to DB
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             # Save the user profile form data to DB
#             # Since we need to set the user attribute ourselves, we set commit=False.
#             # This delays saving the model until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # Did the user provide a profile picture?
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#
#         else:
#             print(user_form.errors, profile_form.errors)
#
#     return render(request, 'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered':registered})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/index/')
#             else:
#                 return HttpResponse("You Rango account is disabled.")
#         else:
#             print("Invalid login details: {0}, {1}".format(username, password))
#             return HttpResponse("Not a valid username/password combination")
#     else:
#         return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# @login_required
# def user_logout(request):
#     # Since we have checked the customer has already logged in the decorator
#     logout(request)
#
#     return HttpResponseRedirect('/rango/index/')

def search(request):

    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list':result_list})


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.last_visit = timezone.now()
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)

def dislike_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes - 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)

def suggest_category(request):

    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cat_list': cat_list})
