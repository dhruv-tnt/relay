from flask import Blueprint, render_template, request, jsonify
import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO

# Create a blueprint object
new_bp = Blueprint('new_bp', __name__, static_folder='../static', static_url_path='/new_bp/static')

# Initialize pin variables
relay_pin = 18
DHT_PIN = 17

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# DHT sensor type
DHT_SENSOR = Adafruit_DHT.DHT22

@new_bp.route('/')
def hello():
    data = rd()
    return render_template('index.html', state=data["state"], color=data["color"], relay_pin=relay_pin, dht_pin=DHT_PIN)

@new_bp.route('/about')
def about():
    data = request.args.get("data")
    wt(data)
    return jsonify(rd())

@new_bp.route('/temp')
def temp():
    temp_data = read_temp_humidity()
    return jsonify(temp_data)

@new_bp.route('/set_pins', methods=['POST'])
def set_pins():
    global relay_pin, DHT_PIN
    relay_pin = int(request.form.get("relay_pin"))
    DHT_PIN = int(request.form.get("dht_pin"))
    
    # Reconfigure GPIO setup
    GPIO.setup(relay_pin, GPIO.OUT)
    
    return redirect(url_for('new_bp.hello'))

def wt(data):
    with open('data.json', 'w') as w:
        if data == 'on':
            GPIO.output(relay_pin, GPIO.HIGH)
            w.write('{"state":"off","color":"red"}')
        else:
            GPIO.output(relay_pin, GPIO.LOW)
            w.write('{"state":"on","color":"green"}')

def rd():
    with open('data.json', 'r') as r:
        data = json.load(r)
        return data

def read_temp_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1)
        }
    else:
        return {
            "temperature": "Error",
            "humidity": "Error"
        }
