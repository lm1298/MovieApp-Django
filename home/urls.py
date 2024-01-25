from django.urls import path

from .api_views import CommentAPIViewMovie, CommentAPIViewTV
from . import views
from .views import home
from .views import  watchlist

urlpatterns = [
    path('', views.index, name='index'),
    path("search/", views.search, name="search"),
    path("tv/<int:tv_id>/", views.view_tv_detail, name="tvdetail"),
    path("movie/<int:movie_id>/", views.view_movie_detail, name="moviedetail"),
    path("api/trendings/", views.view_trendings_results, name="trendings"),
    path("movie/<int:movie_id>/comments.html", views.comment_page, name="comment_page"),
    path("tv/<int:tv_id>/comments.html", views.comment_page2, name="comment_page2"),
    path('movie/<int:movie_id>/comments/api', CommentAPIViewMovie.as_view(), name='movie_comments_api'),
    path('tv/<int:tv_id>/comments/api', CommentAPIViewTV.as_view(), name='tv_comments_api'),
    path('',home, name='home'),
    path('add_movie_to_watchlist/<int:movie_id>/', views.add_movie_to_watchlist, name='add_movie_to_watchlist'),
    path('add_tv_to_watchlist/<int:tv_id>/', views.add_tv_to_watchlist, name='add_tv_to_watchlist'),
    path('watchlist/', watchlist, name='watchlist'),
    path('remove_from_watchlist/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    
]