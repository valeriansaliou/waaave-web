import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from _commons.decorators.security import auth_required
from _commons.helpers.levels import LevelsHelper
from _index.helpers import ContentHelper

from tutorial.models import Meta as TutorialMeta

from tutorial.helpers.process import ProcessHelper
from tutorial.helpers.read import ReadHelper
from tutorial.helpers.tag import TagHelper
from tutorial.saver import TutorialSaver
from tutorial.moderator import TutorialModerator

from .forms import *


@auth_required
def root(request):
    """
    Dashboard > Root
    """
    return HttpResponseRedirect(reverse('dashboard.views.tutorial_root'))


@auth_required
def shot_root(request):
    """
    Dashboard > Shot Root
    """
    return render(request, 'dashboard/dashboard_shot_root.jade')


@auth_required
def shot_new(request):
    """
    Dashboard > Shot New
    """
    return render(request, 'dashboard/dashboard_shot_new.jade')


@auth_required
def shot_edit(request, shot_id):
    """
    Dashboard > Shot Edit
    """
    return render(request, 'dashboard/dashboard_shot_edit.jade')


@auth_required
def tutorial_root(request):
    """
    Dashboard > Tutorial Root
    """
    list_tutorials_obj = ReadHelper.list(request, 'author')

    return render(request, 'dashboard/dashboard_tutorial_root.jade', {
        'tutorial_list': list_tutorials_obj[0],
        'tutorial_statuses': list_tutorials_obj[1],
    })


@auth_required
def tutorial_new(request):
    """
    Dashboard > Tutorial New
    """
    return tutorial_edit(request)


@auth_required
def tutorial_edit(request, tutorial_id=None):
    """
    Dashboard > Tutorial Edit
    """
    edit_status, moderation_status = 'none', 'none'

    if tutorial_id:
        if not tutorial_id.isdigit(): raise Http404
        tutorial_id = int(tutorial_id)

    try:
        tutorial = TutorialMeta.objects.get(id=tutorial_id)
    except (TutorialMeta.DoesNotExist):
        tutorial = None

    # Form actions
    if tutorial:
        form_save_action = reverse('dashboard.views.tutorial_edit', kwargs={'tutorial_id': tutorial_id})
        tutorial_url = tutorial.url_set.filter(is_alias=False).first()
        form_preview_action = reverse('tutorial.views.view', kwargs={
            'tag': tutorial_url.tag,
            'slug': tutorial_url.slug,
        })
    else:
        form_save_action = reverse('dashboard.views.tutorial_new')
        form_preview_action = None

    # Save data?
    if request.method == 'POST':
        form = TutorialNewForm(request.POST)

        if form.is_valid():
            # Save tutorial
            tutorial_saver = TutorialSaver(
                request=request,
                tutorial=tutorial,
            )
            edit_status, edit_redirect = tutorial_saver.save(form)

            # Moderate tutorial
            moderation_message = form.cleaned_data['moderation_message']

            if request.POST.get('moderation_refuse', '0') == '1':
                moderation_status = 'refused' if TutorialModerator(request, tutorial).refuse(moderation_message) else 'none'
            elif request.POST.get('moderation_validate', '0') == '1':
                moderation_status = 'accepted' if TutorialModerator(request, tutorial).accept(moderation_message) else 'none'

            # Redirect to updated URL?
            if edit_redirect is not None:
                return HttpResponseRedirect(edit_redirect)

    elif tutorial_id is not None:
        if request.user.is_staff or request.user.is_superuser:
            TutorialModerator(request, tutorial).pending()

        form = TutorialNewForm(initial={
            'title': tutorial.title,
            'tags': ', '.join([t['name'] for t in TagHelper.list(tutorial, priority=True)]),
            'online': tutorial.is_online,
            'level': LevelsHelper.reverse(tutorial.level)[0],
            'content': tutorial.content.body,
        })

        if request.GET.get('saved', None) is not None:
            edit_status = 'save_done'

    else:
        form = TutorialNewForm()

    return render(request, 'dashboard/dashboard_tutorial_edit.jade', {
        'form': form,
        'form_save_action': form_save_action,
        'form_preview_action': form_preview_action,
        'edit_status': edit_status,
        'moderation_status': moderation_status,
        'tutorial_status': ReadHelper.status(tutorial_id) if tutorial_id else 'new',
        'tutorial_url': ProcessHelper.url(tutorial_id),
    })


@auth_required
def tutorial_trash(request):
    """
    Dashboard > Tutorial Trash
    """
    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if request.method == 'POST':
        if request.user.is_authenticated():
            tutorial_ids = request.POST.getlist('tutorial_id', [])

            if len(tutorial_ids):
                for cur_tutorial_id in tutorial_ids:
                    if not cur_tutorial_id.isdigit(): continue
                    cur_tutorial_id = int(cur_tutorial_id)

                    # Validate item data
                    item_exists, item_author_id = ContentHelper.validate(cur_tutorial_id, 'tutorial')

                    result['contents'][cur_tutorial_id] = {}

                    if item_exists is True:
                        uid = request.user.id
                        
                        if uid == item_author_id\
                           or request.user.is_staff\
                           or request.user.is_superuser:
                            TutorialSaver(
                                request=request,
                                tutorial_id=cur_tutorial_id,
                            ).remove()
                            result['contents'][cur_tutorial_id] = 'Removed'
                        else:
                            result['contents'][cur_tutorial_id] = 'Not allowed'
                    else:
                        result['contents'][cur_tutorial_id] = 'Not found'

                    result['status'] = 'success'
            else:
                result['message'] = 'Data missing'
        else:
            result['message'] = 'Not authenticated'
    else:
        result['message'] = 'Bad request'

    return HttpResponse(json.dumps(result), content_type='application/json')


@auth_required
def followings(request):
    """
    Dashboard > Followings
    """
    return render(request, 'dashboard/dashboard_followings.jade')


@auth_required
def profile_settings(request):
    """
    Dashboard > Profile Settings
    """
    return render(request, 'dashboard/dashboard_profile_settings.jade')