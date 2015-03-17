from urllib import quote
from django import template

register = template.Library()


@register.inclusion_tag('_commons/_page_pagination.jade')
def pagination(page_route, page_current, page_total, url_params={}):
    """
    Generate the pagination block for current page
    """
    left_count, center_count, right_count = 2, 3, 2
    has_more_hidden = page_total > left_count + right_count and True
    left, center, right = [], [], []

    if page_total > center_count:
        # Left range
        left_range_max = left_count if page_total >= left_count\
                                    else page_total
        left.extend([i for i in range(1, left_range_max + 1)])

        # Right range
        right_range_min = page_total - right_count + 1
        right_range_max = page_total
        right.extend([i for i in range(right_range_min, right_range_max + 1)])

    if page_total - left_count + right_count > 0:
        # Center range
        left_max = left[-1] if len(left) else 0
        right_min = right[0] if len(right) else page_total + 1

        center.extend([i for i in range(left_max + 1, right_min)])
        center_len = len(center)

        if page_current in center:
            current_index = center.index(page_current)

            if current_index is 0:
                center = center[0:center_count]
            elif current_index is (center_len - 1):
                center.reverse()
                center = center[0:center_count]
                center.reverse()
            else:
                start_index = (current_index - center_count // 2) or 0
                stop_index = start_index + center_count
                center = center[start_index:stop_index]
        elif page_current in left:
            center = center[0:center_count]
        elif page_current in right:
            center.reverse()
            center = center[0:center_count]
            center.reverse()
        else:
            center = []

    return {
        'url_params': ''.join(['&%s=%s' % (k,quote(v.encode('utf-8')),) for k,v in url_params.items()]),
        'page_route': page_route,
        'page_current': page_current,
        'page_total': page_total,

        'page_previous': page_current - 1 if page_current > 1 else 1,
        'page_next': page_current + 1 if page_current < page_total else page_total,

        'pagination_left': left,
        'pagination_center': center,
        'pagination_right': right,

        'has_more_hidden': has_more_hidden,
    }
