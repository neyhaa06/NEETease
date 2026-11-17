
from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = (
    PROJECT_ROOT / "core" / "data" / "student_lifestyle_dataset.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "ml" / "artifacts"

# Load data
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("Missing values:\n", df.isnull().sum())
print("\nStress category counts:\n", df["Stress_Level"].value_counts())

# Exclude ID and GPA initially.
# GPA is excluded to reduce the risk of using a feature
# that may encode academic outcomes rather than lifestyle.
# The target's generation method still needs verification.
feature_columns = [
    "Study_Hours_Per_Day",
    "Extracurricular_Hours_Per_Day",
    "Sleep_Hours_Per_Day",
    "Social_Hours_Per_Day",
    "Physical_Activity_Hours_Per_Day",
]

X = df[feature_columns]
y = df["Stress_Level"]

# Separate training and test data before fitting preprocessing.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Keep preprocessing and model fitting together in a pipeline.
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42,
        ),
    ),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluate on the held-out test set
accuracy = accuracy_score(y_test, predictions)
report = classification_report(
    y_test, predictions, output_dict=True, zero_division=0
)
matrix = confusion_matrix(
    y_test, predictions, labels=model.classes_
)

print("\nTest accuracy:", round(accuracy, 4))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))
print("Class order:", list(model.classes_))
print("Confusion matrix:\n", matrix)

# Save the model and evaluation results
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(
    {
        "model": model,
        "feature_columns": feature_columns,
        "classes": list(model.classes_),
    },
    OUTPUT_DIR / "stress_classifier.joblib",
)

results = {
    "dataset_rows": int(len(df)),
    "features": feature_columns,
    "target": "Stress_Level",
    "test_size": 0.20,
    "random_state": 42,
    "accuracy": float(accuracy),
    "classification_report": report,
    "class_order": list(model.classes_),
    "confusion_matrix": matrix.tolist(),
    "limitation": (
        "Predictions reflect patterns in this dataset and are not "
        "a clinical assessment. Verify target-label generation "
        "and dataset provenance before deployment."
    ),
}

with open(OUTPUT_DIR / "evaluation.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print("\nSaved model and evaluation to:", OUTPUT_DIR)
