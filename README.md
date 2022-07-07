# Nachkaufomat 3000

Dinge im Space nachkaufen.


## Installation

```bash
git clone https://github.com/Eigenbaukombinat/Nachkaufomat3000.git
cd Nachkaufomat3000
python3 -m venv .
bin/pip install -r requirements.txt
FLASK_APP = main.py bin/flask run
```

## Usage

Im Browser http://localhost:5000/add_qr öffnen, Namen vergeben, QR Code ausdrucken

mqtt-Nachricht "space/nachkaufen" mit dem Titel der nachzukaufenden Sache wird erzeugt, wenn der QR-Code gescanned und mit einem Klick bestätigt wird.


## Todo

* /list_codes bauen (anzeige der bestehenden Dinge, mit Link zu den QR-Codes)
* Persistieren der Dinge und Hashes (Flatfile, yaml, whatever)
* vermeidung von doppelten meldungen
    * zweite aktion vorsehen, um bestehende meldung zurückzusetzen (ggf. inkl meldung "pizza wurde aufgefüllt") 
* konifgurierbar machen (base url, mqtt server, topic)
* ansible 
* styling


