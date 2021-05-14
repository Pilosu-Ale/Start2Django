import json
from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone
from django.http import JsonResponse
from .models import Post
from .forms import PostForm, FormRegistration
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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


def registration_view(request):
    if request.method == "POST":
        form = FormRegistration(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = FormRegistration()
    context = {"form": form}
    return render(request, "api/registration.html", context)

