from django.forms import ModelForm

from polls.models import BookReview


class BookReview_form(ModelForm):
    class Meta:
        model=BookReview
        fields="__all__"