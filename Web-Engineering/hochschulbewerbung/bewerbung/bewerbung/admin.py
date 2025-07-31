from django.contrib import admin
from django import forms
from .models import Studiengang, Bewerbung, Zugangsvoraussetzung, Kontaktanfrage, BewerbungsLog, Abschluss
from import_export.admin import ExportMixin #Excel
from django.utils.html import format_html


admin.site.register(Zugangsvoraussetzung)
admin.site.register(Kontaktanfrage)
admin.site.register(Abschluss)

@admin.register(Studiengang)
class StudiengangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abschluss', 'form')

class BewerbungsLogInline(admin.TabularInline):
    model = BewerbungsLog
    extra = 0
    readonly_fields = ('status_alt', 'status_neu', 'geaendert_am')
    can_delete = False


class BewerbungAdminForm(forms.ModelForm):
    def clean_zeugnis(self):
        datei = self.cleaned_data.get("zeugnis")
        if datei and not datei.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Nur PDF-Dateien sind erlaubt.")
        return datei

    class Meta:
        model = Bewerbung
        fields = "__all__"


@admin.register(Bewerbung)
class BewerbungAdmin(ExportMixin, admin.ModelAdmin):
    form = BewerbungAdminForm
    list_display = ('id', 'vorname', 'nachname', 'geburtsdatum', 'email', 'studiengang', 'status', 'zeugnis_link')
    list_filter = ('status', 'studiengang')
    search_fields = ('vorname', 'nachname', 'email')
    list_editable = ('status',)
    inlines = [BewerbungsLogInline]
    
    def zeugnis_link(self, obj):
        if obj.zeugnis:
            return format_html('<a href="{}" target="_blank">Ansehen</a>', obj.zeugnis.url)
        return "Kein Zeugnis"
    zeugnis_link.short_description = "Zeugnis"



