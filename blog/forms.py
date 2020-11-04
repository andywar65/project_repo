from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import UserUpload, Article
from users.models import User

class UserUploadForm(ModelForm):
    body = forms.CharField(label = _('Text'),
        widget=forms.Textarea(attrs={'placeholder': _("Leave here your message")}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)

class ArticleForm(ModelForm):
    author = forms.ModelChoiceField(label=_("Author"), required = False,
        queryset = User.objects.filter(is_active = True, ).order_by('username'), )

    class Meta:
        model = Article
        fields = '__all__'
