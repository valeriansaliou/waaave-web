from random import randint

from django.db.models.query import QuerySet



class FieldsHelper(object):
    """
    An helper on fields operations
    """

    @staticmethod
    def random(model, number):
        """
        Return random rows from database
        """
        results = []
        results_indexes = []

        instances = model if isinstance(model, QuerySet) else model.objects
        count = instances.count()
        range_end = count - 1

        if number > count:
            number = count
        
        if range_end >= 0:
            while True:
                random_index = randint(0, range_end) if range_end > 0 else 0

                if not random_index in results_indexes:
                    results_indexes.append(random_index)
                    results.append(instances.all()[random_index])

                if len(results_indexes) >= number:
                    break

        return results
