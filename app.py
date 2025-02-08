from flask import Flask, render_template, request, jsonify
import data_retrieval
import model_training
import prediction
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    stock_symbol = request.form['symbol']
    period = request.form.get('period', '1mo')
    
    try:
        historical_data = data_retrieval.get_historical_data(stock_symbol, period)
        latest_price = data_retrieval.get_real_time_price(stock_symbol)
        return jsonify({
            'historical': historical_data.to_dict(orient='records'),
            'latest_price': latest_price,
            'symbol': stock_symbol
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train_model', methods=['POST'])
def train_model():
    stock_symbol = request.form['symbol']
    lookback_days = int(request.form.get('lookback', 60))
    
    try:
        model_path = model_training.train_lstm_model(stock_symbol, lookback_days)
        return jsonify({'message': f'Model trained successfully: {model_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    stock_symbol = request.form['symbol']
    prediction_days = int(request.form.get('days', 7))
    
    try:
        predictions = prediction.get_predictions(stock_symbol, prediction_days)
        return jsonify({
            'predictions': predictions.tolist(),
            'symbol': stock_symbol
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
