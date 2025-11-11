from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import logout
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print("FORM ERRORS =>", form.errors)  # s'affiche dans la console runserver
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})

def logout_view(req):
    logout(req)
    return redirect("login")