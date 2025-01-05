from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, EditRequest

def post_list(request):
    user = request.GET.get("usercode", None)
    requested_me = request.GET.get("requested_me", None)
    requested_to = request.GET.get("requested_to", None)
    if user != None:
        posts = Post.objects.filter(author = request.user).order_by('-created_at')
        return render(request, 'post_list.html', {'posts': posts})
    if requested_me != None:
        edit_requests = EditRequest.objects.filter(author=request.user).select_related('post', 'author', 'requested').order_by('-created_at')
        return render(request, 'posts_list_edit.html', {'edit_requests': edit_requests})
    if requested_to != None:
        edit_requests = EditRequest.objects.filter(requested = request.user).select_related('post', 'author', 'requested').order_by('-created_at')
        return render(request, 'posts_list_edit.html', {'edit_requests': edit_requests})
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})
    

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        post.views += 1
        post.save()
    return render(request, 'post_detail.html', {'post': post})

@login_required(login_url='signin')
def post_create(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post = Post.objects.create(author=author, title=title, content=content)
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Please provide both title and content.')
    return render(request, 'post_form.html')

@login_required(login_url='signin')
def post_update(request, pk):
    edit_access = request.GET.get("status", None)
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and edit_access == None and not EditRequest.objects.filter(requested=request.user, post=pk, status="Given").exists:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated successfully!')
            if EditRequest.objects.filter(requested=request.user, post=pk, status="Given").exists:
                req = EditRequest.objects.filter(requested=request.user, post=pk, status="Given")
                req.update(status="Closed")
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Please provide both title and content.')
    
    return render(request, 'post_form.html', {'post': post})

@login_required(login_url='signin')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')

    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required(login_url='signin')
def post_edit_access(request, pk):
    status = request.GET.get("status", "Open")
    requested = request.GET.get("requested", request.user)
    post = get_object_or_404(Post, pk=pk)
    print(EditRequest.objects.filter(author=post.author, post=post).exists())
    if EditRequest.objects.filter(author=post.author, post=post, requested=requested).exists() and status != "Open":
        req = EditRequest.objects.filter(author=post.author, post=post, requested=requested)
        req.update(status = status)
        edit_requests = EditRequest.objects.filter(author=request.user).select_related('post')
        messages.success(request, "Edit request approved successfully.")
        return render(request, 'posts_list_edit.html', {'edit_requests': edit_requests})
    elif EditRequest.objects.filter(author=post.author, post=post, requested=requested).exclude(status="Closed").exists() and status == "Open":
        messages.error(request, "Edit Request Aready Sent.")
    else:
        req = EditRequest.objects.create(author=post.author, post=post, requested=request.user)
        messages.success(request, "Edit request submitted successfully.")
    return redirect('post_detail', pk=post.pk)