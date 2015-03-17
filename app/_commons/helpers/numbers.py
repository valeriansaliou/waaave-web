import random
from .cache import CacheHelper


def percentage_of(part_1, part_2):
    """
    Returns the percentage between 1 and (1+2)
    """
    try:
        return int('%d' % (float(part_1) / float(part_1 + part_2) * 100))
    except (ValueError, ZeroDivisionError):
        return '0'


def cached_randint(rand_min, rand_max, expiration=60):
    """
    Returns a cached random integer
    """
    assert type(expiration) is int

    namespace = CacheHelper.ns('_commons:helpers:numbers:cached_randint', rand_min=rand_min, rand_max=rand_max)
    result = CacheHelper.io.get(namespace)

    if result is None:
        result = random.randint(rand_min, rand_max)

        CacheHelper.io.set(namespace, result, expiration)

    return result
