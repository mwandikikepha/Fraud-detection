# Paths
TRAIN_DATA_PATH = "data/transactions.csv"
TEST_DATA_PATH  = "data/test_transactions.json"
MODEL_PATH      = "models/fraud_detection_model.pkl"
SCALER_PATH     = "models/scaler.pkl"
PREDICTIONS_PATH = "data/test_predictions.csv"

# Model settings
RANDOM_STATE = 42
TEST_SIZE    = 0.2

# Columns to drop before modeling
DROP_COLS = [
    'transaction_id', 'timestamp', 'sender_id', 'receiver_id',
    'device_id', 'transaction_type', 'sender_avg_lat',
    'sender_avg_lon', 'day', 'device_fraud_rate'
]