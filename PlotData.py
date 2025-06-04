import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import json

# Daten aus CSV-Datei einlesen
bottle_data = []

with open("mqtt_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Kopfzeile überspringen (falls vorhanden)

    for row in reader:
        topic = row[0]
        message = row[1]

        # Nur Zeilen mit "drop_oscillation" verarbeiten
        if topic == "iot1/teaching_factory/drop_oscillation":
            try:
                data = json.loads(message)
                bottle_id = data["bottle"]
                drop_values = list(map(float, data["drop_oscillation"]))
                
                # Daten für die Animation speichern
                bottle_data.append((bottle_id, drop_values))

            except json.JSONDecodeError:
                print(f"Fehler beim Verarbeiten der Zeile: {row}")

# Matplotlib-Setup für Animation
fig, ax = plt.subplots()
line, = ax.plot([], [], marker="o", linestyle="-", color="blue")

ax.set_xlabel("Messpunkt")
ax.set_ylabel("Oszillation")
ax.grid()

# Update-Funktion für die Animation (Legende nur mit aktueller ID setzen)
def update(frame):
    if frame < len(bottle_data):
        bottle_id, drop_values = bottle_data[frame]

        line.set_xdata(range(len(drop_values)))
        line.set_ydata(drop_values)
        ax.set_xlim(0, len(drop_values))
        ax.set_ylim(min(drop_values) - 1, max(drop_values) + 1)
        ax.set_title(f"Drop Oscillation Data - Bottle ID: {bottle_id}")

        # Legende zurücksetzen und nur die aktuelle Flasche anzeigen
        ax.legend([f"Bottle ID: {bottle_id}"])

    return line,

# Animation starten
ani = animation.FuncAnimation(fig, update, frames=len(bottle_data), interval=1000, repeat=False)

plt.show()
