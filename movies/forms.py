from django import forms

from .models import Reviews, Rating


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ("text",)


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    class Meta:
        model = Rating
        fields = ("star",)