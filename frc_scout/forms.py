from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username"})
    )
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Password"})
    )
    location = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Location"})
    )
