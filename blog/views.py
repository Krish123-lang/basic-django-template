from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Post
from .forms import PostForm
from django.contrib import messages
# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def create_post(request):
    form = PostForm()
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'blog/post_form.html', context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'blog/post_form.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

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


def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    context = {'post': post}    
    
    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html',context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('home')