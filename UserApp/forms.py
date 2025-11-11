# UserApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    affiliation = forms.CharField(required=False)
    nationality = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username", "email",
            "first_name", "last_name",
            "affiliation", "nationality",
            "password1", "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        # si ton modèle custom a bien ces champs :
        if hasattr(user, "affiliation"):
            user.affiliation = self.cleaned_data.get("affiliation", "")
        if hasattr(user, "nationality"):
            user.nationality = self.cleaned_data.get("nationality", "")
        if commit:
            user.save()
        return user
