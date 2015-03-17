from time import time

from _commons.helpers.types import TypesHelper
from _index.models import Ids as _IndexIds

from _index.helpers import ContentHelper as _IndexContentHelper
from relevance.helpers import RelevanceHelper

from .models import *


class PoolHelper(object):
    """
    An helper on pool operations
    """

    @staticmethod
    def move(request, user, comment_pool):
        """
        Move a comment from pool to active
        """
        # Prevents circular imports
        from notification.factories import PushCommentNotificationFactory
        
        comment_next_id, comment_next_url = None, None

        for comment_id, comment_url in comment_pool.items():
            try:
                db_pool = Pool.objects.get(id=comment_id)

                # Move comment
                comment = Active(
                    author=user,
                    item=db_pool.item,
                    body=db_pool.body,
                    in_reply_to=db_pool.in_reply_to,
                )
                comment.save()
                db_pool.delete()

                _IndexIds.objects.get_or_create(
                    item_type=TypesHelper.encode('comment'),
                    item_id=comment.id,
                )

                target_user = None
                if db_pool.in_reply_to:
                    try:
                        target_user = AuthUser.objects.get(id=db_pool.in_reply_to.author_id)
                    except AuthUser.DoesNotExist:
                        pass

                PushCommentNotificationFactory(
                    request=request,
                    user=user,
                    target_user=target_user,
                    item_type=comment.item.item_type,
                    item_id=comment.item.item_id,
                ).set(comment)

                # We'll redirect to that comment later
                if not comment_next_id and not comment_next_url:
                    comment_next_id = comment.id
                    comment_next_url = comment_url
            
            except Pool.DoesNotExist:
                pass
            finally:
                if 'comment_pool' in request.session:
                    del request.session['comment_pool']

        return (comment_next_url, comment_next_id)


class ProcessHelper(object):
    """
    An helper on process operations
    """

    @staticmethod
    def real_relevance(count_relevant, count_irrelevant, count_flagged):
        """
        Process a comment's real relevance
        """
        f_factor = count_relevant - (count_flagged * 5 + count_irrelevant)

        if f_factor >= 0:
            return f_factor  # Relevant enough
        return -1            # To-be-trashed


    @staticmethod
    def num_replies(comment_obj, db_all):
        """
        Return the number of replies to a comment
        """
        return db_all.filter(in_reply_to=comment_obj).count()


    @staticmethod
    def body_length(comment_obj):
        """
        Return a comment's body length
        """
        return len(comment_obj.body)


    @staticmethod
    def author_rank(comment_author):
        """
        Return a comment's author rank
        """
        return comment_author.profile.rank or 0


    @classmethod
    def ordering(_class, comment_obj, db_all, comment_author, count_relevant, count_irrelevant, count_flagged):
        """
        Calculate a comment's ordering (a kind of rank)
        """
        relevance = _class.real_relevance(count_relevant, count_irrelevant, count_flagged)
        replies = _class.num_replies(comment_obj, db_all)
        length = _class.body_length(comment_obj)
        author_rank = _class.author_rank(comment_author)

        # Desc: each 'sub-rank' has a certain weight, thus determining the most important comment ordering factor

        k =  (str)((int)((\
                abs(relevance) * 0.66\
              + abs(replies) * 1\
              + abs(length) * 0.0005\
              + abs(author_rank) * 0.10\
             )))                             # Process comment relevance (unsafe)
        k += (str)((int)(time()))            # Add timestamp decimals (most recent comments w/ same relevance first) (safe)
        k = int(k)                           # Finally, reprocess an usable integer value

        if relevance == -1:
            k = -1 * (1/float(k))
        return k


class ReadHelper(object):
    """
    An helper on read operations
    """

    @staticmethod
    def order(comment_list):
        """
        Order a list of comments
        """
        return sorted(comment_list, key=lambda k: k['ordering'], reverse=True)


    @staticmethod
    def generate(user, local_cache, item_author_id, db_obj, db_all, level=1):
        """
        Generate the usable comment object
        """
        # Read comment data
        author_id = db_obj.author_id

        # Read associated data
        local_cache['count']['items'] += 1

        if not author_id in local_cache['author']:
            local_cache['count']['users'] += 1
            local_cache['author'][author_id] = db_obj.author

        # Count data
        count_flagged = db_obj.flag_set.count()
        relevance = RelevanceHelper.get('comment', db_obj.id, user)

        comment_obj = {
            'author': {
                'user': local_cache['author'][author_id],
                'is_master': db_obj.author_id == item_author_id,
                'is_myself': user and db_obj.author_id == user.id,
            },

            'meta': {
                'date': db_obj.date,
                'edit_date': db_obj.edit_date,
                'relevance': relevance,
                'is_flagged': db_obj.flag_set.filter(author_id=user.id).exists(),
            },

            'body': db_obj.body,
            'ordering': ProcessHelper.ordering(
                comment_obj=db_obj,
                db_all=db_all,
                comment_author=local_cache['author'][author_id],
                count_relevant=relevance.get('count_relevant', 0),
                count_irrelevant=relevance.get('count_irrelevant', 0),
                count_flagged=count_flagged,
            ),

            'id': db_obj.id,
            'in_reply_to': None,
        }

        # Reply data?
        if level > 2 and db_obj.in_reply_to:
            if not db_obj.in_reply_to.author_id in local_cache['author']:
                local_cache['author'][db_obj.in_reply_to.author_id] = db_obj.in_reply_to.author

            in_reply_to_user = local_cache['author'][db_obj.in_reply_to.author_id]

            comment_obj['in_reply_to'] = {
                'full_name': '%s %s' % (in_reply_to_user.first_name, in_reply_to_user.last_name,),
                'id': db_obj.in_reply_to.id
            }

        return comment_obj


    @classmethod
    def deepen_level(_class, local_cache, mains, user, item_author_id, comments, level=1):
        """
        Fetch a deeper commenting level
        """
        for comment in comments.filter(is_hidden=False):
            generated = _class.generate(user, local_cache, item_author_id, comment, comments, level)

            if level is 1:
                sub_mains = generated
                sub_mains['replies'] = []
            else:
                sub_mains = mains
                sub_mains['replies'].append(generated)
            
            # Any related comment?
            if comment.comment_active_reply:
                _class.deepen_level(
                    local_cache=local_cache,
                    mains=sub_mains,
                    user=user,
                    item_author_id=item_author_id,
                    comments=comment.comment_active_reply.all(),
                    level=(level + 1),
                )

            if level is 1:
                mains.append(sub_mains)


    @classmethod
    def read(_class, user, item, item_author_id):
        """
        Read comment values from database
        """
        local_cache = {
            'author': {},
            'count': {
                'items': 0,
                'users': 0
            }
        }
        comment_data = {
            'mains': [],
            'total_items': 0,
            'total_users': 0,
            'page_next': -1
        }

        if item:
            _class.deepen_level(
                local_cache=local_cache,
                mains=comment_data['mains'],
                user=user,
                item_author_id=item_author_id,
                comments=Active.objects.filter(item=item, in_reply_to=None),
            )

            comment_data['mains'] = _class.order(comment_data['mains'])

            # Quick counters
            comment_data['total_items'] = local_cache['count']['items']
            comment_data['total_users'] = local_cache['count']['users']

        return comment_data


class MetaHelper(object):
    """
    An helper on meta operations
    """

    @staticmethod
    def count(item_type, item_id):
        """
        Count the number of comments for this item
        """
        item = _IndexContentHelper.get(
            item_id=item_id,
            item_type=item_type,
        )

        return Active.objects.filter(item=item).count() if item else 0
