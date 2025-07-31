from django import forms
from .models import Bewerbung, Abschluss
from django.utils.safestring import mark_safe


#Bewerbungsformular

class BewerbungForm(forms.ModelForm):
    einwilligung = forms.BooleanField(
        required=True,
        label=mark_safe('Ich stimme der <a href="/static/pdf/datenschutzerklärung.pdf" target="_blank">Datenschutzerklärung</a> zu.')
    )

    class Meta:
        model = Bewerbung
        fields = [
            'vorname', 'nachname', 'email', 'geburtsdatum',
            'studiengang', 'abschluss', 'sprachen', 'adresse',
            'telefon', 'zeugnis', 'kommentar', 'einwilligung'
        ]
        widgets = {
            'vorname': forms.TextInput(attrs={'class': 'form-control'}),
            'nachname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'geburtsdatum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'studiengang': forms.Select(attrs={'class': 'form-control'}),
            'abschluss': forms.Select(attrs={'class': 'form-control'}),
            'sprachen': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'zeugnis': forms.FileInput(attrs={'class': 'form-control'}),
            'kommentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean_zeugnis(self):
        datei = self.cleaned_data.get("zeugnis")
        if datei and not datei.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Nur PDF-Dateien sind erlaubt.")
        return datei

