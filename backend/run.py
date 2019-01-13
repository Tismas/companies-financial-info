from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

api_key = '8g327gr4b3t9137t4b'
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
    quote_data = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}').json()
    company_data = requests.get(f'https://autocomplete.clearbit.com/v1/companies/suggest?query={name}').json()
    return jsonify({ 'quote_data': quote_data, 'company_data': company_data })

if __name__ == '__main__':
    app.run()