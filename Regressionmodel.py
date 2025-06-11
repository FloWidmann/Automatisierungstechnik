import pandas as pd
import json

# CSV-Datei laden
df = pd.read_csv("mqtt_data.csv", header=None)

# Filtern nach dispenser-Werten
filteredDispenserBlue = df[df[0].str.contains("dispenser_blue", na=False)]
filteredDispenserGreen = df[df[0].str.contains("dispenser_green", na=False)]
filteredDispenserRed = df[df[0].str.contains("dispenser_red", na=False)]

# JSON-Daten extrahieren
fillLevelBlue = filteredDispenserBlue[1].apply(lambda x: json.loads(x).get("fill_level_grams"))
fillLevelGreen = filteredDispenserGreen[1].apply(lambda x: json.loads(x).get("fill_level_grams"))
fillLevelRed = filteredDispenserRed[1].apply(lambda x: json.loads(x).get("fill_level_grams"))

# NaN-Werte entfernen und Listen in ein DataFrame packen
df_filtered = pd.DataFrame({
    "fill_level_blue": fillLevelBlue.dropna().tolist(),
    "fill_level_green": fillLevelGreen.dropna().tolist(),
    "fill_level_red": fillLevelRed.dropna().tolist()
})

# DataFrame in eine CSV-Datei speichern
df_filtered.to_csv("data_filtered.csv", index=False)

print("CSV-Datei 'data_filtered.csv' wurde erfolgreich erstellt!")
