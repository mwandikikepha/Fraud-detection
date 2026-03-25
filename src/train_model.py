import pandas as pd
import numpy as np
import joblib
import warnings
import sys
import os
warnings.filterwarnings('ignore')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, precision_score, recall_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE

from src.feature_engineering import engineer_features
from config import TRAIN_DATA_PATH, MODEL_PATH, SCALER_PATH, DROP_COLS, RANDOM_STATE, TEST_SIZE

np.random.seed(RANDOM_STATE)

# Load and engineer features
df = pd.read_csv(TRAIN_DATA_PATH)
df = engineer_features(df)

# Define features and target
drop_cols = [c for c in DROP_COLS if c in df.columns]
X = df.drop(columns=drop_cols + ['is_fraud'])
y = df['is_fraud']

print(f"Features: {X.shape[1]}")
print(X.columns.tolist())

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)

print(f"Train size: {X_train.shape[0]:,}")
print(f"Test size:  {X_test.shape[0]:,}")
print(f"Fraud in train: {y_train.mean():.2%}")
print(f"Fraud in test:  {y_test.mean():.2%}")

# Handle class imbalance with SMOTE
smote = SMOTE(random_state=RANDOM_STATE)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled  = scaler.transform(X_test)

# --- Baseline Model ---
lr = LogisticRegression(random_state=RANDOM_STATE)
lr.fit(X_train_scaled, y_train_resampled)
y_pred = lr.predict(X_test_scaled)
print("\nLogistic Regression:")
print(classification_report(y_test, y_pred))

# --- Random Forest ---
rf = RandomForestClassifier(random_state=RANDOM_STATE)
rf.fit(X_train_resampled, y_train_resampled)
y_pred_rf = rf.predict(X_test)
print("\nRandom Forest:")
print(classification_report(y_test, y_pred_rf))

# --- XGBoost ---
xgb = XGBClassifier(random_state=RANDOM_STATE)
xgb.fit(X_train_resampled, y_train_resampled)
y_pred_xgb = xgb.predict(X_test)
print("\nXGBoost:")
print(classification_report(y_test, y_pred_xgb))

# --- LightGBM ---
lgbm = LGBMClassifier(random_state=RANDOM_STATE)
lgbm.fit(X_train_resampled, y_train_resampled)
y_pred_lgbm = lgbm.predict(X_test)
print("\nLightGBM:")
print(classification_report(y_test, y_pred_lgbm))

# --- Model Comparison ---
models = {
    'Logistic Regression': (lr, X_test_scaled),
    'Random Forest':       (rf, X_test),
    'XGBoost':             (xgb, X_test),
    'LightGBM':            (lgbm, X_test)
}

results = []
for name, (model, X_eval) in models.items():
    y_pred = model.predict(X_eval)
    y_prob = model.predict_proba(X_eval)[:,1]
    results.append({
        'Model':     name,
        'AUC':       round(roc_auc_score(y_test, y_prob), 4),
        'F1':        round(f1_score(y_test, y_pred), 4),
        'Precision': round(precision_score(y_test, y_pred), 4),
        'Recall':    round(recall_score(y_test, y_pred), 4)
    })

print("\nModel Comparison:")
print(pd.DataFrame(results))

# --- Hyperparameter Tuning (XGBoost) ---
params = {
    'n_estimators':  [100, 200],
    'max_depth':     [3, 5],
    'learning_rate': [0.1, 0.2]
}

grid = GridSearchCV(XGBClassifier(random_state=RANDOM_STATE), params, cv=3, scoring='f1')
grid.fit(X_train_resampled, y_train_resampled)
print("Best settings:", grid.best_params_)

# --- Final Model ---
best_xgb = XGBClassifier(**grid.best_params_, random_state=RANDOM_STATE)
best_xgb.fit(X_train_resampled, y_train_resampled)

y_pred = best_xgb.predict(X_test)
y_prob = best_xgb.predict_proba(X_test)[:,1]
print("\nFinal Model:")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(best_xgb, MODEL_PATH)
joblib.dump(scaler,   SCALER_PATH)
print("Model saved!")