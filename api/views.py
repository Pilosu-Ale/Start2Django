from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
import json
from django.utils import timezone
from django.http import JsonResponse
from .models import Post
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import PostForm
from django.db.models import Count
from datetime import timedelta
from django.core.cache import cache


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


def homepage(request):

    if cache.get("cache"):
        postList = cache.get("cache")
        print("Data from cache")

    else:
        postList = Post.objects.filter().order_by('-datetime')
        cache.set("cache", postList)
        print("Data from DB")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            username = User.objects.get(username=f"{request.user}")
            new_post = Post(user=username, title=title, content=content, datetime=timezone.now())
            new_post.writeOnChain()
            cache.expire("cache", timeout=0)
        return HttpResponseRedirect("/")
    else:
        form = PostForm()
    return render(request, "api/homepage.html", {'form': form, 'postList': postList})


def userPage(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "api/userPage.html", {"user": user})


@staff_member_required
def usersList(request):
    user_posts = User.objects.annotate(total_posts=Count('post'))

    return render(request, "api/users_list.html", {'user_posts': user_posts})


def posts1h(request):
    response = []
    postList = Post.objects.filter(datetime__gte=timezone.now() - timedelta(hours=1))
    for post in postList:
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


def controlString(request, word):
    response = []
    postList = Post.objects.filter().order_by('-datetime')
    countString = 0
    for post in postList:
        if word in post.content:
            countString += 1
        if word in post.title:
            countString += 1
        if word in post.hash:
            countString += 1
        if word in post.txId:
            countString += 1

    response.append(
        {
            'countString': countString
        }
    )
    return JsonResponse(response, safe=False)
