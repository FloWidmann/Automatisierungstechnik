import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import json

requested_data = "drop_oscillation"
requested_data_full_path = "iot1/teaching_factory/" + requested_data


bottle_data = []

with open("mqtt_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        topic = row[0]
        message = row[1]

        if topic == requested_data_full_path:
            try:
                data = json.loads(message)
                bottle_id = data["bottle"]
                shown_values = list(map(float, data[requested_data]))
                
                bottle_data.append((bottle_id, shown_values))

            except json.JSONDecodeError:
                print(f"Fehler beim Verarbeiten der Zeile: {row}")


fig, ax = plt.subplots()
line, = ax.plot([], [], marker="o", linestyle="-", color="blue")

ax.set_xlabel("Messpunkt")
ax.grid()

def update(frame):
    if frame < len(bottle_data):
        bottle_id, drop_values = bottle_data[frame]

        line.set_xdata(range(len(drop_values)))
        line.set_ydata(drop_values)
        ax.set_xlim(0, len(drop_values))
        ax.set_ylim(min(drop_values) - 1, max(drop_values) + 1)
        ax.set_title(f"{requested_data} - Bottle ID: {bottle_id}")
        ax.legend([f"Bottle ID: {bottle_id}"])

    return line,

ani = animation.FuncAnimation(fig, update, frames=len(bottle_data), interval=2000, repeat=False)

plt.show()
