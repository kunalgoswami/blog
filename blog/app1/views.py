from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post


# Create your views here.
# homepage

def home(request):
    post = Post.objects.all()
    return render(request, 'app1/home.html', {'post': post})


# about page

def about(request):
    return render(request, 'app1/about.html')


# contact page

def contact(request):
    return render(request, 'app1/contact.html')


# dashboard page

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user.id)

        return render(request, 'app1/dashboard.html', {'posts': posts})

    else:
        return HttpResponseRedirect('/login/')


# login page

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, 'invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'app1/login.html', {'form': form})


# signup page

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'account created successfully')
            return HttpResponseRedirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'app1/signup.html', {'form': form})


# logout page

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# add post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                form = PostForm()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
            return render(request, 'app1/addpost.html', {'form': form})
    else:
        HttpResponseRedirect('/login/')


# update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            up = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=up)
            if form.is_valid():
                form.save()
        else:
            up = Post.objects.get(pk=id)
            form = PostForm(instance=up)
        return render(request, 'app1/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            up = Post.objects.get(pk=id)
            up.delete()
            return HttpResponseRedirect('/dashboard/')

    else:
        return HttpResponseRedirect('/login/')
