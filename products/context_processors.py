set_head = {'descr': '', 'author': '', 'title': '', 'custom_css': ''}


def head(request):
    print(set_head)
    return {'head': set_head}
