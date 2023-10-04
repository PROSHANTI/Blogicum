
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils import timezone

from blog.models import Comment, Post


def get_posts() -> QuerySet[Post]:
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def get_posts_author(profile: User) -> QuerySet[Comment]:
    return Post.objects.filter(author=profile)


def get_post_pk_comments(pk: int) -> QuerySet[Comment]:
    return (Comment.objects
                   .get_queryset()
                   .filter(post_id=pk)
                   .order_by('created_at'))


def get_comments(profile: User) -> QuerySet[Comment]:
    return Comment.objects.filter(author=profile)


def queryset_annotate(querset: QuerySet[Post]) -> QuerySet[Post]:
    return (querset
            .annotate(comment_count=Count('comment'))
            .order_by('-pub_date')
            )


def get_paginator(objects: QuerySet,
                  page_number: int,
                  posts_on_page: int) -> Page:
    paginator = Paginator(objects, posts_on_page)
    return paginator.get_page(page_number)
