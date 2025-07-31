from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid # UUID für Bewerbungs-ID

# Dropdown für den Höchstabschluss der Bewerber
class Abschluss(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Abschlüsse"


# Auflistung Studiengänge
class Studiengang(models.Model):
    ONLINE = 'Online'
    PRSENZ = 'Präsenz'
    STUDIENFORM_CHOICES = [
        (ONLINE, 'Online'),
        (PRSENZ, 'Präsenz'),
    ]
    
    name = models.CharField(max_length=100)
    abschluss = models.CharField(max_length=50)  # Bachelor oder Master
    form = models.CharField(
        max_length=10,
        choices=STUDIENFORM_CHOICES,
        default=ONLINE,
    )

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "Studiengänge"     # Damit auf Django nicht Studiengangs steht
        
# Bewerbung, speichert die Bewerberdaten und den Status der Bewerbung      
class Bewerbung(models.Model):
    studiengang = models.ForeignKey('Studiengang', on_delete=models.CASCADE)
    vorname = models.CharField(max_length=100, blank=False)
    nachname = models.CharField(max_length=100, blank=False)
    geburtsdatum = models.DateField(default=timezone.now)
    telefon = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField()
    abschluss = models.ForeignKey(Abschluss, on_delete=models.SET_NULL, null=True)
    sprachen = models.CharField(max_length=100)
    kommentar = models.TextField(blank=True, null=True)
    zeugnis = models.FileField(upload_to='zeugnisse/', blank=False, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('in_bearbeitung', 'In Bearbeitung'), ('genehmigt', 'Genehmigt'), ('abgelehnt', 'Abgelehnt')],
        default='in_bearbeitung'
    )
    
    status_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    # Einwilligung DSGVO

    einwilligung = models.BooleanField(
        default=False,
        help_text="Ich bin mit der Verarbeitung meiner Daten gemäß Datenschutzerklärung einverstanden."
    )

    def save(self, *args, **kwargs):
        if not self.status_code:
            self.status_code = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vorname} {self.nachname}'
    
    class Meta:
        verbose_name_plural = "Bewerbungen"  # Damit auf Django nicht Bewerbungs steht
        
 
# Zugangsvoraussetzungen       
class Zugangsvoraussetzung(models.Model):
    studiengang = models.ForeignKey('Studiengang', on_delete=models.CASCADE)
    abschluss = models.CharField(max_length=100)  
    sprachen = models.CharField(max_length=100)  

    def __str__(self):
        return f'{self.studiengang.name} - {self.abschluss}'

    class Meta:
        verbose_name_plural = "Zugangsvoraussetzungen"  # Damit auf Django nicht Zugangsvoraussetzungs steht
 
 
# Kontaktformular

class Kontaktanfrage(models.Model):
    vorname = models.CharField(max_length=100, default="Unbekannt")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    nachricht = models.TextField()
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Kontaktanfragen"  

 

class BewerbungsLog(models.Model):
    bewerbung = models.ForeignKey(Bewerbung, on_delete=models.CASCADE)
    status_alt = models.CharField(max_length=20)
    status_neu = models.CharField(max_length=20)
    geaendert_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bewerbung} - {self.status_alt} → {self.status_neu}"
