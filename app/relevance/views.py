import json
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext

from _index.helpers import ContentHelper as _IndexContentHelper
from _commons.helpers.redirects import login_required_url, register_required_url

from .helpers import *
from .templatetags.relevance_buttons import relevance_buttons


def action(request, item_type, item_id):
    """
    Relevance > Action
    """
    # Validate item data
    item = _IndexContentHelper.get(item_id, item_type)

    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if item:
        if request.method == 'POST':
            value = request.POST.get('relevance', '') or ''

            if value:
                if request.user.is_authenticated():
                    # Update relevance
                    RelevanceHelper.update(request.user, item, value)
                    
                    # Generate & return response
                    return render(request, 'relevance/relevance_action.jade', {
                        'item_type': item_type,
                        'item_id': item_id,
                    })
                
                else:
                    result['message'] = 'Not authenticated'
                    result['contents']['redirect'] = {
                        'login': login_required_url(request.META.get('HTTP_REFERER', '/')),
                        'register': register_required_url(),
                    }
            else:
                result['message'] = 'Not enough data'
        else:
            result['message'] = 'Bad request'
    else:
        result['message'] = 'Not found'
    
    return HttpResponse(json.dumps(result), content_type='application/json')
