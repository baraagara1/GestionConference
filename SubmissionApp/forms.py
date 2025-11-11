from django import forms
from .models import Submissions
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submissions
        fields = ['title', 'abstract', 'keywords', 'conference', 'paper']
        labels = { 'title': 'Titre de la soumission',
                   'abstract': 'Résumé',
                   'keywords': 'Mots-clés',
                   'paper': 'Fichier PDF',
                   'conference': 'Conférence associée',
                   
                 }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Entrez le titre de votre soumission'
                }
            ),
            'abstract': forms.Textarea(
                attrs={
                    'placeholder': 'Entrez le résumé de votre soumission',
                    'rows': 4
                }
            ),
            'keywords': forms.TextInput(
                attrs={
                    'placeholder': 'Entrez les mots-clés séparés par des virgules'
                }
            ),
            'conference': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
        