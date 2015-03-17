from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def page(request, page_number=1):
    """
    Blog > Page
    """
    return render(request, 'blog/blog_page.jade')


def date(request, date_year, date_month, date_day):
    """
    Blog > Date
    """
    return render(request, 'blog/blog_date.jade')


def category(request, category_slug):
    """
    Blog > Category
    """
    return render(request, 'blog/blog_category.jade')


def post(request, post_year, post_slug):
    """
    Blog > Post
    """
    return render(request, 'blog/blog_post.jade')