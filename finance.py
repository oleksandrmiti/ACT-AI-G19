import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template_string, jsonify, request
import json

app = Flask(__name__)

@app.route('/get_stock_data', methods=['POST'])
def get_stocks():
    data = request.get_json()
    historical_data = {}
    stock_symbols = data.get('array',[])
    # print(stock_symbols)
    stock_symbols = stock_symbols['listSymbols']
    # print(stock_symbols)
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(
            period='1d',
            interval = '1m'
            ).iloc[-1].to_dict()
        # hist['Volume'] = hist.get('Volume') / 1e6 # Convert to millions
        print(hist)
        historical_data[symbol] = hist
    # print(historical_data)
    return jsonify(historical_data)

@app.route('/get_crypto_data',methods=['POST'])
def get_crypto():
    data = request.get_json()
    historical_data = {}
    stock_symbols = data.get('array',[])
    # print(stock_symbols)
    stock_symbols = stock_symbols['listSymbols']
    # print(stock_symbols)
    for symbol in stock_symbols:
        df = yf.download(
            tickers = symbol,
            period = "1d",
            interval = "1m"
            ).iloc[-1]
        dataDict = df.unstack().to_dict()
        dataDict[symbol]['Volume'] = dataDict[symbol]['Volume'] / 1e6  # Convert to millions
        historical_data.update(dataDict)
        # print(historical_data)
        # for stock in hist:
        #     for key in hist[stock]:
        #         historical_data[symbol][stock] = hist[stock][key]
        
    
    return jsonify(historical_data)

@app.route('/api/stocks', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol', 'AAPL')  # Default to AAPL if no symbol is provided
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d')  # Get daily stock data

    if data.empty:
        return jsonify({'error': 'No data found for symbol: ' + symbol}), 404

    return jsonify({
        'symbol': symbol,
        'date': data.index[0].strftime('%Y-%m-%d'),
        'open': float(data['Open'].iloc[0]),  # Convert numpy.float64 to Python float
        'close': float(data['Close'].iloc[0]),
        'high': float(data['High'].iloc[0]),
        'low': float(data['Low'].iloc[0]),
        'volume': int(data['Volume'].iloc[0])  # Convert numpy.int64 to Python int
    })

@app.route('/api/stockGraph', methods = ['POST'])
def gen_graph():
    data = request.get_json()
    symbol = data.get('params', {}).get('symbol')
    
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400
    
    data = yf.download(symbol, period='1d',interval='15m')
    # print(data)
    yData = data['Close']
    print(yData)
    fig = px.line(yData,x=yData.index,y=symbol, title=f'{symbol} Stock Price Over Time')

    graph_html = pio.to_html(fig, full_html=False)
    return jsonify({'graph_html' : graph_html})
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)