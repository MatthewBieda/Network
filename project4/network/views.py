import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import NewPost

from .models import Post, User


class index(CreateView):

    model = Post
    form_class = NewPost
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts =  Post.objects.order_by('-date_posted')
        #context["posts"] = posts

        #Implement pagination
        post_paginator = Paginator(posts, 10)
        page_num = self.request.GET.get('page')
        page = post_paginator.get_page(page_num)
        context["page"] = page
        context["count"] = post_paginator.count

        if self.request.method == "PUT":
            body_data = json.loads(self.request.body)

            postid = body_data['id']
            updatedpost = body_data['content']
            Post.objects.filter(id=postid).update(content=updatedpost)

        if self.request.method == "POST":
            post_data = json.loads(self.request.body)

            desiredaction = post_data['desiredaction']
            likeid = post_data['id']

            if desiredaction == "Like":
                postobject = Post.objects.get(id=likeid)
                postobject.likes.add(self.request.user)
            elif desiredaction == "Unlike":
                postobject = Post.objects.get(id=likeid)
                postobject.likes.remove(self.request.user)

        userinfo = self.request.user

        if self.request.user.is_authenticated:
            logged_in_user_details = User.objects.get(id=userinfo.id)
            likedposts = logged_in_user_details.likes_relation.all()
            context["likedposts"] = likedposts

        return context


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def profile(request, id):

    user = request.user
    #Get user details
    User_Details = User.objects.get(id=id)
    followers = User_Details.followers.all()
    following = User_Details.following.all()

    number_of_followers = len(followers)
    number_of_following = len(following)

    if user in followers:
        already_followed = True
    else:
        already_followed = False

    #Get post details
    Posts = Post.objects.filter(author=id).order_by('-date_posted')

    if request.user.is_authenticated:
        logged_in_user_details = User.objects.get(id=user.id)
        likedposts = logged_in_user_details.likes_relation.all()

    #Implement pagination
    post_paginator = Paginator(Posts, 10)
    page_num = request.GET.get('page')
    page = post_paginator.get_page(page_num)

   
    context = {
        'profile': User_Details,
        'posts': Posts,
        'user': user,
        'followers': followers,
        'follower_number': number_of_followers,
        'following_number': number_of_following,
        'already_followed': already_followed,
        'likedposts': likedposts,
        'posts': Posts,
        'page': page,
        'count': post_paginator.count
    }

    if request.method == "POST":
        if request.POST.get("link") == "Unfollow":
            User_Details.followers.remove(user)
        elif request.POST.get("link") == "Follow":
            User_Details.followers.add(user)
        
        return redirect("following")

    return render(request, "network/profile.html", context)

def following(request):

    #Get currently logged in user
    user = request.user

    #Get list of users followed
    logged_in_user_object = User.objects.get(id=user.id)
    following = logged_in_user_object.following.all()
    
    # Use the queryset of using being followed to filter all posts and order by reverse time posted
    Posts = Post.objects.filter(author__in=following).order_by('-date_posted')

    if request.user.is_authenticated:
        logged_in_user_details = User.objects.get(id=user.id)
        likedposts = logged_in_user_details.likes_relation.all()

    #Implement pagination
    post_paginator = Paginator(Posts, 10)
    page_num = request.GET.get('page')
    page = post_paginator.get_page(page_num)
        
    #Use those posts to populate the page
    context = {
        'posts': Posts,
        'likedposts': likedposts,
        'page': page,
        'count': post_paginator.count
    }
    
    return render(request, "following.html", context)