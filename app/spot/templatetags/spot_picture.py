from django import template
from django.template.loader import render_to_string


register = template.Library()


def spot_picture(spot, size='normal'):
    """
    Return the generated spot picture HTML
    """
    size = size if size in ('small', 'large') else 'normal'
    picture_url = getattr(spot, ('url_picture_%s' % size))()

    spot_picture_img = u'<img src="{src}" class="{class_}" alt="{alt}" height="{height}" width="{width}"/>'.format(
        src=picture_url,
        class_='picture',
        alt='',
        height=size,
        width=size,
    )

    return render_to_string('spot/_spot_picture.jade', {
        'spot': spot,
        'spot_picture': spot_picture_img,
        'size': size,
    })


@register.simple_tag
def spot_picture_small(spot):
    """
    Return spot's small picture
    """
    return spot_picture(spot, 'small')


@register.simple_tag
def spot_picture_normal(spot):
    """
    Return spot's normal picture
    """
    return spot_picture(spot, 'normal')


@register.simple_tag
def spot_picture_large(spot):
    """
    Return spot's large picture
    """
    return spot_picture(spot, 'large')
