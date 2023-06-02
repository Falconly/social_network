from django import forms

from posts import models


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['content'].widget.attrs.update({'width': '100%',
                                                    'rows': '3',
                                                    'placeholder': 'Раскажите что у вас нового...'})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.Posts
        fields = ('content', 'image', 'category', 'user', 'profile')

