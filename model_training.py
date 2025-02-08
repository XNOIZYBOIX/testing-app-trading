import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import os

def preprocess_data(stock_data, lookback=60):
    """Preprocess data for LSTM model"""
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(stock_data['Close'].values.reshape(-1,1))
    
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i, 0])
        y.append(scaled_data[i, 0])
    
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    """Build and compile LSTM model"""
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm_model(symbol, lookback_days=60, epochs=25):
    """Train and save LSTM model"""
    # Load and preprocess data
    df = pd.read_csv(f'data/{symbol}_historical.csv')
    X, y, scaler = preprocess_data(df, lookback_days)
    
    # Reshape data for LSTM
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    # Build and train model
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=epochs, batch_size=32)
    
    # Save model
    model_path = f'models/{symbol}_lstm.h5'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    return model_path
