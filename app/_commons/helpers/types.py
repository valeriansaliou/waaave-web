class TypesHelper(object):
    """
    An helper on types operations
    """

    values = {
        0: 'comment',
        1: 'tutorial',
        2: 'shot',
        3: 'user',
        4: 'book',
    }


    @classmethod
    def encode(_class, item_name):
        """
        Encode a type string to integer
        """
        for type_id, type_name in _class.values.iteritems():
            if item_name == type_name: return type_id
        return None


    @classmethod
    def reverse(_class, item_type):
        """
        Reverse a type integer to string
        """
        assert type(item_type) is int
        if item_type in _class.values:
            return _class.values[item_type]
        return None