1. `django-admin startproject project .`
2. `python3 manage.py startapp blog`
2. `python3 manage.py startapp users`
3. `urls.py(project)`
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("", include("users.urls")),
]
```
5. `settings.py`
```
INSTALLED_APPS = [
    ...
    "blog",
    "users",
]

TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR, "templates"],
        ...
    },
]

LOGIN_URL = 'login'
```
6. `urls.py(blog)`
```
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('post/create', views.create_post, name='post-create'),
    path('post/edit/<int:id>/', views.edit_post, name='post-edit'),
    path('post/delete/<int:id>/', views.delete_post, name='post-delete'),
]
```
7. `views.py(blog)`
```
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Post
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/home.html", context)

@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'blog/post_form.html', context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'blog/post_form.html', {'form': form})


@login_required
def edit_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, id=id)

    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {'form': form, 'id': id}
        return render(request,'blog/post_form.html',context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog/post_form.html',{'form':form})

@login_required
def delete_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post}    
    
    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html',context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('home')
```
8. `models.py(blog)`
```
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_at']
```
9. `forms.py(blog)`
```
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```
## Template (Blog)
10. `home.html`
```
{% include "base.html" %}
{% block content %}
<h1>Home</h1>

<a href="{% url "post-create" %}">Create Post</a>
{% for post in posts %} 
    <h1> {{post.title}} </h1>
    <p> {{post.content}} </p>
    <i> {{ post.published_at | date:"M d, Y h:i A" }} by <b> {{ post.author | title}}</b> </i>

    {% if request.user.is_authenticated and request.user == post.author %}
		<p>
			<a href="{% url 'post-edit' post.id %}">Edit</a> 
			<a href="{% url 'post-delete' post.id%}">Delete</a>
		</p>
	{% endif %}
{% endfor %}
{% endblock content %}
```
11. `post_form.html`
```
{% include "base.html" %}
{% block content %}
<a href="{% url "home" %}">Home</a>
<h2>{% if id %} Edit {% else %} New {% endif %} Post</h2>

<form action="" method="post" novalidate>
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Submit">
</form>
{% endblock content %}
```
12. `post_confirm_delete.html`
```
{% include "base.html" %}
{% block content %}
<h2>Delete Post</h2>
<form method="POST">
  {% csrf_token %}
  <p>Are you sure that you want to delete the post "{{post.title}}"?</p>
  <div>
    <button type="submit">Yes, Delete</button>
    <a href="{% url 'home' %}">Cancel</a>
  </div>
</form>
{% endblock content %}
```
13. `base.html (Root Folder)`
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Site</title>
  </head>
  <body>
  	<header>
	{%if request.user.is_authenticated %}
		<a href="{% url 'home' %}">My Posts</a>
		<a href="{% url 'post-create' %}">New Post</a>
		<span>Hi {{ request.user.username | title }}</span>
		<a href="{% url 'logout' %}">Logout</a>
	{%else%}
		<a href="{% url 'login' %}">Login</a>
		<a href="{% url 'register' %}">Register</a>
	{%endif%}
  	</header>
  	<main>
	  	{% if messages %}
			<div class="messages">
			{% for message in messages %}
				<div class="alert {% if message.tags %}alert-{{ message.tags }}"{% endif %}>
					{{ message }}
				</div>
			{% endfor %}
			</div>
		{% endif %}  
	    {%block content%} 
	    {%endblock content%}
  	</main>
	
  </body>
</html>
```
# Users
1. `urls.py(users)`
```
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
]
```
2. `views.py(users)`
```
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('posts')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('home')
        # either form not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})

def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')
```
3. `forms.py(users)`
```
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```
## Templates(Users)
4. `users/login.html`
```
{% include "base.html" %}
{% block content %}
<form method="POST" novalidate>
	{% csrf_token %}
	<h2>Login</h2>
	{{form.as_p}}
	<input type="submit" value="Login" />
	<p>Don't have an account? <a href="{%url 'register' %}">Register</a></p>
</form>
{% endblock content %}
```
5. `users/register.html`
```
{% extends 'base.html' %}
{% block content %}
<form method="POST" novalidate>
	{% csrf_token %}
	<h2>Sign Up</h2>
	{% for field in form %}
	<p>
		{% if field.errors %}
		<ul class="errorlist">
			{% for error in field.errors %}
			<li>{{ error }}</li>
			{% endfor %}
		</ul>
		{% endif %}
	 	{{ field.label_tag }} {{ field }}
	</p>
	{% endfor %}
	<input type="submit" value="Register" />
	<p>Already has an account? <a href="{%url 'login' %}">Login</a></p>
</form>
{% endblock content%}
```
![1](https://github.com/Krish123-lang/basic-django-template/assets/56486342/45f31561-1e8c-4e0d-ad5e-cca8a4f83789)
![2](https://github.com/Krish123-lang/basic-django-template/assets/56486342/3e642bd0-1db6-4910-9e09-b48833c5f3cc)
![3](https://github.com/Krish123-lang/basic-django-template/assets/56486342/4df36e07-075d-4fbb-851a-6a0c3f89b3a0)
![4](https://github.com/Krish123-lang/basic-django-template/assets/56486342/4ea7397e-9bad-4b07-8f5d-bea0ad4a410d)
![5](https://github.com/Krish123-lang/basic-django-template/assets/56486342/c6792063-4cda-45f9-b6fe-0788e39b97d2)
