__author__ = 'laurichard'
from django import forms
from .models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Plase input the category name...")
    # The model already has a default value, so the HiddenInput is unnecessary
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # Todo What is the required=False doing here?
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form
    class Meta:
        model = Category
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of this page...")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of this page...")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        exclude = ('category',)