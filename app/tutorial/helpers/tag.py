class TagHelper(object):
    """
    An helper on tag operations
    """

    @staticmethod
    def list(tutorial, priority=False):
        """
        Return a list of tutorial tags
        """
        if not tutorial:
            return []

        tags = {}
        tags_list = []
        priority_tag = None

        for tag in tutorial.tutorial_tags.all():
            tags[tag.tag.slug] = tag.tag.name
            tags_list.append(tag.tag.slug)

        # Get priority tag?
        if priority:
            tutorial_url = tutorial.url_set.filter(is_alias=False).first()

            if tutorial_url:
                priority_tag = tutorial_url.tag

        # Move priority tag first?
        if priority_tag and priority_tag in tags_list:
            tags_list.remove(priority_tag)
            tags_list = [priority_tag] + tags_list

        # Build final tag object
        return [{'name': tags[tag], 'slug': tag} for tag in tags_list]


    @staticmethod
    def list_instances(tutorial):
        """
        Return a list of tutorial tags (instances and not processed dict)
        """
        return [t.tag for t in tutorial.tutorial_tags.all()]
