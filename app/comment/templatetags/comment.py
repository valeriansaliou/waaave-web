from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def comment(context, item_type, item_id):
    context['item_type'] = item_type
    context['item_id'] = item_id

    if item_type == 'book':
        context['comment_placeholder'] = 'Leave a review of this book for others to see. Be precise and correct in your language.'
    elif item_type == 'tutorial':
        context['comment_placeholder'] = 'Leave a comment. Avoid comments like +1 or thanks.'

    return render_to_string('comment/comment.jade', context)
