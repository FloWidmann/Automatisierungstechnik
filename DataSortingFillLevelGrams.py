import pandas as pd
import json

# CSV-Datei laden
df = pd.read_csv("mqtt_data.csv", header=None)

# Filtern nach dispenser-Werten
filteredDispenserBlue = df[df[0].str.contains("dispenser_blue", na=False)]
filteredDispenserGreen = df[df[0].str.contains("dispenser_green", na=False)]
filteredDispenserRed = df[df[0].str.contains("dispenser_red", na=False)]
filteredWeight = df[df[0].str.contains("final_weight", na=False)]

# JSON-Daten extrahieren
fillLevelBlue = filteredDispenserBlue[1].apply(lambda x: json.loads(x).get("fill_level_grams"))
fillLevelGreen = filteredDispenserGreen[1].apply(lambda x: json.loads(x).get("fill_level_grams"))
fillLevelRed = filteredDispenserRed[1].apply(lambda x: json.loads(x).get("fill_level_grams"))
finalWeight = filteredWeight[1].apply(lambda x: json.loads(x).get("final_weight"))

# Richtige Zuordnung der BottleIDs
bottleBlue = filteredDispenserBlue[1].apply(lambda x: json.loads(x).get("bottle"))
bottleGreen = filteredDispenserGreen[1].apply(lambda x: json.loads(x).get("bottle"))
bottleRed = filteredDispenserRed[1].apply(lambda x: json.loads(x).get("bottle"))
bottleWeight = filteredWeight[1].apply(lambda x: json.loads(x).get("bottle"))

# Dictionaries direkt in Variablen speichern
dict_blue = dict(zip(bottleBlue.dropna(), fillLevelBlue.dropna()))
dict_green = dict(zip(bottleGreen.dropna(), fillLevelGreen.dropna()))
dict_red = dict(zip(bottleRed.dropna(), fillLevelRed.dropna()))
dict_weight = dict(zip(bottleWeight.dropna(), finalWeight.dropna()))

# Alle einzigartigen Bottle-IDs sammeln (jetzt korrekt!)
all_bottle_ids = sorted(set(dict_blue.keys()).union(set(dict_green.keys()), set(dict_red.keys()), set(dict_weight.keys())))

# Daten in ein DataFrame packen
df_sorted = pd.DataFrame({
    "ID": all_bottle_ids,
    "fill_level_blue": [dict_blue.get(bottle_id, 0.0) for bottle_id in all_bottle_ids],
    "fill_level_green": [dict_green.get(bottle_id, 0.0) for bottle_id in all_bottle_ids],
    "fill_level_red": [dict_red.get(bottle_id, 0.0) for bottle_id in all_bottle_ids],
    "final_weight": [dict_weight.get(bottle_id, 0.0) for bottle_id in all_bottle_ids]
})

# CSV-Datei speichern
df_sorted.to_csv("data_sorted.csv", index=False)

print("CSV-Datei 'data_sorted.csv' wurde erfolgreich erstellt!")
