from django import template

register = template.Library()


@register.inclusion_tag('search/_search_form.jade', takes_context=True)
def search_form(context, search_url_params={}):
    """
    Generate the search form
    """
    # Known types
    search_types = {
      'all': 'Search All',
      'tutorials': 'Tutorials',
      # 'books': 'Books',
      'spots': 'Spots',
      'users': 'Users',
    }

    # Read passed data
    search_id = search_url_params['t']\
                if 't' in search_url_params and search_url_params['t'] in search_types\
                else 'all'

    # Retrieve active type
    search_active = {
      'id': search_id,
      'value': search_types.pop(search_id),
    }

    return {
        'search_params': search_url_params,

        'search_types': search_types,
        'search_active': search_active,
    }
