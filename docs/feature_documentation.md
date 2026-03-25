# Feature Documentation

## Overview

We engineered 15 features from the raw transaction data.
These features are grouped into 4 categories based on what they capture.

All features are created in `src/feature_engineering.py` using the `engineer_features()` function.

---

## Category 1 — Time Features

These capture *when* the transaction happened.
From EDA we found fraud is 15x more likely between 12am and 4am.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `hour` | `timestamp.dt.hour` | Fraud peaks at night hours |
| `day_of_week` | `timestamp.dt.dayofweek` | Captures weekly patterns |
| `month` | `timestamp.dt.month` | Captures monthly patterns |
| `is_weekend` | 1 if day_of_week >= 5 | Weekend behaviour differs |
| `is_night` | 1 if hour <= 4 | Night = 34% fraud rate vs 2% daytime |

---

## Category 2 — Amount Features

These capture *how much* is being sent and whether it looks suspicious.
From EDA we found fraud amounts are 4x higher on average.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `amount_to_balance_ratio` | `amount / sender_balance_before` | Are they sending most of their balance? |
| `balance_after_ratio` | `sender_balance_after / sender_balance_before` | How much is left after? |
| `is_round_amount` | 1 if amount % 100 == 0 | Round amounts are 50x more common in fraud |

---

## Category 3 — Behavioural Features

These capture *how this sender normally behaves* and whether this transaction is unusual.
These are the most powerful features because they detect anomalies.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `sender_tx_count` | Count of all sender's transactions | High volume senders may be suspicious |
| `sender_tx_per_day` | Count of sender's transactions per day | Unusual daily activity |
| `sender_avg_amount` | Mean of sender's transaction amounts | Establishes normal spending level |
| `amount_vs_avg` | `amount / sender_avg_amount` | Is this amount way above their norm? |
| `sender_unique_receivers` | Count of unique receivers per sender | Fraudsters send to many different accounts |
| `receiver_tx_count` | Count of all receiver's transactions | Mule accounts receive many transactions |

---

## Category 4 — Device & Location Features

These capture *where and from what device* the transaction happened.
From EDA we found fraud transactions come from more spread out locations.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `device_tx_count` | Count of transactions per device | Shared/stolen devices used for fraud |
| `location_distance` | Distance from sender's average location | Fraud often comes from unusual locations |

---

## Feature Importance (from XGBoost model)

After training, these were the most important features:

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | `location_distance` | 0.33 |
| 2 | `amount` | 0.14 |
| 3 | `hour` | 0.14 |
| 4 | `device_tx_count` | 0.08 |
| 5 | `is_night` | 0.07 |
| 6 | `is_weekend` | 0.05 |
| 7 | `is_round_amount` | 0.04 |
| 8 | `amount_vs_avg` | 0.04 |

---

## Note on Data Leakage

During development, `device_fraud_rate` (average fraud rate per device) was initially created as a feature.
This was removed because it is calculated directly from the target variable `is_fraud`, which would give the model an unfair advantage and inflate performance scores.

After removing it, the model F1 score dropped from 0.93 to 0.78 — the honest, real performance.# Feature Documentation

## Overview

We engineered 15 features from the raw transaction data.
These features are grouped into 4 categories based on what they capture.

All features are created in `src/feature_engineering.py` using the `engineer_features()` function.

---

## Category 1 — Time Features

These capture *when* the transaction happened.
From EDA we found fraud is 15x more likely between 12am and 4am.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `hour` | `timestamp.dt.hour` | Fraud peaks at night hours |
| `day_of_week` | `timestamp.dt.dayofweek` | Captures weekly patterns |
| `month` | `timestamp.dt.month` | Captures monthly patterns |
| `is_weekend` | 1 if day_of_week >= 5 | Weekend behaviour differs |
| `is_night` | 1 if hour <= 4 | Night = 34% fraud rate vs 2% daytime |

---

## Category 2 — Amount Features

These capture *how much* is being sent and whether it looks suspicious.
From EDA we found fraud amounts are 4x higher on average.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `amount_to_balance_ratio` | `amount / sender_balance_before` | Are they sending most of their balance? |
| `balance_after_ratio` | `sender_balance_after / sender_balance_before` | How much is left after? |
| `is_round_amount` | 1 if amount % 100 == 0 | Round amounts are 50x more common in fraud |

---

## Category 3 — Behavioural Features

These capture *how this sender normally behaves* and whether this transaction is unusual.
These are the most powerful features because they detect anomalies.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `sender_tx_count` | Count of all sender's transactions | High volume senders may be suspicious |
| `sender_tx_per_day` | Count of sender's transactions per day | Unusual daily activity |
| `sender_avg_amount` | Mean of sender's transaction amounts | Establishes normal spending level |
| `amount_vs_avg` | `amount / sender_avg_amount` | Is this amount way above their norm? |
| `sender_unique_receivers` | Count of unique receivers per sender | Fraudsters send to many different accounts |
| `receiver_tx_count` | Count of all receiver's transactions | Mule accounts receive many transactions |

---

## Category 4 — Device & Location Features

These capture *where and from what device* the transaction happened.
From EDA we found fraud transactions come from more spread out locations.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `device_tx_count` | Count of transactions per device | Shared/stolen devices used for fraud |
| `location_distance` | Distance from sender's average location | Fraud often comes from unusual locations |

---

## Feature Importance (from XGBoost model)

After training, these were the most important features:

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | `location_distance` | 0.33 |
| 2 | `amount` | 0.14 |
| 3 | `hour` | 0.14 |
| 4 | `device_tx_count` | 0.08 |
| 5 | `is_night` | 0.07 |
| 6 | `is_weekend` | 0.05 |
| 7 | `is_round_amount` | 0.04 |
| 8 | `amount_vs_avg` | 0.04 |

---

## Note on Data Leakage

During development, `device_fraud_rate` (average fraud rate per device) was initially created as a feature.
This was removed because it is calculated directly from the target variable `is_fraud`, which would give the model an unfair advantage and inflate performance scores.

After removing it, the model F1 score dropped from 0.93 to 0.78 — the honest, real performance.# Feature Documentation

## Overview

We engineered 15 features from the raw transaction data.
These features are grouped into 4 categories based on what they capture.

All features are created in `src/feature_engineering.py` using the `engineer_features()` function.

---

## Category 1 — Time Features

These capture *when* the transaction happened.
From EDA we found fraud is 15x more likely between 12am and 4am.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `hour` | `timestamp.dt.hour` | Fraud peaks at night hours |
| `day_of_week` | `timestamp.dt.dayofweek` | Captures weekly patterns |
| `month` | `timestamp.dt.month` | Captures monthly patterns |
| `is_weekend` | 1 if day_of_week >= 5 | Weekend behaviour differs |
| `is_night` | 1 if hour <= 4 | Night = 34% fraud rate vs 2% daytime |

---

## Category 2 — Amount Features

These capture *how much* is being sent and whether it looks suspicious.
From EDA we found fraud amounts are 4x higher on average.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `amount_to_balance_ratio` | `amount / sender_balance_before` | Are they sending most of their balance? |
| `balance_after_ratio` | `sender_balance_after / sender_balance_before` | How much is left after? |
| `is_round_amount` | 1 if amount % 100 == 0 | Round amounts are 50x more common in fraud |

---

## Category 3 — Behavioural Features

These capture *how this sender normally behaves* and whether this transaction is unusual.
These are the most powerful features because they detect anomalies.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `sender_tx_count` | Count of all sender's transactions | High volume senders may be suspicious |
| `sender_tx_per_day` | Count of sender's transactions per day | Unusual daily activity |
| `sender_avg_amount` | Mean of sender's transaction amounts | Establishes normal spending level |
| `amount_vs_avg` | `amount / sender_avg_amount` | Is this amount way above their norm? |
| `sender_unique_receivers` | Count of unique receivers per sender | Fraudsters send to many different accounts |
| `receiver_tx_count` | Count of all receiver's transactions | Mule accounts receive many transactions |

---

## Category 4 — Device & Location Features

These capture *where and from what device* the transaction happened.
From EDA we found fraud transactions come from more spread out locations.

| Feature | How it's created | Why it helps |
|---------|-----------------|--------------|
| `device_tx_count` | Count of transactions per device | Shared/stolen devices used for fraud |
| `location_distance` | Distance from sender's average location | Fraud often comes from unusual locations |

---

## Feature Importance (from XGBoost model)

After training, these were the most important features:

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | `location_distance` | 0.33 |
| 2 | `amount` | 0.14 |
| 3 | `hour` | 0.14 |
| 4 | `device_tx_count` | 0.08 |
| 5 | `is_night` | 0.07 |
| 6 | `is_weekend` | 0.05 |
| 7 | `is_round_amount` | 0.04 |
| 8 | `amount_vs_avg` | 0.04 |

---

## Note on Data Leakage

During development, `device_fraud_rate` (average fraud rate per device) was initially created as a feature.
This was removed because it is calculated directly from the target variable `is_fraud`, which would give the model an unfair advantage and inflate performance scores.

After removing it, the model F1 score dropped from 0.93 to 0.78 — the honest, real performance.