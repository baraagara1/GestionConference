from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator

 # Titre lettres/espaces/tirets
title_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="le nom de la conférence ne doit contenir que des lettres et des espaces"
)
# Create your models here.
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255, unique=True, validators=[title_validator])
    THEME=[
        ("IA","Computer Science & ia"),
        ("SE","Science&Engineering"),
        ("SC","Social Sciences & Education"),
        ("IT","interdiscplinaryThemes")   ,
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=255)
    description = models.TextField(validators=[
        MinLengthValidator(30, "La description doit contenir au moins 30 caractères.")
    ])
    start_date=models.DateField()
    end_date=models.DateField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
       

    def clean(self):
        # 3) start_date < end_date
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError({"start_date": "La date de début doit être avant la date de fin."})

    def __str__(self):
        return self.name    

