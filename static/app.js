async function loadStockData() {
    const symbol = document.getElementById('symbol').value;
    if (!symbol) return;

    showStatus('Loading stock data...');
    try {
        const response = await fetch('/get_stock_data', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `symbol=${encodeURIComponent(symbol)}`
        });
        
        const data = await response.json();
        if (data.error) throw data.error;
        
        plotChart(data.historical, data.latest_price, symbol);
        showStatus('Data loaded successfully');
    } catch (error) {
        showStatus(`Error: ${error}`);
    }
}

async function trainModel() {
    const symbol = document.getElementById('symbol').value;
    const lookback = document.getElementById('lookback').value;
    
    if (!symbol) return;

    showStatus('Training model...');
    try {
        const response = await fetch('/train_model', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `symbol=${encodeURIComponent(symbol)}&lookback=${lookback}`
        });
        
        const result = await response.json();
        if (result.error) throw result.error;
        
        showStatus(result.message);
    } catch (error) {
        showStatus(`Training failed: ${error}`);
    }
}

async function getPredictions() {
    const symbol = document.getElementById('symbol').value;
    const predDays = document.getElementById('predDays').value;
    
    if (!symbol) return;

    showStatus('Generating predictions...');
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `symbol=${encodeURIComponent(symbol)}&days=${predDays}`
        });
        
        const data = await response.json();
        if (data.error) throw data.error;
        
        addPredictionsToChart(data.predictions);
        showStatus(`Predicted next ${predDays} days`);
    } catch (error) {
        showStatus(`Prediction failed: ${error}`);
    }
}

function plotChart(historicalData, latestPrice, symbol) {
    const dates = historicalData.map(d => d.Date);
    const closes = historicalData.map(d => d.Close);
    
    const trace = {
        x: dates,
        y: closes,
        type: 'scatter',
        name: 'Historical'
    };
    
    const layout = {
        title: `${symbol} Stock Price`,
        showlegend: true
    };
    
    Plotly.newPlot('chart', [trace], layout);
}

function addPredictionsToChart(predictions) {
    const chartDiv = document.getElementById('chart');
    const newDates = Array.from({length: predictions.length}, (_,i) => 
        new Date(Date.now() + (i+1)*86400000).toISOString().split('T')[0]
    );
    
    const trace = {
        x: newDates,
        y: predictions,
        type: 'scatter',
        name: 'Predicted',
        line: {color: 'orange', dash: 'dot'}
    };
    
    Plotly.addTraces(chartDiv, trace);
}

function showStatus(message) {
    document.getElementById('status').textContent = message;
    setTimeout(() => {
        document.getElementById('status').textContent = '';
    }, 5000);
}
