from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post

AMOUNT_OBJ_ON_ONE_PAGE = 10


class DispatchNeededMixin:
    def dispatch_comment(self, request: HttpRequest, *args, **kwargs):
        comment = get_object_or_404(self.model, pk=self.kwargs['comment_id'])
        if comment.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def dispatch_post_detail(self, request: HttpRequest, *args, **kwargs):
        instance = get_object_or_404(self.model, id=self.kwargs['pk'])
        if instance.is_published is False and request.user != instance.author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def dispatch_post_delete(self, request: HttpRequest, *args, **kwargs):
        post = get_object_or_404(self.model, pk=self.kwargs['post_id'])
        if post.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def dispatch_post_update(self, request: HttpRequest, *args, **kwargs):
        instance = get_object_or_404(self.model, id=self.kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        view_name = request.resolver_match.view_name
        dispatch_dict = {
            'blog:edit_comment': self.dispatch_comment,
            'blog:delete_comment': self.dispatch_comment,
            'blog:post_detail': self.dispatch_post_detail,
            'blog:delete_post': self.dispatch_post_delete,
            'blog:edit_post': self.dispatch_post_update,
        }
        for view_url in dispatch_dict:
            if view_name == view_url:
                return dispatch_dict[view_url](request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class PostMixin:
    model = Post
    paginate_by = AMOUNT_OBJ_ON_ONE_PAGE


class PostModelMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class CommentMixin:
    form_class = CommentForm
    model = Comment
    template_name = 'blog/comment.html'
