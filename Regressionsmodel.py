import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Daten laden
df = pd.read_csv("data_sorted_fill_level_grams.csv")
print(f"Kopfzeile {df.head} \n\n")

# Relevante Spalten auswählen
xData = df[["fill_level_blue", "fill_level_green", "fill_level_red"]]  # Eingangsgrößen
yData = df["final_weight"]  # Zielgröße

# Trainings- und Testdaten aufteilen
xTrainingData, xTestData, yTrainingData, yTestData = train_test_split(xData, yData, test_size=0.2, random_state=42)

# Modell erstellen und trainieren
model = LinearRegression()
model.fit(xTrainingData, yTrainingData)

#print(xTrainingData)
# Vorhersagen machen
yPredictedData = model.predict(xTestData)

mse = mean_squared_error(yTestData, yPredictedData)
print(f"Mittlerer quadratischer Fehler (MSE): {mse}")

# Modellparameter anzeigen
print("Koeffizienten:", model.coef_)
print("Intercept:", model.intercept_)
