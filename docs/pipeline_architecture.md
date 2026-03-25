# Pipeline Architecture

## Overview

The fraud detection pipeline runs in 5 steps, in order.
Each step is a Python script that does one job and passes results to the next step.

```
transactions.csv
      ↓
1. validate_data.py       → checks data is clean
      ↓
2. feature_engineering.py → creates features for the model
      ↓
3. train_model.py         → trains and saves the model
      ↓
4. evaluate_model.py      → checks how well the model performs
      ↓
5. predict.py             → generates predictions on test data
      ↓
test_predictions.csv
```

---

## How Each Step Works

### Step 1 — Data Validation (`src/validate_data.py`)

**What it does:**
Loads the raw transaction data and checks it is ready for processing.

**Checks performed:**
- Dataset shape (should be 50,000 rows × 14 columns)
- Column names and data types
- Missing values (none found)
- Duplicate transaction IDs

**Input:** `data/transactions.csv`
**Output:** Confirmation that data is clean

---

### Step 2 — Feature Engineering (`src/feature_engineering.py`)

**What it does:**
Takes the raw data and creates 15 new features that help the model detect fraud.
Groups features into 4 categories: time, amount, behaviour, and location.

**Input:** Raw transaction dataframe
**Output:** Dataframe with 15 additional feature columns

---

### Step 3 — Model Training (`src/train_model.py`)

**What it does:**
Trains 4 machine learning models and saves the best one.

**Steps inside:**
1. Splits data into 80% train, 20% test
2. Handles class imbalance using SMOTE (fraud is only 4% of data)
3. Scales features using StandardScaler
4. Trains Logistic Regression, Random Forest, XGBoost, LightGBM
5. Compares all 4 models
6. Tunes XGBoost (best model) using GridSearchCV
7. Saves final model and scaler

**Input:** Feature-engineered dataframe
**Output:** `models/fraud_detection_model.pkl`, `models/scaler.pkl`

---

### Step 4 — Model Evaluation (`src/evaluate_model.py`)

**What it does:**
Loads the saved model and measures how well it detects fraud.

**Metrics reported:**
- Classification report (precision, recall, F1)
- Confusion matrix
- ROC curve
- Feature importance chart

**Input:** `models/fraud_detection_model.pkl`
**Output:** Performance metrics and charts

---

### Step 5 — Predictions (`src/predict.py`)

**What it does:**
Loads the test data, applies the same feature engineering, runs the model, and saves predictions.

**Input:** `data/test_transactions.json`, `models/fraud_detection_model.pkl`
**Output:** `data/test_predictions.csv`

---

## How to Run

### Run locally
```bash
python main.py
```

### Run with Docker
```bash
docker build -f dockerfiles/Dockerfile -t fraud-detection .
docker run -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models fraud-detection
```

### Run with Argo Workflows
```bash
argo submit argo/workflow.yaml
argo watch fraud-detection-pipeline-xxxxx
```

---

## Technology Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Main programming language |
| pandas / numpy | Data processing |
| scikit-learn | Model training and evaluation |
| XGBoost | Best performing model |
| imbalanced-learn | Handling class imbalance (SMOTE) |
| Docker | Packaging the pipeline |
| Argo Workflows | Running the pipeline on Kubernetes |