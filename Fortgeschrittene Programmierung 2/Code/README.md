# Game_Anna_Mai
Spiel für Programmieren

**FREE MAI !!**
Ein Spiel bei dem es Dein Ziel ist, die bösen Mai-Klone und Dämonenfledermäuse zu besiegen, binnen der Zeit genug Punkte zu sammeln und so Mai zu retten.

**Spielbeschreibung**
In diesem Spiel steuerst du einen Charakter (Anna), der sich durch eine Karte bewegt und Gegner bekämpft. 
Du kannst schießen, Gegnern ausweichen und durch strategisches Spielen deine Punktzahl erhöhen. 
Schaffst du es, Mai zu retten, bevor die Zeit abläuft?

**Funktionen**

***Bewegungssystem:***
Der Spieler bewegt sich mit den Tasten W, A, S, D oder den Pfeiltasten.
Kollisionen verhindern, dass der Spieler durch z.B. Statuen oder Bäume geht.

***Waffen und Schießen:***
Eine Waffe folgt der Mausposition und schießt, wenn du mit der linken Maustaste klickst.

***Gegner-Logik:***
Gegner verfolgen den Spieler und versuchen, ihn zu fangen.
Sie können durch Schüsse eliminiert werden.

***Sieg- und Niederlagenbedingungen:***
Gewinn: Überlebe den Timer und erreiche 127 Punkte oder mehr.
Verlust: Verliere, wenn die Gegner dich treffen oder der Timer abläuft, während Du unter 127 Punkte hast.

***Kamerasteuerung:***
Die Kamera folgt dem Spieler und bleibt innerhalb der Kartengrenzen.

***Punktesystem:***
Erhöhe deine Punktzahl, indem du Gegner eliminierst.


**Steuerung**

***Bewegung:*** WASD und mit Cursortasten
***Schießen:*** Linksklick auf der Maus oder Trackpad
***Spiel neustarten:*** R
***Spiel beenden:*** Q

**Spielmechanik**

***Timer:***
Das Spiel startet mit einem Timer von 30 Sekunden.
Du kannst _Uhren_ auf der Map sammeln und dabei deine Spielzeit bis zu 40 Sekunden erhöhen, um mehr Zeit zu haben die notwendigen Punkte für Mai's Befreiung zu sammeln.
Wie oben schon erwähnt überlebst Du den Timer und hast die MIN Punktzahl erreicht: U WON!, anderenfalls: U FLOPPED!

***Gegner:***
Gegner spawnen an zufälligen Positionen auf der Karte und verfolgen den Spieler.
Sie sterben, wenn sie von einer Kugel getroffen werden.

***Waffe:***
Die Waffe rotiert mit der Mausbewegung.
Kugeln werden in die Richtung der Mausposition geschossen.

**Dateien**
1. main.py
2. player.py
3. sprites.py
4. groups.py
5. settings.py

**Voraussetzungen**
+ Python
+ pygame
+ pytmx für die map aus tiled
+ Tiled-> falls Dich irgendwas an der Map stören sollte, kannst du so dir die Map nach Deinem ermessen anpassen

**Uns bekannte Probleme**
- In manchen Winkeln fehlerhaft erscheinende Waffenrotation
- An Bäumen Hängenbleibende Gegner aus Platzgründen

**CREDITS**
- Spielentwicklung: 

Mai Phuong Hoang
Matrikelnummer: 941249
mai.p.hoang@student.fh-kiel.de

Anna Taghavi Raof
Matrikelnummer: 943502
anna.raof@student.fh-kiel.de


- Unterstützung: ChatGPT für Optimierung, Fine-Tuning und Bugfixes.
- Verwendete Assets
Background: selbsterstellt mit Props/Tiles von https://cainos.itch.io/pixel-art-top-down-basic

Waffe: https://sungraphica.itch.io/gun-collection-game-asset-free-version
Patrone: https://dinopixel.com/bullet-pixel-art-42595
Uhr: https://img.itch.zone/aW1nLzE3NTg5OTk2LnBuZw==/315x250%23c/a61YaG.png

Charaktere:
Anna und Mai Charaktere: erstellt mit My Little Star
Dämonenfledermaus: https://xzany.itch.io/flying-demon-2d-pixel-art

Animationen der Anna und Mai Charaktere erstellt mit: https://www.pixilart.com

Audio:
https://leohpaz.itch.io/minifantasy-forgotten-plains-sfx-pack

https://leohpaz.itch.io/rpg-essentials-sfx-free

https://ne-mene.itch.io/general-sound-pack