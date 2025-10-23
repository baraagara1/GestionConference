from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Conference


# Create your views here.
def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(CreateView):
    model=Conference
    fields="__all__"
    template_name="conferences/form.html"
    success_url = reverse_lazy("liste_conferences")
class UpdateConferenceView(UpdateView):
    model = Conference
    fields = ["name", "theme", "description", "location", "start_date", "end_date"]
    template_name = "conferences/form.html"
    success_url = reverse_lazy("liste_conferences")
class DeleteConferenceView(DeleteView):
    model = Conference
    template_name = "conferences/confirm_delete.html"
    success_url = reverse_lazy("liste_conferences")