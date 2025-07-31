from django.shortcuts import render, redirect, get_object_or_404
from .forms import BewerbungForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bewerbung
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
from django.shortcuts import render, redirect
from .models import Kontaktanfrage


#  Mit ChatGPT generiert:
#  API-Ansicht für Bewerbungen hatte bei mir anfangs Probleme, da ich nicht wusste, wie ich die GET- und POST-Methoden kombinieren sollte.
#  Funktionalität: Die API ermöglicht es, Bewerbungen zu erstellen und abzurufen. GET-Anfragen listen alle Bewerbungen auf, POST-Anfragen speichern neue Bewerbungen.
#  Treffsicherheit: Hoch - Die API funktioniert wie erwartet und erfüllt die Anforderungen.

def bewerbung_view(request):
    if request.method == 'POST':
        form = BewerbungForm(request.POST, request.FILES)
        if form.is_valid():
            bewerbung = form.save()

            # Bestätigungsmail
            send_mail(
                subject="Ihre Bewerbung ist eingegangen",
                message=(
                    f"Sehr geehrte*r {bewerbung.vorname} {bewerbung.nachname},\n\n"
                    "vielen Dank für Ihre Bewerbung.\n"
                    "Wir prüfen Ihre Unterlagen und melden uns zeitnah.\n\n"
                    "Mit freundlichen Grüßen\nIhre International University CALM"
                ),
                from_email=None,
                recipient_list=[bewerbung.email],
                fail_silently=False
            )
            return redirect('danke', code=bewerbung.status_code)
    else:
        form = BewerbungForm()  # wichtig

    return render(request, 'bewerbung.html', {'form': form})



def benutzer_login(request):
    if request.method == "POST":
        benutzername = request.POST["username"]
        passwort = request.POST["password"]
        benutzer = authenticate(request, username=benutzername, password=passwort)
        if benutzer is not None:
            login(request, benutzer)
            if benutzer.is_staff:
                return redirect('/admin/')  # Admin weiter ins Adminbereich
            else:
                return redirect('/bewerbung/')  # Normale Nutzer ins Formular
        else:
            messages.error(request, "Login fehlgeschlagen")
    return render(request, "login.html")



def benutzer_logout(request):
    logout(request)
    return redirect("/login/")


@api_view(['GET', 'POST'])  # Musste POST für die Speicherung der Bewerbungen nutzen und GET für die Auflistung der Bewerbungen als JSON
def bewerbung_api(request):
    if request.method == 'GET':
        # Zugriff nur für Admins / Staff
        if not request.user.is_staff:
            return Response({"detail": "Zugriff verweigert."}, status=403)

        bewerbungen = Bewerbung.objects.all()

        # Filter Studiengang und Status
        studiengang_id = request.GET.get('studiengang')
        if studiengang_id:
            bewerbungen = bewerbungen.filter(studiengang=studiengang_id)

        status_filter = request.GET.get('status')
        if status_filter:
            bewerbungen = bewerbungen.filter(status=status_filter)

        serializer = BewerbungSerializer(bewerbungen, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BewerbungSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Bewerbung erfolgreich gespeichert'}, status=201)
        return Response(serializer.errors, status=400)



@api_view(['POST'])
def kontakt_api(request):
    serializer = KontaktanfrageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Kontaktanfrage gespeichert"}, status=201)
    return Response(serializer.errors, status=400)


# HTML-Ansicht:
def status_check_view(request):
    code = request.GET.get("code")
    bewerbung = Bewerbung.objects.filter(status_code=code).first()
    return render(request, "status_check.html", {"bewerbung": bewerbung, "code": code})

# API:
@api_view(['POST'])
def status_check_api(request):
    email = request.data.get("email")
    geburtsdatum = request.data.get("geburtsdatum")
    try:
        bewerbung = Bewerbung.objects.get(email=email, geburtsdatum=geburtsdatum)
        return Response({"status": bewerbung.status}, status=200)
    except Bewerbung.DoesNotExist:
        return Response({"detail": "Keine Bewerbung gefunden"}, status=404)


def kontakt(request):
    if request.method == 'POST':
        vorname = request.POST.get('vorname', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        nachricht = request.POST.get('nachricht', '')

        # Speichern in die Datenbank (erscheint im Admin)
        Kontaktanfrage.objects.create(
            vorname=vorname,
            name=name,
            email=email,
            nachricht=nachricht
        )
        return render(request, 'danke_kontakt.html')
    return render(request, 'kontakt.html')

def danke_seite(request, code):
    bewerbung = get_object_or_404(Bewerbung, status_code=code)
    return render(request, 'danke_absenden.html', {'code': code, 'bewerbung': bewerbung})

@csrf_exempt
def sende_statuscode(request):
    if request.method == "POST":
        email = request.POST.get("email")
        geburtsdatum = request.POST.get("geburtsdatum")

        try:
            bewerbung = Bewerbung.objects.get(email=email, geburtsdatum=geburtsdatum)
            send_mail(
                subject="Ihr Bewerbungsstatus-Code",
                message=(
                    f"Sehr geehrte*r {bewerbung.vorname} {bewerbung.nachname},\n\n"
                    f"Ihr individueller Bewerbungs-Code lautet: {bewerbung.status_code}\n"
                    f"Sie können ihn hier prüfen: http://127.0.0.1:8000/status/?code={bewerbung.status_code}\n\n"
                    "Mit freundlichen Grüßen\nIhre International University CALM"
                ),
                from_email=None,
                recipient_list=[bewerbung.email],
                fail_silently=False
            )
            return render(request, "statuscode_versendet.html", {"success": True})
        except Bewerbung.DoesNotExist:
            return render(request, "statuscode_versendet.html", {"error": "Keine Bewerbung gefunden."})

    return render(request, "statuscode_versendet.html")

def startseite(request):
    return render(request, 'startseite.html')

def kontakt_view(request):
    return render(request, 'kontakt.html')

def danke_kontakt(request):
    return render(request, 'danke_kontakt.html')

def bwl_view(request):
    return render(request, 'bwl.html')

def studiengaenge_view(request):
    # Deine Logik
    return render(request, 'studiengaenge.html')

def psychologie_view(request):
    return render(request, 'psychologie.html')

def winfo_view(request):
    return render(request, 'winfo.html')

def dbm_view(request):
    return render(request, 'dbm.html')

def voraussetzungen_view(request):
    return render(request, 'voraussetzungen.html')

def bewerbungsprozess_view(request):
    return render(request, 'bewerbungsprozess.html')


