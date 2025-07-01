import pandas as pd
import json

# CSV-Datei laden
df = pd.read_csv("mqtt_data.csv", header=None)

# Filtern nach dispenser-Werten
filteredDropOscillation = df[df[0].str.contains("drop_oscillation", na=False)]
filteredIsBottleCracked = df[df[0].str.contains("ground_truth", na=False)]

# JSON-Daten extrahieren
dropOscillations = filteredDropOscillation[1].apply(lambda x: json.loads(x).get("drop_oscillation"))
isBottleCracked = filteredIsBottleCracked[1].apply(lambda x: json.loads(x).get("is_cracked"))

# Richtige Zuordnung der BottleIDs
bottleOscillation = filteredDropOscillation[1].apply(lambda x: json.loads(x).get("bottle"))
crackedBottles = filteredIsBottleCracked[1].apply(lambda x: json.loads(x).get("bottle"))

# Dictionaries direkt in Variablen speichern
dictOscillation = dict(zip(bottleOscillation.dropna(), dropOscillations.dropna()))
dictCrackedBottles = dict(zip(crackedBottles.dropna(), isBottleCracked.dropna()))


# Alle einzigartigen Bottle-IDs sammeln
all_bottle_ids = sorted(set(dictCrackedBottles.keys()).union(set(dictOscillation.keys())))

# Daten in ein DataFrame packen
df_sorted = pd.DataFrame({
    "ID ": all_bottle_ids,
    "is cracked ": [dictCrackedBottles.get(bottle_id, 0.0) for bottle_id in all_bottle_ids],
    "oscilation ": [dictOscillation.get(bottle_id, 0.0) for bottle_id in all_bottle_ids]
})


# CSV-Datei speichern
df_sorted.to_csv("data_sorted_vibration.csv", index=False)

print("CSV-Datei 'data_sorted_vibration.csv' wurde erfolgreich erstellt!")
