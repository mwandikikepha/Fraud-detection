import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import warnings
import sys
import os
warnings.filterwarnings('ignore')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, RocCurveDisplay
from imblearn.over_sampling import SMOTE

from src.feature_engineering import engineer_features
from config import TRAIN_DATA_PATH, MODEL_PATH, DROP_COLS, RANDOM_STATE, TEST_SIZE

# Load and engineer features
df = pd.read_csv(TRAIN_DATA_PATH)
df = engineer_features(df)

# Define features and target
drop_cols = [c for c in DROP_COLS if c in df.columns]
X = df.drop(columns=drop_cols + ['is_fraud'])
y = df['is_fraud']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)

# Load model
best_xgb = joblib.load(MODEL_PATH)

# Predictions
y_pred = best_xgb.predict(X_test)
y_prob = best_xgb.predict_proba(X_test)[:,1]

# How did it do?
print(classification_report(y_test, y_pred))

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
plt.title("Confusion Matrix")
plt.show()

# ROC curve
RocCurveDisplay.from_predictions(y_test, y_prob)
plt.title("ROC Curve")
plt.show()

# Which features matter most?
importance = pd.Series(best_xgb.feature_importances_, index=X.columns)
importance.sort_values(ascending=True).tail(15).plot(kind='barh')
plt.title("Top 15 Most Important Features")
plt.show()