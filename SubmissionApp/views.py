# SubmissionApp/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submissions
from .forms import SubmissionForm

class ListSubmissions(LoginRequiredMixin, ListView):
    model = Submissions
    context_object_name = "submissions"
    template_name = "submissions/liste.html"

    def get_queryset(self):
        qs = Submissions.objects.filter(user=self.request.user).select_related("conference")
        conference_id = self.kwargs.get("conference_id")
        if conference_id:
            qs = qs.filter(conference_id=conference_id)
        return qs

class SubmissionDetail(LoginRequiredMixin, DetailView):
    model = Submissions
    context_object_name = "submission"
    template_name = "submissions/detail.html"

class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = Submissions
    template_name = "submissions/form.html"
    form_class = SubmissionForm
    success_url = reverse_lazy("liste_submissions")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user           # <- injecte user dans le form
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user       # <- lie l’instance au user
        # status/payed automatiques via modèle (default/False)
        return super().form_valid(form)

class SubmissionUpdate(LoginRequiredMixin, UpdateView):
    model = Submissions
    template_name = "submissions/form.html"
    form_class = SubmissionForm
    success_url = reverse_lazy("liste_submissions")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        # Sécurité : l’utilisateur modifie uniquement ses soumissions
        return Submissions.objects.filter(user=self.request.user)
