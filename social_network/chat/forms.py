from django import forms

from chat import models


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control',
                                                 'style': 'resize:none;display:block;float:left;',
                                                 'placeholder': 'Написать сообщение...',
                                                 'rows': '1',})

    class Meta:
        fields = ('to_user', 'from_user', 'text', 'chat')
        model = models.Messages
