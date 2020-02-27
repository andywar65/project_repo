from django import forms
from django.forms import ModelForm
from .models import UserUpload, Event, Blog
from users.models import User

class UserUploadForm(ModelForm):
    body = forms.CharField(label = 'Testo',
        widget=forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)

class EventForm(ModelForm):
    manager = forms.ModelChoiceField(label="Responsabile", required = False,
        queryset = User.objects.with_perm('pagine.add_event').order_by('username'), )

    class Meta:
        model = Event
        fields = '__all__'

class BlogForm(ModelForm):
    author = forms.ModelChoiceField(label="Autore", required = False,
        queryset = User.objects.filter(is_active = True, ).order_by('username'), )

    class Meta:
        model = Blog
        fields = '__all__'
