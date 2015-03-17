from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from _commons.decorators.security import auth_required
from _commons.decorators.permissions import user_staff_required
from _commons.helpers.types import TypesHelper
from _index.helpers import ContentHelper

from relevance.helpers import RelevanceHelper
from dashboard.views import tutorial_trash as dashboard_tutorial_trash
from tutorial.helpers.read import ReadHelper

from comment.models import Active as CommentActive
from comment.models import Flag as CommentFlag


@auth_required
@user_staff_required
def root(request):
    """
    Moderation > Root
    """
    return HttpResponseRedirect(reverse('moderation.views.tutorials'))


@auth_required
@user_staff_required
def tutorials(request):
    """
    Moderation > Tutorials
    """
    return render(request, 'moderation/moderation_tutorials.jade', {
        'tutorial_list': ReadHelper.list(request, 'unmoderated')[0],
    })


@auth_required
@user_staff_required
def tutorial_trash(request):
    """
    Moderation > Tutorial Trash
    """
    return dashboard_tutorial_trash(request)


@auth_required
@user_staff_required
def shots(request):
    """
    Moderation > Shots
    """
    return render(request, 'moderation/moderation_shots.jade')


@auth_required
@user_staff_required
def comments(request, page=1):
    """
    Moderation > Comments
    """
    flagged_threshold = 2

    # Process paging
    page = int(page)
    comments = []

    comments_per_page = 10
    comments_start = (page - 1) * comments_per_page
    comments_end = comments_start + comments_per_page

    comment_all_db = CommentActive.objects.order_by('-date')
    comment_db = comment_all_db[comments_start:comments_end]

    if page > 1 and not len(comment_db):
        raise Http404

    comment_all_count = comment_all_db.count() if comment_all_db else 0
    page_total = comment_all_count // comments_per_page\
                  + (1 if comment_all_count % comments_per_page else 0)

    # Generate comment data
    for cur_comment_db in comment_db:
        cur_comment_relevance = RelevanceHelper.get('comment', cur_comment_db.id)
        cur_relevant_is_count = cur_comment_relevance.get('count_relevant', 0)
        cur_relevant_is_not_count = cur_comment_relevance.get('count_irrelevant', 0) or 1

        cur_comment_status = 'none'

        if cur_comment_db.flag_set.count() >= flagged_threshold:
            cur_comment_status = 'flagged'
        elif cur_relevant_is_count and cur_relevant_is_count // cur_relevant_is_not_count > 1:
            cur_comment_status = 'liked'
        elif cur_relevant_is_not_count > 1:
            cur_comment_status = 'disliked'

        comments.append({
            'comment': cur_comment_db,
            'status': cur_comment_status,
            'from': ContentHelper.read(cur_comment_db.item),
            'author': cur_comment_db.author,
        })

    return render(request, 'moderation/moderation_comments.jade', {
        'comments': comments,
        'page_current': page,
        'page_total': page_total,
    })


@auth_required
@user_staff_required
def users(request):
    """
    Moderation > Users
    """
    return render(request, 'moderation/moderation_users.jade')


@auth_required
@user_staff_required
def advertising(request):
    """
    Moderation > Advertising
    """
    return render(request, 'moderation/moderation_advertising.jade')