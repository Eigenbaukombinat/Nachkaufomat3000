from flask import Flask, abort, send_file, request
import hashlib
import paho.mqtt.client as mqtt
import qrcode
import io

app = Flask(__name__)

MQTT = mqtt.Client("Nachkaufomat3000")
MQTT.connect("localhost")
BASE_URL = "http://localhost:5000"

DINGE = set(['Chips', 'Pizza'])
HASHES = {}


def send_mqtt(title):
    MQTT.publish("space/nachkaufen", title)


for ding in DINGE:
    hash = hashlib.md5(ding.encode('utf8')).hexdigest()
    print(f"{ding}: {hash}")
    HASHES[hash] = ding


@app.route("/<hash>")
def nachkauf_entry(hash):
    if hash in HASHES:
        return f'<p><a href="/nachkauf/{hash}">Ja, {HASHES[hash]} wirklich nachkaufen.</p>'
    else:
        abort(404)


@app.route("/nachkauf/<hash>")
def nachkauf_send(hash):
    if hash in HASHES:
        send_mqtt(HASHES[hash])
        return f'<h1>DANKE! <3</h>'
    else:
        abort(404)


@app.route("/new_qr")
def nachkauf_new_qr():
    return f'<form action="/add_qr"><input type="text" name="ding" /><input type="submit"></form>'


@app.route("/add_qr")
def add_qr():
    ding = request.args.get('ding')
    hash = hashlib.md5(ding.encode('utf-8')).hexdigest()
    DINGE.add(ding)
    HASHES[hash] = ding
    return f'<h1>{ding}</h1></<img src="/qr_code/{hash}"/>'


@app.route("/list_codes")
def list_codes():
    # returnlist of codes with links to current codes and link to add-form
    pass

def gen_qr_image(url):
    # define qr code parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=30,
        border=1,
    )
    # fill it with data
    qr.add_data(url)
    qr.make(fit=True)
    # generate image from qr code data
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, "png")
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route("/qr_code/<hash>")
def nachkauf_add_qr(hash):
    url = f"{BASE_URL}/{hash}"
    return gen_qr_image(url)


