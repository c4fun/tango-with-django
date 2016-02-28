from django.conf.urls import url, include
from rango import views

urlpatterns = [
    # name is optional--to allow you to distinguish one mapping from another
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
]