import json

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404

from _commons.helpers.cache import CacheHelper
from _commons.helpers.redirects import login_required_url, register_required_url
from _commons.helpers import durations
from _commons.helpers.levels import LevelsHelper
from _commons.helpers.rank import RankHelper
from _commons.helpers.types import TypesHelper
from dashboard.forms import TutorialNewForm
from rank.helpers import RankProcessHelper
from relevance.helpers import RelevanceHelper

from _index.models import Ids as _IndexIds

from .helpers.related import RelatedHelper
from .helpers.process import ProcessHelper
from .helpers.tag import TagHelper as TutorialTagHelper
from .saver import *


def root(request):
    """
    Tutorial > Root
    """
    return HttpResponsePermanentRedirect(reverse('explore.views.tutorials'))


def view(request, tag, slug):
    """
    Tutorial > View
    """
    namespace = CacheHelper.ns('tutorial:views:view', tag=tag, slug=slug)

    tutorial_id, tut_status, tut_path = ProcessHelper.check('view', tag, slug)

    # This is a 404, man!
    if tut_status == 'not_found':
        raise Http404

    # Handle tutorial save POST before display? (used for edit preview)
    is_preview = False

    if request.method == 'POST' and request.POST.get('edit_preview', '0') == '1':
        save_form = TutorialNewForm(request.POST)

        if save_form.is_valid():
            is_preview = True
            TutorialSaver(
                request=request,
                tutorial_id=tutorial_id,
            ).save(save_form)

    # Redirect after tutorial is saved, just in case URL is changed...
    if tut_status == 'redirect':
        return HttpResponsePermanentRedirect(tut_path)
    if tut_status == 'unpublished' and not is_preview:
        raise Http404

    tutorial_args = CacheHelper.io.get(namespace) if not is_preview else None

    if tutorial_args is None:
        # Read tutorial data
        try:
            tutorial = Meta.objects.get(id=tutorial_id)
            index = _IndexIds.objects.get(item_type=TypesHelper.encode('tutorial'), item_id=tutorial_id)

            tut_author = tutorial.author_set.filter(is_master=True).first()
            aut_user = tut_author.user
        except (Meta.DoesNotExist, _IndexIds.DoesNotExist):
            raise Http404

        tutorial_duration = ProcessHelper.duration(tutorial.content.body, tutorial.level)

        # Pass data to template
        tutorial_args = {
            # Commons
            'item_id': index.item_id,
            'item_type': 'tutorial',

            # Models
            'aut_user': aut_user,
            'aut_profile': aut_user.profile,
            'tut_author': tut_author,
            'tut_content': tutorial.content,
            'tut_meta': tutorial,
            'tut_tags': TutorialTagHelper.list_instances(tutorial),

            # Context values
            'tut_tag': tag,
            'tut_slug': slug,
            'is_preview': is_preview,

            # Processed values
            'tut_meta_edit_date': tutorial.content.date,
            'tut_meta_level': LevelsHelper.reverse(tutorial.level)[1],
            'tut_meta_duration': durations.humanize(tutorial_duration),
            'tut_stats_views': ProcessHelper.views(tutorial),
        }

        if not is_preview:
            CacheHelper.io.set(namespace, tutorial_args)

    tutorial_args.update(
        RelevanceHelper.get('tutorial', tutorial_args['item_id'], request.user)
    )

    return render(request, 'tutorial/tutorial_view.jade', tutorial_args)


def view_related_tutorials(request, tag, slug):
    """
    Tutorial > View Related Tutorials
    """
    namespace = CacheHelper.ns('tutorial:views:view_related_tutorials', tag=tag, slug=slug)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, tutorial = RelatedHelper.build_response_complete(
            request=request,
            tutorial_tag=tag,
            tutorial_slug=slug,
            expects='tutorials',
        )

        if response_data['status'] == 'not_found':
            raise Http404

        CacheHelper.io.set(namespace, response_data)

    return render(request, 'tutorial/tutorial_view_related_tutorials.jade', response_data)


def view_related_tutorials_fetch(request, tag, slug, page=1):
    """
    Tutorial > View Related Tutorials
    """
    response_data, _ = RelatedHelper.build_response(
        request=request,
        tutorial_tag=tag,
        tutorial_slug=slug,
        expects='tutorials',
        page=int(page),
    )

    if len(response_data['related_tutorials']):
        return render(request, 'tutorial/tutorial_view_related_tutorials_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


def view_related_developers(request, tag, slug):
    """
    Tutorial > View Related Developers
    """
    namespace = CacheHelper.ns('tutorial:views:view_related_developers', tag=tag, slug=slug)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, tutorial = RelatedHelper.build_response_complete(
            request=request,
            tutorial_tag=tag,
            tutorial_slug=slug,
            expects='developers',
        )

        if response_data['status'] == 'not_found':
            raise Http404

        CacheHelper.io.set(namespace, response_data)

    return render(request, 'tutorial/tutorial_view_related_developers.jade', response_data)


def view_related_developers_fetch(request, tag, slug, page=1):
    """
    Tutorial > View Related Developers
    """
    response_data, _ = RelatedHelper.build_response(
        request=request,
        tutorial_tag=tag,
        tutorial_slug=slug,
        expects='developers',
        page=int(page),
    )

    if len(response_data['related_developers']):
        return render(request, 'tutorial/tutorial_view_related_developers_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )
