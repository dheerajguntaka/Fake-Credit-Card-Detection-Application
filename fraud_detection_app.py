""# Fake Credit Card Detection System Using Python
# Structured Approach: Data Collection, Data Preprocessing, Rule-Based Detection, Validation, Deployment

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from flask import Flask, request, jsonify
import os

# Step 1: Data Collection
def load_data(file_path):
    '''
    Loads credit card transaction data from a CSV file.
    Args:
        file_path (str): The path to the CSV file containing transaction data.
    Returns:
        DataFrame: Loaded dataset as a Pandas DataFrame.
    '''
    try:
        data = pd.read_csv(file_path)
        print("✅ Data successfully loaded.")
        return data
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return None

# Step 2: Data Preprocessing
def preprocess_data(df):
    '''
    Preprocesses the transaction data for analysis.
    Args:
        df (DataFrame): The raw dataset.
    Returns:
        DataFrame: Preprocessed dataset.
    '''
    print("🔄 Preprocessing data...")

    # Drop duplicates and null values
    df = df.drop_duplicates()
    df = df.dropna()

    # Normalize 'Amount' field and extract relevant features
    if 'Amount' in df.columns:
        df['Amount'] = df['Amount'].astype(float)
    
    # Handle timestamp if present
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    print("✅ Data preprocessing completed.")
    return df

# Step 3: Rule-Based Fraud Detection
def luhn_algorithm(card_number: str) -> bool:
    '''Validates credit card number using Luhn's Algorithm.'''
    card_number = card_number.replace(' ', '')
    if not card_number.isdigit():
        return False

    total = 0
    reverse_digits = card_number[::-1]

    for idx, digit in enumerate(reverse_digits):
        n = int(digit)
        if idx % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0

def rule_based_detection(df):
    '''
    Analyzes transaction patterns using predefined fraud detection rules.
    Args:
        df (DataFrame): Preprocessed transaction data.
    Returns:
        DataFrame: Data with an additional column for fraud detection.
    '''
    print("🔍 Applying rule-based fraud detection...")

    # Rule 1: Luhn validation for card numbers
    if 'CardNumber' in df.columns:
        df['LuhnValid'] = df['CardNumber'].apply(luhn_algorithm)
    
    # Rule 2: Large transaction detection
    if 'Amount' in df.columns:
        df['HighAmount'] = df['Amount'] > 1000  # Threshold for high transactions
    
    # Rule 3: Check for multiple transactions in a short period (if Timestamp exists)
    if 'Timestamp' in df.columns:
        df['TimeGap'] = df['Timestamp'].diff().dt.total_seconds()
        df['SuspiciousTime'] = df['TimeGap'] < 60  # Less than 60 seconds apart

    # Mark as Fraudulent if any of the rules are triggered
    df['Fraudulent'] = df['LuhnValid'] & (df['HighAmount'] | df['SuspiciousTime'])
    print("✅ Rule-based detection applied.")
    return df

# Step 4: Fraud Detection & Validation (Anomaly Detection)
def anomaly_detection(df):
    '''
    Uses Isolation Forest for anomaly detection.
    Args:
        df (DataFrame): Transaction data after rule-based detection.
    Returns:
        DataFrame: Data with anomaly scores and predictions.
    '''
    print("🚀 Performing anomaly detection...")
    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)

    # Selecting features for anomaly detection
    features = df[['Amount']] if 'Amount' in df.columns else df
    model.fit(features)

    # Predicting anomalies (-1 is anomaly, 1 is normal)
    df['Anomaly'] = model.predict(features)
    df['Anomaly'] = df['Anomaly'].apply(lambda x: True if x == -1 else False)

    print("✅ Anomaly detection completed.")
    return df

# Step 5: System Deployment - Flask API
app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_fraud():
    data = request.json
    card_number = data.get('CardNumber')
    amount = float(data.get('Amount'))
    
    # Luhn validation
    luhn_valid = luhn_algorithm(card_number)
    
    # Rule-based detection
    high_amount = amount > 1000
    is_fraudulent = luhn_valid and high_amount
    
    response = {
        "CardNumber": card_number,
        "Amount": amount,
        "LuhnValid": luhn_valid,
        "HighAmount": high_amount,
        "Fraudulent": is_fraudulent
    }
    
    return jsonify(response)

if __name__ == "__main__":
    print("🚀 Starting Fraud Detection API...")

    # Updated to handle SystemExit error gracefully
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
""
