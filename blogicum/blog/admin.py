from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'post',
        'author',
    )


admin.site.empty_value_display = 'Не задано'
