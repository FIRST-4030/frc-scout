from django import forms


class LoginForm(forms.Form):
    team_number = forms.DecimalField(label="", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "Team Number"})
    )
    scout_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Scout Name"})
    )
    team_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Team Password"})
    )
    location = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Location"})
    )
