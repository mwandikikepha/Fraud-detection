import pandas as pd
import numpy as np


def engineer_features(df):

    # Convert to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- Temporal Features ---
    df['hour']        = df['timestamp'].dt.hour
    df['day']         = df['timestamp'].dt.day
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month']       = df['timestamp'].dt.month
    df['is_weekend']  = (df['day_of_week'] >= 5).astype(int)
    df['is_night']    = (df['hour'] <= 4).astype(int)

    # --- Transaction Velocity Features ---
    # How many transactions has each sender made in total?
    df['sender_tx_count'] = df.groupby('sender_id')['transaction_id'].transform('count')

    # How many transactions has each sender made per day?
    df['sender_tx_per_day'] = df.groupby(['sender_id', df['timestamp'].dt.date])['transaction_id'].transform('count')

    # How much does this sender usually spend on average?
    df['sender_avg_amount'] = df.groupby('sender_id')['amount'].transform('mean')

    # Is this transaction amount unusual for this sender?
    df['amount_vs_avg'] = df['amount'] / (df['sender_avg_amount'] + 1)

    # How many unique receivers has this sender sent to?
    df['sender_unique_receivers'] = df.groupby('sender_id')['receiver_id'].transform('nunique')

    # Total transactions per receiver
    df['receiver_tx_count'] = df.groupby('receiver_id')['transaction_id'].transform('count')

    # --- Amount-Based Features ---
    # How much of their balance are they sending?
    df['amount_to_balance_ratio'] = df['amount'] / (df['sender_balance_before'] + 1)

    # How much balance is left after the transaction?
    df['balance_after_ratio'] = df['sender_balance_after'] / (df['sender_balance_before'] + 1)

    # Is the amount a round number?
    df['is_round_amount'] = (df['amount'] % 100 == 0).astype(int)

    # --- Behavioral Features ---
    # How many different receivers has this sender used?
    df['sender_unique_receivers'] = df.groupby('sender_id')['receiver_id'].transform('nunique')

    # --- Device & Location Features ---
    # How often is this device used?
    df['device_tx_count'] = df.groupby('device_id')['transaction_id'].transform('count')

    # How far is this transaction from the sender's usual location?
    df['sender_avg_lat'] = df.groupby('sender_id')['location_lat'].transform('mean')
    df['sender_avg_lon'] = df.groupby('sender_id')['location_lon'].transform('mean')
    df['location_distance'] = np.sqrt(
        (df['location_lat'] - df['sender_avg_lat'])**2 +
        (df['location_lon'] - df['sender_avg_lon'])**2
    )

    return df