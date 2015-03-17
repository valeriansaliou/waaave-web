from tutorial.helpers.read import ReadHelper as TutorialReadHelper



class ModerationHelper(object):
    """
    An helper on moderation operations
    """

    @staticmethod
    def count_unmoderated(user):
        """
        Returns the number of unmoderated items
        """
        count = 0

        count += TutorialReadHelper.count_unmoderated(user)
        # count += ShotReadHelper.count_unmoderated(user)

        return count