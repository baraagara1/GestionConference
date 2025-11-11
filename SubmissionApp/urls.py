from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    # Liste complète des soumissions
    path('liste/', ListSubmissions.as_view(), name='liste_submissions'),

    # Liste filtrée par conférence
    path('conference/<int:conference_id>/', ListSubmissions.as_view(), name='liste_submissions_conference'),
    # Détail d'une soumission
    path('submissions/detail/<str:pk>/', SubmissionDetail.as_view(), name='submission_detail'), # Ajouter une soumission
    path('add/', SubmissionCreate.as_view(), name='add_submission'),

    # Modifier une soumission
    path('update/<str:pk>/', SubmissionUpdate.as_view(), name='update_submission'),
]