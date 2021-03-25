from django import forms

from .models import Book, Genres, Review


class BookForm(forms.ModelForm):
    # genres = forms.MultipleChoiceField(
    #         choices=Genres,
    #         initial='0',
    #         widget=forms.SelectMultiple(),
    #         required=False,
    #         label='Genres',
    #     )
    class Meta:
        model = Book
        fields = [
            'title', 'user', 'author', 'genres', 'summary', 'cover_page'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # self.fields['slug'].widget.attrs.update({'hidden': True})
        self.fields['user'].widget.attrs.update({'hidden': True})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['genres'].widget.attrs.update({'class': 'form-control'})
        self.fields['cover_page'].widget.attrs.update({'class': 'form-control'})
        # self.fields['timestamp'].widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'hidden': True})
        self.fields['book'].widget.attrs.update({'hidden': True})
        self.fields['review'].widget.attrs.update({'class': 'form-control'})
