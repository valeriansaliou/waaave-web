def humanize(seconds):
    """
    Convert a duration in seconds to an human-readable form
    """
    assert type(seconds) is int
    if seconds >= 86400:
        res = seconds // 86400
        return '%s day' % res if res == 1 else '%s days' % res
    if seconds >= 3600:
        res = seconds // 3600
        return '%s hour' % res if res == 1 else '%s hours' % res
    if seconds >= 60:
        res = seconds // 60
        return '%s minute' % res if res == 1 else '%s minutes' % res
    return '%s second' % seconds if seconds == 1 else '%s seconds' % seconds
