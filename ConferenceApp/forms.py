from django import forms
from .models import Conference
class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'location','description','start_date', 'end_date']
        labels = {
            'name': 'Nom de la conférence',
            'theme': 'Thèmatique de la conférence',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Entrez le nom de la conférence'
                    }
                ),
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date'
                    }
                ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date'
                    }
                ),
        }