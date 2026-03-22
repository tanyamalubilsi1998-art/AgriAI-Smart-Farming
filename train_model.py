import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier

print("Loading real-world dataset...")
try:
    df = pd.read_csv('crop_data.csv')
except FileNotFoundError:
    print("Error: Could not find 'crop_data.csv'. Make sure it is in your folder!")
    exit()

X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

print("Training Agronomy AI Model on real data...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/agronomy_model.pkl')
print("Success! Your AI model is trained and saved.")