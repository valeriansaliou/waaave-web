from django import template
from relevance.helpers import *

register = template.Library()


@register.inclusion_tag('relevance/relevance_buttons.jade', takes_context=True)
def relevance_buttons(context, item_type, item_id):
    relevance_data = RelevanceHelper.get(item_type, item_id, user=context['request'].user)
    relevance_data.update({
        'item_type': item_type,
        'item_id': item_id,
    })

    return relevance_data
