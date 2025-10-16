from django.db import models

# Create your models here.
# Create your models here.
class OrganizingCommittee(models.Model):
    Roles = [
        ("chair", "Chair"),
        ("co-chair", "Co-Chair"),
        ("member", "Member"),
    ]
    committee_role = models.CharField(max_length=255, choices=Roles, default="chair")
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="committees")
    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE, related_name="committees")