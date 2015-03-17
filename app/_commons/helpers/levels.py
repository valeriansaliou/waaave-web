class LevelsHelper(object):
    """
    An helper on levels operations
    """

    values = [
        ('dummy','Dummy',),                 # 0
        ('novice','Novice',),               # 1
        ('intermediate','Intermediate',),   # 2
        ('advanced','Advanced',),           # 3
    ]


    @classmethod
    def encode(_class, content_name):
        """
        Encode a level string to integer
        """
        counter = 0
        for cont_value in _class.values:
            if content_name == cont_value[0]: return counter
            counter += 1
        return 0


    @classmethod
    def reverse(_class, content_level):
        """
        Reverse level string to integer
        """
        assert type(content_level) is int
        try:
            return _class.values[content_level]
        except IndexError:
            return None


    @classmethod
    def as_tuples(_class):
        """
        Return the list of levels in tuples
        """
        return _class.values
