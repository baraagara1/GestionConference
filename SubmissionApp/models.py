from django.db import models
from ConferenceApp.models import Conference
from UserApp.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid
def generate_submission_id():
    return "SUB-"+uuid.uuid4().hex[:8].upper()
def validate_keywords(value):
    keywords =[k.strip() for k in value.split(',') if k.strip()]
    if len(keywords)>10:
        raise ValidationError("Vous ne pouvez pas entrer plus de 10 mots-clés.")
# Create your models here.
class Submissions(models.Model):
    submission_id=models.CharField(max_length=50,primary_key=True,unique=True,editable=False)
    title=models.CharField(max_length=50)
    abstract=models.CharField(max_length=50)
    keywords=models.CharField(max_length=50, validators=[validate_keywords])
    paper = models.FileField(
    upload_to="papers/",
    validators=[FileExtensionValidator(allowed_extensions=['pdf'], message="Le fichier doit être au format PDF.")]
    )


    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected")
    ]
    status=models.CharField(max_length=50, choices=STATUS)
    payed=models.BooleanField(default=False)

    submission_date=models.DateTimeField(auto_now_add=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    def save(self, *args, **kwargs):
        if not self.submission_id:
            new_id = generate_submission_id()
            while Submissions.objects.filter(submission_id=new_id).exists():
                new_id = generate_submission_id()
            self.submission_id = new_id
        # Appel de clean() avant la sauvegarde
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submission_id} - {self.title}"
    def clean(self):
        """Validation personnalisée pour les soumissions."""
        if self.conference.start_date <= timezone.now().date():
            raise ValidationError("Vous ne pouvez soumettre que pour des conférences à venir.")

        today = timezone.now().date()
        submissions_today = Submissions.objects.filter(
            user=self.user,
            submission_date__date=today
        ).exclude(pk=self.pk).count()  # exclude self (utile en cas de modification)

        if submissions_today >= 3:
            raise ValidationError("Vous avez déjà soumis 3 conférences aujourd'hui. Limite atteinte.")