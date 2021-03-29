from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .templatetags.auth_extras import can_write_blogs

from .models import User, Group, Post, Comment

from markdown2 import markdown


def can_write_blogs(user):
    return user.groups.filter(name="can_write_blogs").exists()


def index(request):
    posts = Post.objects.all().order_by("-post_time")
    return render(request, "blogapp/index.html", {"posts": posts})


def page(request, page_id):
    if request.method == "POST":
        comment_page = Post.objects.get(id=page_id)
        comment_author = request.user
        # comment_time is set automatically
        comment_body = request.POST["newCommentText"]
        if comment_body == "":
            pass
        else:
            comment = Comment(
                comment_page=comment_page,
                comment_author=comment_author,
                comment_body=comment_body,
            )
            comment.save()
    page_content = Post.objects.get(id=page_id)
    comments = page_content.comments.all().order_by("-comment_time")
    return render(
        request,
        "blogapp/page.html",
        {
            "page_content": page_content,
            "page_id": page_id,
            "comments": comments,
        },
    )


def register_view(request):
    if request.method == "POST":
        first_name = request.POST["inputFirstName"]
        last_name = request.POST["inputLastName"]
        username = request.POST["inputUsername"]
        email = request.POST["inputEmail"]
        can_write_blogs = request.POST.get("canWriteBlogs", False)

        # Ensure password matches confirmation
        password = request.POST["inputPassword"]
        confirmation = request.POST["inputPasswordConfirm"]
        if password != confirmation:
            return render(
                request, "blogapp/register.html", {"message": "Passwords must match."}
            )

        # Checking that required fields are entered
        if "" in [first_name, username, password]:
            return render(
                request,
                "blogapp/register.html",
                {"message": "Required fields must not be blank."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            if can_write_blogs != False:
                cwb_group, created = Group.objects.get_or_create(name="can_write_blogs")
                cwb_group.user_set.add(user)
            user.save()
        except IntegrityError:
            return render(
                request, "blogapp/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blogapp/register.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["inputUsername"]
        password = request.POST["inputPassword"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "blogapp/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "blogapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def newpost(request):
    if can_write_blogs(request.user):
        if request.method == "POST":
            title = request.POST["inputTitle"]
            subtitle = request.POST["inputSubtitle"]
            author = request.user
            # post_time is set automatically
            body_md = request.POST["newPostBody"]
            body_html = markdown(body_md)  # converting the markdown text into html

            # Checking that required fields are entered
            if "" in [title, body_md]:
                return render(
                    request,
                    "blogapp/newpost.html",
                    {"message": "Required fields must not be blank."},
                )
            # Creating the post. If the title is already taken, sends message to the user
            try:
                post = Post(
                    post_title=title,
                    post_subtitle=subtitle,
                    post_author=author,
                    post_body_md=body_md,
                    post_body_html=body_html,
                )
                post.save()
            except IntegrityError:
                return render(
                    request,
                    "blogapp/newpost.html",
                    {
                        "message": "Another post with similar title already exists.",
                        "title": title,  # passing the already written content to avoid its loss
                        "subtitle": subtitle,
                        "body": body_md,
                    },
                )

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "blogapp/newpost.html")
    else:
        return HttpResponse("You are not allowed to write blogs.")