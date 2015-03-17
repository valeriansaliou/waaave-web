from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from .helpers import *


def root(request):
    """
    Explore > Root
    """
    return HttpResponseRedirect(reverse('explore.views.tutorials'))


def tutorials(request, page=1):
    """
    Explore > Tutorials Newest
    """
    success, response_data = TutorialsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='-date',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.tutorials',
    })
    
    return render(request, 'explore/explore_tutorials.jade', response_data)


def tutorials_popular(request, page=1):
    """
    Explore > Tutorials Popular
    """
    success, response_data = TutorialsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='popular',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.tutorials_popular',
    })

    return render(request, 'explore/explore_tutorials.jade', response_data)


def tutorials_alphabetical(request, page=1):
    """
    Explore > Tutorials Alphabetical
    """
    success, response_data = TutorialsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='title',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.tutorials_alphabetical',
    })
    
    return render(request, 'explore/explore_tutorials.jade', response_data)


def tutorials_yours(request, page=1):
    """
    Explore > Tutorials Yours
    """
    success, response_data = TutorialsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='-date',
        author_id=request.user.id,
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.tutorials_yours',
    })
    
    return render(request, 'explore/explore_tutorials.jade', response_data)


def books(request, page=1):
    """
    Explore > Books
    """
    success, response_data = BooksExploreHelper.build_response(
        request=request,
        page=page,
        order_by='-date',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.books',
    })

    return render(request, 'explore/explore_books.jade', response_data)


def books_popular(request, page=1):
    """
    Explore > Books
    """
    success, response_data = BooksExploreHelper.build_response(
        request=request,
        page=page,
        order_by='popular',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.books_popular',
    })

    return render(request, 'explore/explore_books.jade', response_data)


def books_alphabetical(request, page=1):
    """
    Explore > Books
    """
    success, response_data = BooksExploreHelper.build_response(
        request=request,
        page=page,
        order_by='title',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.books_alphabetical',
    })

    return render(request, 'explore/explore_books.jade', response_data)


def spots(request, page=1):
    """
    Explore > Spots
    """
    success, response_data = SpotsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='-date',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.spots',
    })

    return render(request, 'explore/explore_spots.jade', response_data)


def spots_popular(request, page=1):
    """
    Explore > Spots
    """
    success, response_data = SpotsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='popular',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.spots_popular',
    })

    return render(request, 'explore/explore_spots.jade', response_data)


def spots_alphabetical(request, page=1):
    """
    Explore > Spots
    """
    success, response_data = SpotsExploreHelper.build_response(
        request=request,
        page=page,
        order_by='name',
    )

    if not success:
        raise Http404

    response_data.update({
        'explore_view': 'explore.views.spots_alphabetical',
    })

    return render(request, 'explore/explore_spots.jade', response_data)
