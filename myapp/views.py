# myapp/views.py

from django.contrib.auth.decorators import login_required #데코레이터(@)를 사용하려면 필수로 필요함.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm, CommentForm

class PostEditMixin(PermissionRequiredMixin):
    permission_required = 'myapp.change_post'
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.author:
            raise Http404("You don't have permission to edit this post.")
        return obj

class PostDeleteMixin(PermissionRequiredMixin):
    permission_required = 'myapp.delete_post'
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.author:
            raise Http404("You don't have permission to delete this post.")
        return obj

class PostEditView(LoginRequiredMixin, PostEditMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(LoginRequiredMixin, PostDeleteMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'post_list.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'post_form.html', context)

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_list')
    else:
        form = CommentForm()
    context = {'form': form, 'post': post}
    return render(request, 'comment_form.html', context)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    context = {'post': post}
    return render(request, 'post_confirm_delete.html', context)

@login_required
def comment_delete(request, board_id, comment_id):
    post = get_object_or_404(Post, pk=board_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('post_list')
    
    context = {'comment': comment, 'post': post}
    return render(request, 'comment_confirm_delete.html', context)

