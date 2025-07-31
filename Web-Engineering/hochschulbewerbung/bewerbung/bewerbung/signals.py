from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Bewerbung, BewerbungsLog
from django.core.mail import send_mail

# Generiert mit ChatGPT
# Qualität: Sehr gut -funktioniert einwandfrei und erfüllt die Anforderungen
# Lesbarkeit: Hoch - Klar strukturierter Code

@receiver(pre_save, sender=Bewerbung)
def log_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            alt = Bewerbung.objects.get(pk=instance.pk)
            if alt.status != instance.status:
                # Statusänderung loggen
                BewerbungsLog.objects.create(
                    bewerbung=instance,
                    status_alt=alt.status,
                    status_neu=instance.status
                )
                
                # Zusage E-Mail
                if instance.status == 'genehmigt':
                    send_mail(
                        subject='Zusage Studienplatz',
                        message=(
                            f"Sehr geehrte*r {instance.vorname} {instance.nachname},\n\n"
                            "Herzlichen Glückwunsch! Sie haben einen Studienplatz erhalten.\n"
                            f"Studiengang: {instance.studiengang.name}\n\n"
                            "Mit freundlichen Grüßen\nIhre International University CALM "
                        ),
                        from_email=None,
                        recipient_list=[instance.email],
                        fail_silently=False,
                    )
                
                # Absage E-Mail
                elif instance.status == 'abgelehnt':
                    send_mail(
                        subject='Absage Studienplatz',
                        message=(
                            f"Sehr geehrte*r {instance.vorname} {instance.nachname},\n\n"
                            "leider müssen wir Ihnen mitteilen, dass wir Ihnen aktuell keinen Studienplatz anbieten können.\n\n"
                            "Wir wünschen Ihnen dennoch viel Erfolg auf Ihrem weiteren Weg.\n\n"
                            "Mit freundlichen Grüßen\nIhre International University CALM "
                        ),
                        from_email=None,
                        recipient_list=[instance.email],
                        fail_silently=False,
                    )

        except Bewerbung.DoesNotExist:
            pass
