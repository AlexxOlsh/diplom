from django.contrib.auth.models import User
from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=200, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=350)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    rating = models.FloatField("Рейтинг фильма", default=3.5)
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def average_rating(self):
        ratings = self.ratings.all()
        return ratings.aggregate(models.Avg('star'))['star__avg'] or 3.5

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    star = models.SmallIntegerField("Звезда", default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    text = models.TextField("Сообщение", max_length=5000)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.user.username} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Favorites(models.Model):
    """Избранное"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


