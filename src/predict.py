import pandas as pd
import numpy as np
import joblib
import json
import warnings
import sys
import os
warnings.filterwarnings('ignore')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.feature_engineering import engineer_features
from config import TEST_DATA_PATH, MODEL_PATH, DROP_COLS, PREDICTIONS_PATH

# Load the test data
with open(TEST_DATA_PATH, 'r') as f:
    test_data = json.load(f)

test_df = pd.DataFrame(test_data)
print(f"Test transactions: {len(test_df)}")

# Apply the same feature engineering
test_df = engineer_features(test_df)

# Load model
best_xgb = joblib.load(MODEL_PATH)

# Drop same columns as training
drop_cols = [c for c in DROP_COLS if c in test_df.columns]
X_test_final = test_df.drop(columns=drop_cols)

# Generate predictions
predictions = best_xgb.predict(X_test_final)

# Save to file
submission_df = pd.DataFrame({
    'transaction_id':  test_df['transaction_id'],
    'predicted_fraud': predictions
})

# Verify format
print(f"Submission shape: {submission_df.shape}")
print(f"Unique predictions: {submission_df['predicted_fraud'].unique()}")
print(f"\nPrediction distribution:")
print(submission_df['predicted_fraud'].value_counts())

submission_df.head()

# Save predictions to CSV
submission_df.to_csv(PREDICTIONS_PATH, index=False)
print("✅ Predictions saved to test_predictions.csv")
print("\n⚠️ Remember to include this file in your submission!")