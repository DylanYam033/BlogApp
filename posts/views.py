from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from .models import *
from .forms import *

class PostListView(ListView):
    model = Post
    
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'New Post'
        })
        return context
    

class PostDetailView(DetailView): 
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail_post", slug=post.slug)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form':CommentForm()
        })
        return context

    def get_object(self,**kwargs):
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            PostViewed.objects.get_or_create(user=self.request.user, post=object)

        return object

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Update Post'
        })
        return context

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like[0].delete()
        return redirect('detail_post', slug=slug)
    else:
        Like.objects.create(user=request.user, post=post)
        return redirect('detail_post', slug=slug)
    
 