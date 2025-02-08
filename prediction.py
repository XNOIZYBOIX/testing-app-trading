import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

def get_predictions(symbol, prediction_days=7):
    """Generate predictions using trained LSTM model"""
    try:
        # Load model and data
        model = load_model(f'models/{symbol}_lstm.h5')
        df = pd.read_csv(f'data/{symbol}_historical.csv')
        
        # Preprocess data
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1))
        
        # Create prediction sequence
        lookback = model.input_shape[1]
        seq = scaled_data[-lookback:]
        predictions = []
        
        # Generate predictions
        for _ in range(prediction_days):
            pred = model.predict(seq.reshape(1, lookback, 1))
            predictions.append(pred[0][0])
            seq = np.append(seq[1:], pred)
            
        # Inverse transform predictions
        return scaler.inverse_transform(np.array(predictions).reshape(-1,1))
    
    except Exception as e:
        raise ValueError(f"Prediction failed for {symbol}: {str(e)}")