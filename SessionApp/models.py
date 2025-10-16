from django.db import models
from ConferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

room_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s]+$',
    message="Le titre de la salle ne doit contenir que des lettres, des chiffres et des espaces."
)
title_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="le nom de la conférence ne doit contenir que des lettres et des espaces"
)
# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50, validators=[title_validator])
    topic=models.CharField(max_length=50)
    session_day=models.DateField()
    start_time=models.DateTimeField(auto_now=True)
    end_time=models.DateTimeField(auto_now_add=True)
    room=models.CharField(max_length=255, validators=[room_validator])
    #conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE ,related_name="sessions")
    conference=models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="sessions")
       # conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE, related_name="sessions")
    #Autre Syntaxe conference = models.ForeignKey(Conference)
    def clean(self):
        # Vérifie si la conférence est définie avant de valider
        if self.conference:
            start = self.conference.start_date
            end = self.conference.end_date

            # Si la session ne respecte pas les bornes
            if not (start <= self.session_day <= end):
                raise ValidationError(
                    f"La date de la session ({self.session_day}) doit être comprise entre "
                    f"les dates de la conférence ({start} - {end})."
                )
        # Vérifie si l'heure de début est avant l'heure de fin
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être avant l'heure de fin.")
        

