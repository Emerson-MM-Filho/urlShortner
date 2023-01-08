from django.shortcuts import redirect, get_object_or_404

from url.models import Url


def redirect_view(request, *args, **kwargs):
    if request.method == 'GET':
        url = get_object_or_404(Url, short_url=kwargs.get('short_url'))
        url.use_counter += 1
        url.save()
        return redirect(url.original_url)
