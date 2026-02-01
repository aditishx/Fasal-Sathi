import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv(r"C:\Users\Shiva\OneDrive\Desktop\crop_data.csv")

X = data.drop("label", axis=1)
y = data["label"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
pickle.dump(model, open("crop_model.pkl", "wb"))

print("Crop model trained and saved successfully")
