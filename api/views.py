from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
import json
from django.utils import timezone
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import PostForm


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


@login_required
def homepage(request):
    postList = Post.objects.filter().order_by('datetime')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            username = User.objects.get(username=f"{request.user}")
            new_post = Post(user=username, title=title, content=content, datetime=timezone.now())
            new_post.writeOnChain()

        return HttpResponseRedirect("/")
    else:
        form = PostForm()
    return render(request, "api/homepage.html", {'form': form, 'postList': postList})


def userPage(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {"user": user}
    return render(request, "api/userPage.html", context)
