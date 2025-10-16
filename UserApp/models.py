from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import  RegexValidator
from random import choices
from string import ascii_uppercase, digits

# Nom/Prénom: lettres, espaces, tirets
name_validator = RegexValidator(
    r'^[A-Za-zÀ-ÿ\- ]+$',
    "Ce champ ne doit contenir que des lettres, espaces ou tirets."
)

def generate_user_id():
    # USER + 4 caractères = longueur exactement 8
    return "USER" + "".join(choices(ascii_uppercase + digits, k=4))

# Create your models here.
def verify_email(email):
    domaines = ["esprit.tn", "seasame.com", "tek.tn", "central.net"]
    if "@" not in email:
        raise ValidationError("Email invalide.")
    email_domaine = email.split("@")[1].lower()
    if email_domaine not in domaines:
        raise ValidationError("l'email est invalide et doit appartenir à un domaine universitaire privé")

class User(AbstractUser):
    user_id=models.CharField(max_length=8, primary_key=True , unique=True, editable=False)
    first_name = models.CharField(max_length=255, validators=[name_validator])
    last_name = models.CharField(max_length=255, validators=[name_validator])

    affiliation=models.CharField(max_length=255)
    ROLE = [
    ("participant", "participant"),
    ("committee", "organizing commitee member"),
]
    role = models.CharField(max_length=255, choices=ROLE, default="participant")

    nationality=models.CharField(max_length=50)
    email=models.EmailField(unique=True,
                            validators=[verify_email])
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
             
    def save(self, *args, **kwargs):
        if not self.user_id:
            newid=generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
            self.user_id=newid

        super().save(*args, **kwargs)

