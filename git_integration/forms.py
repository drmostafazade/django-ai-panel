from django import forms
from .models import GitHubToken

class GitHubTokenForm(forms.Form):
    token = forms.CharField(
        label='GitHub Personal Access Token',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'ghp_xxxxxxxxxxxx'
        }),
        help_text='<a href="https://github.com/settings/tokens/new" target="_blank">دریافت توکن جدید</a>'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self):
        token_value = self.cleaned_data['token']
        token, created = GitHubToken.objects.update_or_create(
            user=self.user,
            defaults={'token': token_value}
        )
        return token
