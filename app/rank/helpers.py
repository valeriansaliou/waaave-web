from _commons.helpers.rank import RankHelper

from .models import Record as RankRecord


class RankProcessHelper(object):
    """
    An helper on rank process operations
    """

    @classmethod
    def create(_class, recipient, sender, entity, action):
        """
        Creates and saves the rank record
        """
        # checks if a rank record already exists for relevant clicks
        if action[0] in ('click_relevant', 'click_irrelevant'):
            rank_record = _class.check_if_exist(recipient, sender, entity, action)
        else:
            rank_record = RankRecord()

        rank_record.recipient_id = recipient.user.id
        rank_record.recipient_rank = recipient.rank

        # checks if the sender is not an anonymous user
        if sender is None:
            rank_record.sender_id = None
            rank_record.sender_rank = None
            rank_record.sender_rank_impact = None
        else:
            rank_record.sender_id = sender.user.id
            rank_record.sender_rank = sender.rank
            sender_rank_info = RankHelper.get_rank(sender.rank)
            rank_record.sender_rank_impact = sender_rank_info[2]

        rank_record.entity_id = entity[0]
        rank_record.entity_type = entity[1]
        rank_record.action_type = action[0]
        rank_record.action_exp = action[1]
        rank_record.action_exp_with_impact = action[1] if action[2] == False else action[1] * sender_rank_info[2]
        rank_record.save()

        _class.update_user_experience(recipient, rank_record.action_exp_with_impact, 'create')

        return rank_record


    @classmethod
    def cancel(_class, recipient, sender, entity, action):
        """
        Cancels and deletes the rank record
        """
        # checks if the sender is not an anonymous user
        sender_id = None if sender is None else sender.user.id

        rank_record = RankRecord.objects.filter(recipient_id=recipient.user.id, sender_id=sender_id, entity_id=entity[0], entity_type=entity[1], action_type=action[0]).first()
        
        if rank_record:
            rank_record.delete()
            _class.update_user_experience(recipient, rank_record.action_exp_with_impact, 'cancel')

        return rank_record


    @classmethod
    def check_if_exist(_class, recipient, sender, entity, action):
        """
        Checks if a rank record already exists
        """
        action_type = 'click_irrelevant' if action[0] == 'click_relevant' else 'click_relevant'
        rank_record = RankRecord.objects.filter(recipient_id=recipient.user.id, sender_id=sender.user.id, entity_id=entity[0], entity_type=entity[1], action_type=action_type)
        
        count = rank_record.count()
        rank_record = rank_record.first()

        if rank_record and count != 0:
            _class.update_user_experience(recipient, rank_record.action_exp_with_impact, 'cancel')

        return rank_record if count == 1 else RankRecord()


    @staticmethod
    def update_user_experience(user, experience, type):
        """
        Updates the user experience
        """
        user.experience = float(user.experience) + float(experience) if type == 'create' else float(user.experience) - float(experience)

        # prevents negative rank from being saved in database
        if user.experience < 0:
            user.experience = 0

        # saves the new rank if level up!
        rank = RankHelper.get_rank_from_experience(user.experience)
        if user.rank != rank:
            user.rank = rank

        user.save()

        return True
