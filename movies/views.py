from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import *
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["star_form"] = RatingForm()

        user = self.request.user
        movie = kwargs.get('object')

        if user.id:
            favorite_list, created = Favorites.objects.get_or_create(user=user)

            if favorite_list.movies.filter(id=movie.pk).exists():
                context['is_favourite'] = True
            else:
                context['is_favourite'] = False
        return context


class MainMoviesView(ListView):
    """Сортировка фильмов по рейтингу"""
    template_name = 'home.html'
    model = Movie
    queryset = Movie.objects.filter(draft=False).order_by('-rating')[:30]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context


class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов"""
    def get_queryset(self):
        if self.request.GET.getlist("year"):
            if self.request.GET.getlist("genre"):
                queryset = Movie.objects.filter(
                    Q(year__in=self.request.GET.getlist("year")) &
                    Q(genres__in=self.request.GET.getlist("genre")) &
                    Q(draft = False)
                ).distinct()
            else:
                queryset = Movie.objects.filter(
                    Q(year__in=self.request.GET.getlist("year"))&
                    Q(draft=False)
                ).distinct()
        else:
            if self.request.GET.getlist("genre"):
                queryset = Movie.objects.filter(
                    Q(genres__in=self.request.GET.getlist("genre"))&
                    Q(draft=False)
                ).distinct()

        return queryset


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie_id = pk
            form.user = request.user
            movie = Movie.objects.filter(id=pk).first()
            form.save()
        return HttpResponseRedirect(movie.get_absolute_url())


class Search(ListView):
    """Поиск фильмов"""
    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class AddStarRating(View):
    """Добавление рейтинга к фильму"""
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user_id=request.POST.get("user"),
                movie_id=request.POST.get("movie"),
                defaults={'star': request.POST.get("star")},
            )
            film = Movie.objects.get(id=request.POST.get("movie"))
            new_rating = film.average_rating()
            film.rating = new_rating
            film.save()

            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class FavouriteMovieView(DetailView):
    """Избранное"""
    model = Favorites

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.filter(url=kwargs["slug"]).first()

        favorite_list, created = Favorites.objects.get_or_create(user=request.user)
        if favorite_list.movies.filter(id=movie.pk).exists():
            favorite_list.movies.remove(movie.pk)
        else:
            favorite_list.movies.add(movie.pk)
        favorite_list.save()
        return HttpResponseRedirect(movie.get_absolute_url())


class FavoritesListView(ListView):
    """Список любимых фильмов"""
    model = Favorites
    template_name = 'favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        favorite_list, created = Favorites.objects.get_or_create(user=user)
        context["favourite_movies"] = favorite_list.movies.all()
        return context