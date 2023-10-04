from django.urls import include, path

from blog import views
from blog.apps import BlogConfig

from .posts_url import posts_url
from .profile_url import profile_url

app_name = BlogConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', include(posts_url)),
    path('profile/', include(profile_url)),
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(),
         name='category_posts'),

]
