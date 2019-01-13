from flask import Flask, render_template, Response, request, jsonify
import requests

api_key = '8g327gr4b3t9137t4b'
app = Flask(__name__, template_folder='../front/build', static_folder='../front/build/static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols')
def symbols_autocomplete():
    if not 'symbol' in request.args:
        return 'Bad request'

    symbol = request.args['symbol']
    return Response(
        requests.get(f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}'),
        mimetype='application/json'
    )

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