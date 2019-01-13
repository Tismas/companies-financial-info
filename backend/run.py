from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import requests

api_key = 'TA12U6P8JPBF71G2'
app = Flask(__name__, template_folder='../front/build', static_folder='../front/build/static', static_url_path='/static')
CORS(app)

def symbols_mapper(symbol_obj):
    result = {}
    for key in symbol_obj:
        new_key = key.split()[-1]
        result[new_key] = symbol_obj[key]
    return result

def preprocess_name(name):
    name = [part for part in name.split() if not '.' in part]
    return '_'.join(name)

def save_daily_data(symbol):
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS quotes (symbol text, date text, open real, high real, low real, close real, volume real)')

    quotes = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}').json()
    if 'Time Series (Daily)' not in quotes:
        return
    quotes = quotes['Time Series (Daily)']
    for date in quotes:
        c.execute(f'SELECT date FROM quotes WHERE symbol=? AND date=?', [symbol, date])
        if not c.fetchone():
            values = quotes[date]
            c.execute(f"INSERT INTO quotes VALUES (?,?,?,?,?,?,?)", 
                [symbol, date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. volume']]
            )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols')
def symbols_autocomplete():
    if not 'symbol' in request.args:
        return 'Bad request'

    symbol = request.args['symbol']
    symbols = requests.get(f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}').json()
    if not 'bestMatches' in symbols:
        return jsonify({ 'bestMatches': [] })
    symbols['bestMatches'] = [symbols_mapper(symbol) for symbol in symbols['bestMatches']]
    return jsonify(symbols)

@app.route('/company')
def company_data():
    if 'name' not in request.args or 'symbol' not in request.args:
        return 'Bad request'

    name = preprocess_name(request.args['name'])
    symbol = request.args['symbol']
    quote_data = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}').json()['Time Series (5min)']
    company_data = requests.get(f'https://autocomplete.clearbit.com/v1/companies/suggest?query={name}').json()
    save_daily_data(symbol)
    return jsonify({ 'quote_data': quote_data, 'company_data': company_data })

if __name__ == '__main__':
    app.run()