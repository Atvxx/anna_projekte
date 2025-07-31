##Vorbereitung
import csv

liste = []
paketliste = []
ladung = []
paketnummern_ladung = []

gesamtpreis = 0
aktuelle_ladung = 0

zahlenabfrage = True
dateiabfrage = True


## Eingabe der Anzahl der LKWs
while zahlenabfrage:
    try:
        anzahl_lkws = input("Bitte geben Sie die Anzahl der zu beladenden Fahrzeuge ein: ")
        if anzahl_lkws.lower() == "quit":
            print("Das Programm wird geschlossen.")
            exit()
        anzahl_lkws = int(anzahl_lkws)
        if anzahl_lkws > 0:
            zahlenabfrage = False
        else:
            print("Fehler! Bitte geben Sie einen positiven Zahlenwert ein.")
    except ValueError:
        print("Fehler! Ihre Eingabe war kein gültiger Zahlenwert.")


## Eingabe des maximalen Volumens pro LKW
max_volumen_lkws = []
for lkw_nummer in range(1, anzahl_lkws + 1):
    zahlenabfrage = True
    while zahlenabfrage:
        try:
            max_volumen = input(f"Bitte geben Sie das (fixe) maximale Volumen des Transporters {lkw_nummer} in Kubikmetern ein: ")
            if max_volumen.lower() == "quit":
                print("Das Programm wird geschlossen.")
                exit()
            max_volumen = float(max_volumen.replace(',', '.'))
            if max_volumen > 0:
                max_volumen_lkws.append(max_volumen)
                zahlenabfrage = False
            else:
                print("Fehler! Bitte geben Sie einen positiven Zahlenwert ein.")
        except ValueError:
            print("Fehler! Ihre Eingabe war kein gültiger Zahlenwert.")
            
        
## Einlesen der CSV-Datei und Integration in eine Liste
while dateiabfrage:
    try:
        dateipfad = input("Bitte geben Sie den Dateipfad ein: ")
        if dateipfad.lower() == "quit":
            print("Das Programm wird geschlossen.")
            exit()
        elif not dateipfad.endswith('.csv'):
            print("Fehler! Die ausgewählte Datei ist nicht im CSV-Format. Bitte überprüfen Sie das Dateiformat der ausgewählten Datei.")
            continue
        with open(dateipfad, 'rb') as f:
            content = f.read()
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]
            if content.strip() == b'':
                print("Fehler! Die ausgewählte Datei enthält keine Daten.")
                exit()
            else:
                content = content.decode('utf-8')
                reader = csv.reader(content.splitlines(), delimiter=';')
                rows = list(reader)
                if not rows:
                    print("Fehler! Die ausgewählte Datei enthält keine Daten.")
                    exit()
                elif len(rows) == 1 and all(not any(field.strip() for field in row) for row in rows):
                    print("Fehler! Die ausgewählte Datei enthält keine Daten.")
                    exit()
                elif len(rows) > 1 and all(not any(field.strip() for field in row) for row in rows[1:]):
                    print("Fehler! Die ausgewählte Datei enthält keine Daten.")
                    exit()
                for paket in rows:
                    liste.append(paket)
        dateiabfrage = False
    except FileNotFoundError:
        print("Fehler! Die ausgewählte Datei konnte nicht gefunden werden. Bitte überprüfen Sie den Dateipfad.")
        continue


## Anpassen der Liste (Formatierung) 
fehlende_daten_count = 0 
ungültige_pakete = []
for i, element in enumerate(liste):
    neue_liste = element[:3]
    while len(neue_liste) < 3:
        neue_liste.append('0')
    if len(neue_liste) < 3 or any(attr == '' or attr.lower() == 'null' for attr in neue_liste):
        fehlende_daten_count += 1
        ungültige_pakete.append(element[0])
        continue
    paketliste.append(neue_liste)

if fehlende_daten_count > 0:
    print(f"Achtung! Mindestens ein Datensatz war unvollständig und wurde entfernt. Überprüfen Sie die folgenden Datensätze: Pakete {', '.join(ungültige_pakete)}.")

paketliste = paketliste[1:]


## Anpassen der Liste (Sortierung) -> Durchschnittswert (Preis / Volumen) bilden und nach höchsten Durchschnittswert sortieren
verarbeitete_liste = []
for paket in paketliste:
    try:
        paketnummer = paket[0]
        volumen = float(paket[1].replace(',', '.'))
        preis = float(paket[2].replace('€', '').replace(',', '.'))
        if volumen <= 0 or preis <= 0:
            continue
        preis_pro_volumen = preis / volumen
        verarbeitete_liste.append([paketnummer, volumen, preis, preis_pro_volumen])
    except ValueError:
        continue

## Preis-pro-Volumen wird in absteigender Reihenfolge sortiert
verarbeitete_liste.sort(key=lambda x: x[3], reverse=True)


## Beladung der LKWs
lkw_ladung = [[] for _ in range(anzahl_lkws)]
lkw_gesamtpreis = [0 for _ in range(anzahl_lkws)]
lkw_aktuelle_ladung = [0 for _ in range(anzahl_lkws)]

for paket in verarbeitete_liste:
    for lkw_nummer in range(anzahl_lkws):
        max_volumen = max_volumen_lkws[lkw_nummer]
        if lkw_aktuelle_ladung[lkw_nummer] + paket[1] <= max_volumen:
            lkw_ladung[lkw_nummer].append(paket[0])
            lkw_gesamtpreis[lkw_nummer] += paket[2]
            lkw_aktuelle_ladung[lkw_nummer] += paket[1]
            break


## Ausgabe
for lkw_nummer in range(anzahl_lkws):
    max_ladevolumen = max_volumen_lkws[lkw_nummer]
    aktuelle_ladung = round(lkw_aktuelle_ladung[lkw_nummer],2)
    gesamtpreis = round(lkw_gesamtpreis[lkw_nummer],2)
    paketnummern_ladung = lkw_ladung[lkw_nummer]

    if aktuelle_ladung == 0:
        print(f"Achtung! Der LKW {lkw_nummer + 1} mit einem maximalen Ladevolumen von {max_ladevolumen} Kubikmetern ist leer.")
    elif aktuelle_ladung / max_ladevolumen < 0.9:
        print(f"Achtung! Der LKW {lkw_nummer + 1} mit einem maximalen Ladevolumen von {max_ladevolumen} Kubikmetern ist nicht voll beladen. Es sind nur {aktuelle_ladung} Kubikmeter mit folgenden Paketen beladen: {sorted(paketnummern_ladung, key=int)}. Diese Pakete ergeben einen Gesamtpreis von {gesamtpreis}€.")
    else:
        print(f"Für eine optimale Beladung des LKW {lkw_nummer + 1} mit {max_ladevolumen} Kubikmetern Ladevolumen müssen folgende Pakete beladen werden: {sorted(paketnummern_ladung, key=int)}. Diese Pakete ergeben ein Gesamtvolumen von {aktuelle_ladung} Kubikmetern und einen Gesamtpreis von {gesamtpreis}€.")