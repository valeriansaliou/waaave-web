from django import template
from django.template.loader import render_to_string
from _commons.shortcuts import get_user


register = template.Library()


@register.simple_tag
def get_rank(user=None):
    if user:
        user = get_user(user_id=user.id)
        return render_to_string('_commons/_rank.jade', { 'user': user })
    else:
        return None

