class RankHelper(object):
    """
    For more details: https://docs.google.com/document/d/1_Xb3HW9oZeymqUpCw9NnkpvilXFIBw0Hcn2Nr3x5LIs

    LEVEL EQUATIONS (OR RANK EQUATIONS)
    L < 15           e(L) = L^3 * ((((L+1)/3)+24)/50)
    15 <= L <= 36    e(L) = L^3 * ((L+14)/50)
    37 <= L <= 100   e(L) = L^3 * (((L/2)+32)/50)

    IMPACT EQUATION
    I(L) = (L/40) + 0.95
    """

    ranks = [
        # <list>[[N]<tuple>(<int>rank<int>experience,<decimal>impact,)]

        (0, 0, 0.95,),                  # 0
        (1, 0, 0.98,),                  # 1
        (2, 4, 1.00,),                  # 2
        (3, 14, 1.03,),                 # 3
        (4, 33, 1.05,),                 # 4
        (5, 65, 1.08,),                 # 5
        (6, 114, 1.10,),                # 6
        (7, 183, 1.13,),                # 7
        (8, 276, 1.15,),                # 8
        (9, 399, 1.18,),                # 9
        (10, 553, 1.20,),               # 10
        (11, 745, 1.23,),               # 11
        (12, 979, 1.25,),               # 12
        (13, 1260, 1.28,),              # 13
        (14, 1592, 1.30,),              # 14
        (15, 1958, 1.33,),              # 15
        (16, 2458, 1.35,),              # 16
        (17, 3046, 1.38,),              # 17
        (18, 3732, 1.40,),              # 18
        (19, 4527, 1.43,),              # 19
        (20, 5440, 1.45,),              # 20
        (21, 6483, 1.48,),              # 21
        (22, 7667, 1.50,),              # 22
        (23, 9004, 1.53,),              # 23
        (24, 10506, 1.55,),             # 24
        (25, 12188, 1.58,),             # 25
        (26, 14061, 1.60,),             # 26
        (27, 16140, 1.63,),             # 27
        (28, 18440, 1.65,),             # 28
        (29, 20975, 1.68,),             # 29
        (30, 23760, 1.70,),             # 30
        (31, 26812, 1.73,),             # 31
        (32, 30147, 1.75,),             # 32
        (33, 33781, 1.78,),             # 33
        (34, 37732, 1.80,),             # 34
        (35, 42018, 1.83,),             # 35
        (36, 46656, 1.85,),             # 36
        (37, 51160, 1.88,),             # 37
        (38, 55969, 1.90,),             # 38
        (39, 61099, 1.93,),             # 39
        (40, 66560, 1.95,),             # 40
        (41, 72367, 1.98,),             # 41
        (42, 78533, 2.00,),             # 42
        (43, 85072, 2.03,),             # 43
        (44, 91999, 2.05,),             # 44
        (45, 99326, 2.08,),             # 45
        (46, 107070, 2.10,),            # 46
        (47, 115244, 2.13,),            # 47
        (48, 123863, 2.15,),            # 48
        (49, 132943, 2.18,),            # 49
        (50, 142500, 2.20,),            # 50
        (51, 152549, 2.23,),            # 51
        (52, 163105, 2.25,),            # 52
        (53, 174186, 2.28,),            # 53
        (54, 185808, 2.30,),            # 54
        (55, 197986, 2.33,),            # 55
        (56, 210739, 2.35,),            # 56
        (57, 224084, 2.38,),            # 57
        (58, 238037, 2.40,),            # 58
        (59, 252616, 2.43,),            # 59
        (60, 267840, 2.45,),            # 60
        (61, 283726, 2.48,),            # 61
        (62, 300293, 2.50,),            # 62
        (63, 317560, 2.53,),            # 63
        (64, 335544, 2.55,),            # 64
        (65, 354266, 2.58,),            # 65
        (66, 373745, 2.60,),            # 66
        (67, 394000, 2.63,),            # 67
        (68, 415050, 2.65,),            # 68
        (69, 436917, 2.68,),            # 69
        (70, 459620, 2.70,),            # 70
        (71, 483180, 2.73,),            # 71
        (72, 507617, 2.75,),            # 72
        (73, 532953, 2.78,),            # 73
        (74, 559209, 2.80,),            # 74
        (75, 586406, 2.83,),            # 75
        (76, 614566, 2.85,),            # 76
        (77, 643712, 2.88,),            # 77
        (78, 673864, 2.90,),            # 78
        (79, 705046, 2.93,),            # 79
        (80, 737280, 2.95,),            # 80
        (81, 770589, 2.98,),            # 81
        (82, 804997, 3.00,),            # 82
        (83, 840527, 3.03,),            # 83
        (84, 877202, 3.05,),            # 84
        (85, 915046, 3.08,),            # 85
        (86, 954084, 3.10,),            # 86
        (87, 994340, 3.13,),            # 87
        (88, 1035837, 3.15,),           # 88
        (89, 1078603, 3.18,),           # 89
        (90, 1122660, 3.20,),           # 90
        (91, 1168035, 3.23,),           # 91
        (92, 1214753, 3.25,),           # 92
        (93, 1262840, 3.28,),           # 93
        (94, 1312323, 3.30,),           # 94
        (95, 1363226, 3.33,),           # 95
        (96, 1415578, 3.35,),           # 96
        (97, 1469404, 3.38,),           # 97
        (98, 1524731, 3.40,),           # 98
        (99, 1581587, 3.43,),           # 99
        (100, 1640000, 3.45,),          # 100
    ]


    actions = [
        # <list>[[N]<tuple>(<str>action,<int>experience,<bool>impact,)]

        # Tutorial, Answers and Comment entities
        ('tuto_validation', 50, False),           # 0
        ('share_waaave', 5, True),                # 1
        ('click_relevant', 1, True),              # 2
        ('click_irrelevant', -5, True),           # 3
        ('visit', 0.05, False),                   # 4

        # User entities
        ('link_facebook', 15, False),             # 5
        ('link_twitter', 15, False),              # 6
        ('link_google', 15, False),               # 7
        ('follower', 5, True),                    # 8
        ('registration_complete', 4, False),      # 9

        # Others
        ('feedback_report', 50, False),           # 10
    ]


    @classmethod
    def get_rank(_class, rank_id):
        """
        Returns the rank tuple according to its id
        """
        assert type(rank_id) is int
        try:
            return _class.ranks[rank_id]
        except IndexError:
            return None


    @classmethod
    def get_rank_from_experience(_class, exp):
        """
        Returns the rank tuple from the user experience
        """
        assert type(exp) is int or float
        try:
            counter = 0
            for rank in _class.ranks:
                if exp < rank[1]: return _class.ranks[counter-1][0]
                counter += 1
            return None
        except IndexError:
            return None


    @classmethod
    def get_action(_class, action_id):
        """
        Returns the action tuple according to its id
        """
        assert type(action_id) is int
        try:
            return _class.actions[action_id]
        except IndexError:
            return None


    @classmethod
    def get_action_by_name(_class, action_name):
        """
        Return the action tuple according to its name
        """
        assert type(action_name) is str
        try:
            counter = 0
            for action_value in _class.actions:
                if action_name == action_value[0]: return _class.actions[counter]
                counter += 1
            return None
        except IndexError:
            return None
