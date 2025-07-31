from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BewerbungForm, UserProfileForm, CustomUserCreationForm  # CustomUserCreationForm ergänzen
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bewerbung, UserProfile  # UserProfile hinzugefügt
from django.core.mail import send_mail
# API Ansicht
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BewerbungSerializer
from rest_framework.permissions import IsAdminUser
# Kontaktansicht
from .serializers import KontaktanfrageSerializer
from .models import Kontaktanfrage
# status code erneut versenden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def register(request):
    # CustomUserCreationForm verwenden und UserProfile anlegen
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile direkt anlegen mit den zusätzlichen Feldern
            UserProfile.objects.create(
                user=user,
                vorname=form.cleaned_data.get('first_name'),
                name=form.cleaned_data.get('last_name'),
                adresse=form.cleaned_data.get('adresse'),
                plz=form.cleaned_data.get('plz')
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

#