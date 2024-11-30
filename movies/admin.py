from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("id", "name")


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    # fields = (("actors", "directors", "genres"), )
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": ("rating",)
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Актеры", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Параметры", {
            "fields": (("url", "draft",),)
        }),
    )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "id")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "star", "user")
    readonly_fields = ("movie", "star", "user")


admin.site.register(Genre)
admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Favorites)

