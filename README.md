# Mobile Money Fraud Detection
**Challenge:** AI Engineering Challenge — End-to-End ML Fraud Detection Pipeline

---

## What This Project Does

This project builds a system that automatically detects fraudulent mobile money transactions. It works like this:

1. Takes in transaction data (amount, time, location, sender, receiver)
2. Engineers features that help identify suspicious patterns
3. Trains a machine learning model to flag fraud
4. Packages everything into an automated pipeline using Docker and Argo Workflows

---

## Project Structure

```
ai_project/
├── README.md                        # This file
├── config.py                        # All paths and settings in one place
├── main.py                          # Runs the full pipeline with one command
├── requirements.txt                 # All Python libraries needed
├── data/
│   ├── transactions.csv             # Training data (50,000 transactions)
│   ├── test_transactions.json       # Test data (10,000 transactions)
│   └── test_predictions.csv        # Our fraud predictions (submitted)
├── models/
│   ├── fraud_detection_model.pkl    # Trained XGBoost model
│   └── scaler.pkl                   # Feature scaler
├── notebooks/
│   └── fraud_detection1.ipynb      # Full analysis notebook
├── dockerfiles/
│   └── Dockerfile                   # Packages the pipeline into a container
├── argo/
│   └── workflow.yaml                # Argo pipeline definition
└── src/
    ├── validate_data.py             # Step 1: Check data quality
    ├── feature_engineering.py       # Step 2: Create model features
    ├── train_model.py               # Step 3: Train the model
    ├── evaluate_model.py            # Step 4: Evaluate performance
    └── predict.py                   # Step 5: Generate predictions
```

---

## Phase 1: Data Science

### The Data
- 50,000 labeled mobile money transactions (Jan–Jun 2024)
- 14 columns: transaction ID, timestamp, sender, receiver, amount, type, balances, device, location
- Fraud rate: 4% (2,000 fraud / 48,000 legitimate)

### Key Findings from EDA

| Finding | Detail |
|---------|--------|
| Night fraud | Transactions at 12am–4am are 15x more likely to be fraud |
| High amounts | Fraud median amount is KES 5,474 vs KES 1,368 for legitimate |
| Round numbers | 10% of fraud uses round amounts vs 0.002% of legitimate |
| Location | Fraud transactions come from more spread out locations |
| Transaction type | All types have similar fraud rates — weak signal alone |

### Features Engineered

| Feature | Description |
|---------|-------------|
| `is_night` | 1 if transaction is between 12am–4am |
| `hour` | Hour of the day |
| `day_of_week` | Day of the week |
| `is_weekend` | 1 if Saturday or Sunday |
| `amount_to_balance_ratio` | How much of their balance they are sending |
| `balance_after_ratio` | How much balance is left after transaction |
| `is_round_amount` | 1 if amount is a round number |
| `sender_tx_count` | Total transactions this sender has made |
| `sender_tx_per_day` | How many transactions sender makes per day |
| `sender_avg_amount` | Sender's average transaction amount |
| `amount_vs_avg` | Is this amount unusual for this sender? |
| `sender_unique_receivers` | How many different receivers this sender has used |
| `receiver_tx_count` | Total transactions this receiver has received |
| `device_tx_count` | How often this device is used |
| `location_distance` | How far this transaction is from sender's usual location |

### Model Results

| Model | AUC | F1 | Precision | Recall |
|-------|-----|----|-----------|--------|
| Logistic Regression | 0.9971 | 0.8529 | 0.7789 | 0.9425 |
| Random Forest | 0.9990 | 0.9078 | 0.8610 | 0.9600 |
| XGBoost | 0.9995 | 0.9428 | 0.9381 | 0.9475 |
| LightGBM | 0.9995 | 0.9371 | 0.9246 | 0.9500 |

**Winner: XGBoost** — highest AUC and F1 score.

### Final Model Performance (after removing data leakage)

| Metric | Value |
|--------|-------|
| Accuracy | 98% |
| Precision | 79% |
| Recall | 78% |
| F1 Score | 0.78 |
| AUC-ROC | 0.9995 |

### Top Features by Importance
1. `location_distance` — fraud happens far from sender's usual location
2. `amount` — fraud involves higher amounts
3. `hour` — time of day is a strong signal
4. `device_tx_count` — device usage frequency
5. `is_night` — night transactions are riskier

---

## Phase 2: MLOps

### Docker
The entire pipeline is packaged into a Docker container for reproducibility.

**Build the image:**
```bash
docker build -f dockerfiles/Dockerfile -t fraud-detection .
```

**Run the pipeline:**
```bash
docker run -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models fraud-detection
```

### Argo Workflow
The pipeline is defined as an Argo Workflow with 5 steps that run in order:

```
validate-data → engineer-features → train-model → evaluate-model → export-model
```

Each step runs inside the `fraud-detection` Docker container.

**To run with Argo (requires Kubernetes + Argo installed):**
```bash
argo submit argo/workflow.yaml
argo watch fraud-detection-pipeline-xxxxx
```

---

## How to Run Locally

### 1. Set up environment
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python main.py
```

### 3. Or run steps individually
```bash
python src/validate_data.py
python src/train_model.py
python src/evaluate_model.py
python src/predict.py
```

### 4. Run with Docker
```bash
docker build -f dockerfiles/Dockerfile -t fraud-detection .
docker run -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models fraud-detection
```

---

## Test Predictions

Predictions for the test set are saved in `data/test_predictions.csv`.

- Total test transactions: 10,000
- Flagged as fraud: 306 (3.06%)
- Expected fraud rate: ~4%

Format:
```csv
transaction_id,predicted_fraud
6739205AC695C940,0
0891D338A86BFD86,1
...
```

---

## Limitations & Future Improvements

- **More historical data** — behavioural features would be stronger with more transaction history per user
- **Real-time features** — velocity features (transactions in last hour) would improve detection
- **Threshold tuning** — adjusting the fraud threshold based on business cost of false positives vs false negatives
- **Model monitoring** — track model performance over time as fraud patterns change
