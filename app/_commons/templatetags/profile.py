from django import template

register = template.Library()


@register.inclusion_tag('_commons/_profile_social_networks.jade', takes_context=True)
def social_networks(context, user):
    """
    Return user's social network connections
    """
    association_facebook = user.social_auth.filter(provider='facebook').first()
    association_twitter = user.social_auth.filter(provider='twitter').first()
    association_googleplus = user.social_auth.filter(provider='google-oauth2').first()

    return {
        'social_facebook': association_facebook.uid if association_facebook else None,
        'social_twitter': association_twitter.extra_data['access_token']['screen_name']\
                           if (association_twitter and 'access_token' in association_twitter.extra_data)\
                           else None,
        'social_googleplus': association_googleplus.extra_data['id']\
                              if (association_googleplus and 'id' in association_googleplus.extra_data)\
                              else None,
        'social_website': user.profile.website_url(),
    }


@register.inclusion_tag('_commons/_profile_meta_author.jade', takes_context=True)
def meta_author(context, user):
    """
    Return user's social network connections
    """
    association_googleplus = user.social_auth.filter(provider='google-oauth2').first()

    return {
        'social_googleplus': association_googleplus.extra_data['id']\
                              if (association_googleplus and 'id' in association_googleplus.extra_data)\
                              else None,
    }
