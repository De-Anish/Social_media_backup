from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tweets/create/', views.tweet_create, name='tweet_create'),
    path('tweets/<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('tweets/<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('follow/', views.follow_user, name='follow_user'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('like-ajax/<int:tweet_id>/', views.like_tweet_ajax, name='like_tweet_ajax'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('comment/<int:tweet_id>/', views.add_comment, name='add_comment'),
    path('my-posts/', views.my_posts, name='my_posts'),
] 