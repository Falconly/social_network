from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect

from posts import models


# Create your views here.
@login_required
def delete_post(request, post_pk):

    post = models.Posts.objects.post(post_pk)
    if request.user == post.user:
        post.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('Это не ваш пост')

