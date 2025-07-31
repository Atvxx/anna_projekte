# **Web Engineering Projektgruppe Q**  
FH Kiel - Sommersemester 2025  


Erstellt wurde eine Hochschul-Webseite erstellt mit einer Datenbankanbindung. Es wurde mit Django, Bootstrap, REST-API entwickelt. Hierbei basiert sich das Backend auf Django 5.2.1 und es wurde die Django REST Framework sowie einige Hilfspakete wie import_export und widget_tweaks genutzt.

## Features der Webseite:

-	Online-Bewerbungsformular mit Upload-Funktion (z.B. Zeugnis)
-	Login-/Logout-System für Admins
-	Bestätigungs-E-Mail bei Zu- oder Absage im Terminal
-	Statuscode Generierung
-	REST-API für Bewerbung und Statusabfrage
-	Admin-Export-Funktion (CSV/Excel über django-import-export)
-	Individuelle Bewerbungsstatus-Abfrage via generierten Code
-	Responsive Design mit Bootstrap CDN
-	Benutzerrollen: Superuser (Admin), User Staff (Backend) und Bewerber (Frontend)
- Google Übersetzer Button


## Installation und Setup (lokal)

### Voraussetzungen

- Python 3.10 oder neuer
- Ein Terminal (z. B. in VS Code)

### Schritte

```bash
# 1. ZIP-Datei entpacken und ins Projektverzeichnis wechseln
cd hochschulbewerbung

# 2. Virtuelle Umgebung erstellen
python -m venv venv

# 3. Virtuelle Umgebung aktivieren
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Abhängigkeiten installieren
pip install -r requirements.txt

# Falls keine requirements.txt vorhanden:
pip install django
pip install djangorestframework
pip install django-import-export
pip install django-widget-tweaks

# requirements.txt erstellen
pip freeze > requirements.txt

# 5. Datenbank vorbereiten
python manage.py makemigrations
python manage.py migrate

# 6. Superuser erstellen (für Adminbereich), wenn man einen eigenen Account erstellen möchte --> Ansonsten skippen
python manage.py createsuperuser

# 7. Datenbank Dump laden (einmalig)
python manage.py loaddata datenbank_backup.json

# 8. Projekt starten
python manage.py runserver

```

Die Seite ist nun erreichbar unter: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Mit dem eigenen Superuser/Admindaten hier einloggen: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Admindaten:

-Username: emyho

-Passwort: maimai123

---


## API-Endpunkte

- **GET** Bewerber auflisten  
  [http://127.0.0.1:8000/api/bewerbung/](http://127.0.0.1:8000/api/bewerbung/)

- **POST** Bewerber anlegen (unten auf „POST“ klicken)  
  [http://127.0.0.1:8000/api/bewerbung/](http://127.0.0.1:8000/api/bewerbung/)

### Filterbeispiele

```text
# Auflistung nur Bewerber mit dem Studiengang mit der ID (z.B. 2)
/api/bewerbung/?studiengang=2

# Auflistung nur abgelehnte Bewerber
/api/bewerbung/?status=abgelehnt

# Auflistung nur Bewerber mit dem Studiengang ID 2 und genehmigt
/api/bewerbung/?studiengang=2&status=genehmigt
```

---

## Besondere Features im Detail

### 1. Bewerber:innen können ihre Unterlagen über ein Online-Bewerbungsformular einreichen. Nach dem Absenden erhalten sie einen automatisch generierten persönlichen Code, mit dem sie den Status ihrer Bewerbung abfragen können.
Für die Statusabfrage müssen die Bewerber:innen ihren Code eingeben. Anschließend wird angezeigt, ob die Bewerbung angenommen, abgelehnt oder noch in Bearbeitung ist.
Falls der persönliche Code verloren geht, kann dieser erneut angefordert werden. Dazu geben die Bewerber:innen ihre E-Mail-Adresse und ihr Geburtsdatum an, der Code wird dann an die angegebene E-Mail-Adresse gesendet.
Wenn sich der Status der Bewerbung ändert, indem ein Admin die Bewerbung bearbeitet, bekommen Bewerber:innen eine Benachrichtigung.
Falls man Fragen an die IUC hat, kann man ein Kontaktanfrage-Formular ausfüllen und wir (die Admins) erhalten die Anfrage im Admin-Bereich.
Da sich das Projekt aktuell im Entwicklungsmodus (Lokal) befindet, werden E-Mails nicht tatsächlich versendet, sondern erscheinen in der Konsole bzw. im Terminal.

### 2. Zeugnis-Upload mit Dateispeicherung

-	Das Bewerbungsformular erlaubt den Upload von PDF-Dateien (z. B. Zeugnisse).
-	Die Dateien werden im Ordner media/ gespeichert und sind über das Admin-Panel abrufbar.
-	Eine Validierung prüft, ob eine Datei hochgeladen wurde und ob es sich um ein zulässiges Format handelt.
  
###  3. Studiengangs Auswahl dynamisch
-	Die Auswahl von Studiengängen im Bewerbungsformular basiert auf Modellen in der Datenbank.
-	So können Admins jederzeit neue Studiengänge hinzufügen, ohne den Code anpassen zu müssen.
-	Dies verbessert die Zugänglichkeit für internationale Bewerber:innen.
---

## Bildquellen

Die verwendeten Bilder stammen von [Freepik](https://www.freepik.com) und [Pixabay](https://www.pixabay.com). Die Nutzung erfolgt gemäß den jeweiligen Lizenzbedingungen.


## Sonstige Quellen

Folgende Inhalte wurden mithilfe von KI (ChatGPT/DALL·E) erstellt oder generiert:

- Datenschutzerklärung (Text)
- Top-Uni-Icon (Grafik)
- Uni-Logo (Grafik)
- DBM-Flyer (Grafik & Text)
- BWL-Studienverlaufsplan (Grafik & Text)
- Lageplan (Grafik)
- Texte auf der Website


## Kontakt

Diese Website wurde im Rahmen eines Hochschulprojekts erstellt von:

**Teammitglieder:**  
- Anna Taghavi Raof | anna.raof@student.fh-kiel.de
- Celia Meißner | celia.meissner@student.fh-kiel.de
- Chris Lopes | Salgueiro christian.salgueiro@student.fh-kiel.de
- Mai Phuong Hoang | mai.p.hoang@student.fh-kiel.de
