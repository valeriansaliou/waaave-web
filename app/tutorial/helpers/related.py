from _commons.helpers.types import TypesHelper

from _index.models import Ids as _IndexIds

from tutorial.models import *
from tutorial.factories import *
from user.helpers import AdvancedStatsUserHelper




class RelatedHelper(object):
    """
    An helper on tutorial related operations
    """

    @classmethod
    def build_response(_class, request, tutorial_tag, tutorial_slug, expects='tutorials', page=1):
        """
        Builds the tutorial related response
        """
        # Response data object
        response_data = {
            'status': 'none',
        }

        # Validate tutorial availability
        tutorial_id, _, _ = ProcessHelper.check('view', tutorial_tag, tutorial_slug)

        try:
            tutorial = Meta.objects.get(id=tutorial_id)
        except Meta.DoesNotExist:
            response_data['status'] = 'not_found'
            return response_data, None

        # Generate the results themselves
        items_per_page = 12

        related_feed, has_show_more = RelatedFactory(tutorial, fetch_type=expects).get(
            page=page,
            items_per_page=items_per_page,
        )

        response_data.update({
            'status': 'success',
            ('related_%s' % expects): related_feed,
            'has_show_more': has_show_more,
            'next_page': page + 1,

            'tut_tag': tutorial_tag,
            'tut_slug': tutorial_slug,
        })

        return response_data, tutorial


    @classmethod
    def build_response_complete(_class, request, tutorial_tag, tutorial_slug, expects='tutorials'):
        response_data, tutorial = _class.build_response(
            request=request,
            tutorial_tag=tutorial_tag,
            tutorial_slug=tutorial_slug,
            expects=expects,
        )

        if response_data['status'] != 'not_found':
            try:
                index = _IndexIds.objects.get(item_type=TypesHelper.encode('tutorial'), item_id=tutorial.id)
                author = tutorial.author_set.filter(is_master=True).first()

                response_data.update({
                    # Commons
                    'item_id': index.item_id,
                    'item_type': 'tutorial',

                    # Models
                    'aut_user': author.user,
                    'aut_profile': author.user.profile,
                    'aut_stats': AdvancedStatsUserHelper(author.user).get(),
                    'tut_content': tutorial.content,
                    'tut_meta': tutorial,
                })
            except _IndexIds.DoesNotExist:
                response_data['status'] = 'not_found'

        return response_data, tutorial
