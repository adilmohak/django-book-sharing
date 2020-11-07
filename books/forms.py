from django import forms

from .models import Book, GENRES, Genres


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
            'genres', 'slug', 'user', 'title', 'author', 'summary', 'cover_page'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'hidden': True})
        self.fields['user'].widget.attrs.update({'hidden': True})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['genres'].widget.attrs.update({'class': 'form-control'})
        self.fields['cover_page'].widget.attrs.update({'class': 'form-control'})
        # self.fields['timestamp'].widget.attrs.update({'class': 'form-control'})
