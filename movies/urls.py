from django.urls import path

from . import views


urlpatterns = [
    path("", views.MainMoviesView.as_view(), name="home"),
    path("movies/", views.MoviesView.as_view(), name="movies"),
    path("movies/filter/", views.FilterMoviesView.as_view(), name="filter"),
    path("movies/add-rating/", views.AddStarRating.as_view(), name="add_rating"),
    path("movies/search/", views.Search.as_view(), name="search"),
    path("movies/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("movies/<slug:slug>/favourite/", views.FavouriteMovieView.as_view(), name="favourite"),
    path("movies/review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]