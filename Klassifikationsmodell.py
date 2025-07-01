import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# CSV laden
df = pd.read_csv("deine_datei.csv")

# Zeitreihe aus String in Liste umwandeln
df["oscillation"] = df["oscilattion"].apply(lambda x: np.array(eval(x), dtype=float))

# Features extrahieren (z. B. Mittelwert, Standardabweichung, Max, Min)
df["osc_mean"] = df["oscillation"].apply(np.mean)
df["osc_std"] = df["oscillation"].apply(np.std)
df["osc_max"] = df["oscillation"].apply(np.max)
df["osc_min"] = df["oscillation"].apply(np.min)

# Zielvariable
y = df["is cracked"]

# Feature-Matrix
X = df[["osc_mean", "osc_std", "osc_max", "osc_min"]]

# Train/Test-Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Klassifikator trainieren
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Vorhersage & F1-Score
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred)
