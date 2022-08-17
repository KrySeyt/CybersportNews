import pytils
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext as _

from .models import New, Category, NewComment

CATEGORIES = Category.objects.exclude(name='Неизвестно')
DEFAULT_CATEGORY_NAME: str = 'Другое'


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text', 'image_url', 'is_published', 'category']
        widgets = {
            'text': forms.Textarea()
        }

    def clean_title(self):
        if pytils.translit.slugify(self.cleaned_data['title']) == '':
            raise ValidationError(message=_('Из названия невозможно сформировать slug'), code='invalid')
        return self.cleaned_data['title']


class ChangeUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, request: HttpRequest, *args, **kwargs):
        self.user: User = request.user
        initial: dict = {
            'first_name': self.user.get_short_name(),
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
        }
        super(ChangeUserDataForm, self).__init__(*args, initial=initial, **kwargs)

    def clean(self):
        pass

    def clean_username(self):
        username: str = self.cleaned_data.get('username')
        if username != self.user.get_username() and User.objects.filter(username=username).exists():
            raise ValidationError(message=_('User with this username already exists'), code='invalid')
        return username

    def clean_email(self):
        email: str = self.cleaned_data.get('email')
        if email != self.user.email and User.objects.filter(email=email).exists():
            raise ValidationError(message=_('User with this email already exists'), code='invalid')
        return email

    def save(self, commit=True):
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.username = self.cleaned_data.get('username')
        self.user.email = self.cleaned_data.get('email')

        if commit:
            self.user.save()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise ValidationError(message=_('User with this email already exists'), code='Invalid')
        return self.cleaned_data.get('email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = NewComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 150,
                'rows': 2,
            })
        }
