from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            pseudo = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if len(password) < 8:
                messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
            else:
                user = authenticate(request, username=pseudo, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, 'Vous êtes connecté')
                    return redirect('acceuil')
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/Login.html', {"form": form})


def deconnexion(request):
    logout(request)
    return redirect('login')
