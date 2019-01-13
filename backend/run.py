from flask import Flask, render_template, Response, request, jsonify
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

@app.route('/quote')
def last_day_quote():
    if not 'symbol' in request.args:
        return 'Bad request'

    symbol = request.args['symbol']
    return Response(
        requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run()