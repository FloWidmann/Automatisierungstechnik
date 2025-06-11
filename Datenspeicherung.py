import paho.mqtt.client as mqtt
import csv

currentTimeStamp = 0
timeInterval = 1 # in seconds
maxTime = 15 #15 minutes
maxTimeStamps = maxTime * 60 * timeInterval  



# MQTT-Broker und Verbindungseinstellungen
broker = "158.180.44.197"
port = 1883
topic = "iot1/teaching_factory/#"

# CSV-Datei öffnen (falls nicht existiert, wird sie erstellt) und Header schreiben
csv_file = "mqtt_data.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Topic", "Message"])  # Kopfzeile setzen

# Callback-Funktion für empfangene Nachrichten
def on_message(client, userdata, message):
    msg = message.payload.decode()
    topic = message.topic

    print("message received:")
    print(f"Topic: {topic}, Message: {msg}")
    print("\n")

    # Daten in CSV-Datei speichern
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([topic, msg])  # Daten anhängen

# MQTT-Client einrichten
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")
mqttc.on_message = on_message
mqttc.connect(broker, port)
mqttc.subscribe(topic, qos=0)

# MQTT-Schleife starten (Daten werden kontinuierlich empfangen und gespeichert)
while currentTimeStamp <= maxTimeStamps:
    mqttc.loop(timeInterval)
    currentTimeStamp = currentTimeStamp + timeInterval

print("Einlesen beendet nach: " + currentTimeStamp + " Schritte")