import json

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from _commons.helpers.cache import CacheHelper

from .helpers import *
from .forms import *


def root(request):
    """
    Search > Root
    """
    search_type = request.GET.get('t', 'all')
    search_query = request.GET.get('q', '')

    if search_type and search_query:
        # Initialize data
        search_page = str(request.GET.get('p', 1))
        search_page = int(search_page) if search_page.isdigit() else 1

        if search_page is 0:
            raise Http404

        results_per_page = 20
        start = (search_page - 1) * results_per_page
        end = start + results_per_page

        # Read search results from cache
        namespace = CacheHelper.ns('search:views:root', search_type=search_type, search_query=search_query, search_page=search_page)
        results = CacheHelper.io.get(namespace)

        if results is None:
            results = {
                'tutorials_all': None,
                'tutorials': None,

                'books_all': None,
                'books': None,

                'spots_all': None,
                'spots': None,

                'users_all': None,
                'users': None,
            }

            form = TyphoonSearchForm({
                't': search_type,
                'q': search_query,
            })

            # Search for tutorials
            if search_type in ('all', 'tutorials'):
                results['tutorials_all'] = form.search_tutorials()
                results['tutorials'] = TutorialsListHelper.adapt(results['tutorials_all'], start, end)

            # Search for books
            if search_type in ('all', 'books'):
                results['books_all'] = form.search_books()
                results['books'] = BooksListHelper.adapt(results['books_all'], start, end)

            # Search for spots
            if search_type in ('all', 'spots'):
                results['spots_all'] = form.search_spots()
                results['spots'] = SpotsListHelper.adapt(results['spots_all'], start, end)

            # Search for users
            if search_type in ('all', 'users'):
                results['users_all'] = form.search_users()
                results['users'] = UsersListHelper.adapt(results['users_all'], start, end)

            CacheHelper.io.set(namespace, results, 300)

        # Process the total number of pages (for paging)
        search_page_total = max(
            CommonListHelper.paging(
                results['tutorials_all'],
                results_per_page,
            )[1],

            CommonListHelper.paging(
                results['books_all'],
                results_per_page,
            )[1],

            CommonListHelper.paging(
                results['spots_all'],
                results_per_page,
            )[1],

            CommonListHelper.paging(
                results['users_all'],
                results_per_page,
            )[1],
        ) or 1

        # Page overflow?
        if search_page > search_page_total:
            raise Http404

        results.update({
            'search_page': search_page,
            'search_page_total': search_page_total,

            'search_url_params': {
                't': search_type,
                'q': search_query,
            },
        })
    else:
        return HttpResponsePermanentRedirect(reverse('explore.views.tutorials'))

    return render(request, 'search/search_root.jade', results)


def root_page(request, page):
    """
    Search > Root Page
    """
    return root(request)


def suggest(request):
    """
    Search > Suggest (Autocomplete)
    """
    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    # Initialize data
    search_type = request.GET.get('t', 'all')
    search_query = request.GET.get('q', None)

    if search_type and search_query:
        if search_type in ('all', 'tutorials', 'books', 'spots', 'users'):
            # Read search results from cache
            namespace = CacheHelper.ns('search:views:suggest', search_type=search_type, search_query=search_query)
            search_args = CacheHelper.io.get(namespace)

            if search_args is None:
                # Adapt search form
                form = TyphoonSearchForm({
                    't': search_type,
                    'q': search_query,
                })

                search_args = {
                    'search_url_params': {
                        't': search_type,
                        'q': search_query,
                    },

                    'tutorials': [],
                    'books': [],
                    'spots': [],
                    'users': [],

                    'total': 0,
                    'matches': 0,
                }

                # Search for tutorials
                if search_type in ('all', 'tutorials'):
                    tutorials_max = 3
                    tutorials_all = form.search_tutorials()

                    search_args['tutorials'] = TutorialsListHelper.adapt(tutorials_all, 0, tutorials_max)
                    search_args['matches'] += len(tutorials_all)
                    search_args['total'] += len(search_args['tutorials'])

                # Search for books
                if search_type in ('all', 'books'):
                    books_max = 3
                    books_all = form.search_books()

                    search_args['books'] = BooksListHelper.adapt(books_all, 0, books_max)
                    search_args['matches'] += len(books_all)
                    search_args['total'] += len(search_args['books'])

                # Search for spots
                if search_type in ('all', 'spots'):
                    spots_max = 3
                    spots_all = form.search_spots()

                    search_args['spots'] = SpotsListHelper.adapt(spots_all, 0, spots_max)
                    search_args['matches'] += len(spots_all)
                    search_args['total'] += len(search_args['spots'])

                # Search for users
                if search_type in ('all', 'users'):
                    users_max = 3
                    users_all = form.search_users()

                    search_args['users'] = UsersListHelper.adapt(users_all, 0, users_max)
                    search_args['matches'] += len(users_all)
                    search_args['total'] += len(search_args['users'])

                CacheHelper.io.set(namespace, search_args, 300)

            return render(request, 'search/search_suggest.jade', search_args)
    
        result['message'] = 'Invalid Type'
    else:
        result['message'] = 'Bad Request'

    return HttpResponse(json.dumps(result), content_type='application/json')
