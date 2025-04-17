from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth import login, logout
from .models import Post, Category, UserProfile, PostImage, Comment
from .forms import PostForm, UserRegistrationForm, UserProfileForm, CommentForm, RegisterForm

def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    # posts = Post.objects.filter(title__contains='django1')
    # posts = Post.objects.filter(published_date__year=2025)
    # posts = Post.objects.filter(published_date__month=1, published_date__year=2024)
    # posts = Post.objects.filter(category__name__exact="django")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


# def post(request, title):
#     post = get_object_or_404(Post, slug=title)
#     context = {'post': post}
#     context.update(get_categories())
#     return render(request, "blog/post.html", context)

def post(request, title):
    post = get_object_or_404(Post, slug=title)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post', title=title)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def category(request, name):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.published_date = now()
#             post.save()
#             return index(request)
#     create_form = PostForm()
#     context = {'create_form': create_form}
#     context.update(get_categories())
#     return render(request, "blog/create.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.save()
            for image in request.FILES.getlist('additional_images'):
                PostImage.objects.create(image=image, post=post)

            return redirect('index')
    else:
        form = PostForm()

    context = {'create_form': form}
    context.update(get_categories())
    return render(request, "blog/create.html", context)

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'blog/profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {'form': form}
    context.update(get_categories())
    return render(request, "blog/update_profile.html", context)


@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/my_post.html", context)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('my_posts')
    return render(request, "blog/confirm_delete.html", {'post': post})


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             UserProfile.objects.get_or_create(user=user)
#             return redirect('blog_login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, "blog/registration_user.html", {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, "blog/registration_user.html", {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('index')




def about(request):
    context = {}
    return render(request, "blog/about.html", context)

def services(request):
    context = {}
    return render(request, "blog/services.html", context)

def contact(request):
    context = {}
    return render(request, "blog/contact.html", context)