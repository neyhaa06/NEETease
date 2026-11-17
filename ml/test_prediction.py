from pathlib import Path

import joblib
import pandas as pd

# Locate the saved model
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "ml" / "artifacts" / "stress_classifier.joblib"

# Load the model and its feature information
saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
feature_columns = saved_data["feature_columns"]

# Example lifestyle data for testing only
student_data = {
    "Study_Hours_Per_Day": 5.0,
    "Extracurricular_Hours_Per_Day": 2.0,
    "Sleep_Hours_Per_Day": 7.0,
    "Social_Hours_Per_Day": 2.0,
    "Physical_Activity_Hours_Per_Day": 1.0,
}

# Arrange inputs in exactly the same order as training
input_data = pd.DataFrame(
    [[student_data[column] for column in feature_columns]],
    columns=feature_columns,
)

# Generate prediction and class probabilities
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)[0]

print("\n--- neetEase Stress Model Test ---")
print("Input lifestyle data:", student_data)
print("Predicted dataset category:", prediction)
print("\nModel probability scores:")

for category, probability in zip(model.classes_, probabilities):
    print(f"{category}: {probability:.1%}")

print("\nTest completed. No database changes were made.")