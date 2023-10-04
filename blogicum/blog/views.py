from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone as timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import CommentForm, PostForm, UserForm
from blog.mixins import (CommentMixin, DispatchNeededMixin, PostMixin,
                         PostModelMixin)
from blog.models import Category, Post
from blog.service import (get_post_pk_comments, get_posts, get_posts_author,
                          queryset_annotate)

AMOUNT_OBJ_ON_ONE_PAGE = 10


class AddCommentView(LoginRequiredMixin, CommentMixin, CreateView):

    def form_valid(self, form: Form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['pk']}
        )


class EditCommentView(LoginRequiredMixin,
                      DispatchNeededMixin,
                      CommentMixin,
                      UpdateView):
    pk_url_kwarg = 'comment_id'

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['post_id']}
        )


class DeleteCommentView(LoginRequiredMixin,
                        DispatchNeededMixin, CommentMixin, DeleteView):
    pk_url_kwarg = 'comment_id'

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs={
                'pk': self.kwargs['post_id']}
        )


class IndexView(PostMixin, ListView):
    template_name = 'blog/index.html'
    queryset = queryset_annotate(get_posts())


class PostDetailView(DispatchNeededMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = get_post_pk_comments(self.kwargs['pk'])
        return context


class CategoryPostsView(PostMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Post]:
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug,
                                          is_published=True)
        return queryset_annotate(get_posts()).filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category

        return context


class ProfileView(PostMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        self.profile = get_object_or_404(User,
                                         username=self.kwargs["username"])
        if self.request.user == self.profile:
            return queryset_annotate(get_posts_author(self.profile))
        return (queryset_annotate(get_posts_author(self.profile))
                .filter(is_published=True,
                        pub_date__lte=timezone.now())
                .order_by('-pub_date'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context


class UserUpdateProfileView(LoginRequiredMixin,
                            DispatchNeededMixin,
                            UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('profile')
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin,
                     DispatchNeededMixin,
                     PostModelMixin,
                     UpdateView):
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, PostModelMixin, CreateView):

    def get_success_url(self) -> str:
        username = self.request.user.username
        return reverse(
            'blog:profile',
            kwargs={
                'username': username
            })

    def form_valid(self, form: Form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DispatchNeededMixin, DeleteView):
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context
