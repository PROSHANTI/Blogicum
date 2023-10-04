from django.urls import path

from blog import views

profile_url = [
    path('edit/', views.UserUpdateProfileView.as_view(), name='edit_profile'),
    path('<slug:username>/', views.ProfileView.as_view(), name='profile'),

]
