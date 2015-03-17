from django.shortcuts import render


def root(request):
    """
    Shot > Root
    """
    return render(request, 'shot/shot_root.jade')

def tag(request, tag):
    """
    Shot > tag
    """
    return render(request, 'shot/shot_tag.jade')

def view(request, tag, slug):
    """
    Shot > View
    """
    return render(request, 'shot/shot_view.jade')