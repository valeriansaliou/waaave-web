class StatusesHelper(object):
    """
    An helper on statuses operations
    """

    values = {
        0: ('none','Not Moderated',),
        1: ('moderated','Being Moderated',),
        2: ('accepted','Accepted',),
        3: ('refused','Refused',),
    }


    @classmethod
    def encode(_class, enc_status_name):
        """
        Encode a status string to integer
        """
        for status_id, status_data in _class.values.iteritems():
            if enc_status_name == status_data[0]: return status_id
        return 0


    @classmethod
    def reverse(_class, rev_status_id):
        """
        Reverse a status integer to string
        """
        assert type(rev_status_id) is int
        if rev_status_id in _class.values:
            return _class.values[rev_status_id]
        return None


    @classmethod
    def as_tuples(_class):
        """
        Return the list of statuses in tuples
        """
        return [(key, value.title()) for key, value in CONTENT_LEVELS.items()]