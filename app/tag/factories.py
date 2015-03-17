from .models import *


class TagFactory:
    """
    Builds tags and retrieve them from the database
    """
    
    def __init__(self, slug=None, uid=None):
        self.slug = slug
        self.uid = uid


    def search(self, name=None):
        """
        Searches for a tag with provided name
        """
        return List.objects.filter(slug__contains=self.slug)


    def exists(self):
        """
        Checks if tag exists
        """
        return List.objects.filter(slug=self.slug).exists() if self.slug else False


    def delete(self):
        """
        Deletes tag
        """
        db_slug_all = List.objects.filter(slug=self.slug)

        if db_slug_all.exists:
            db_slug_all.delete()
            return True

        return False


    def read(self):
        """
        Reads tag
        """
        try:
            return List.objects.get(slug=self.slug)
        except List.DoesNotExist:
            return None


    def store(self, data):
        """
        Stores tag
        """
        can_edit = False
        db_list = self.read()

        if db_list is None:
            can_edit = True
            db_list = List()
        elif db_list.author_id == self.uid:
            can_edit = True

        if can_edit:
            db_list.name = data['name']
            db_list.description = data['desc']
            db_list.slug = self.slug
            db_list.author_id = self.uid

            db_list.save()

        return db_list
