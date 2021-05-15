import json
from django.utils import timezone
from django.http import JsonResponse
from .models import Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def posts(request):
    response = []
    postss = Post.objects.filter().order_by('-datetime')
    for post in postss:
        response.append(
            {
                'datetime': post.datetime,
                'content': post.content,
                'author': f"{post.user}",
                'txId': post.txId,
                'hash': post.hash,
            }
        )
    return JsonResponse(response, safe=False)


@csrf_exempt
def newPost(request):
    data = json.loads(request.body)
    user = data['user']
    title = data['title']
    content = data['content']

    username = User.objects.get(username=f"{user}")

    new_post = Post(user=username, title=title, content=content, datetime=timezone.now())
    new_post.writeOnChain()

    response = []
    postss = Post.objects.filter().order_by('-datetime')
    for post in postss:
        response.append(
            {
                'datetime': post.datetime,
                'content': post.content,
                'author': f"{post.user}",
                'txId': post.txId,
                'hash': post.hash,
            }
        )
    return JsonResponse(response, safe=False)




