from django.urls import path

from blog import views

posts_url = [
    path('<int:pk>/comment/',
         views.AddCommentView.as_view(),
         name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.EditCommentView.as_view(),
         name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.DeleteCommentView.as_view(),
         name='delete_comment'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('<int:pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
]
