from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__, template_folder='../front/build', static_folder='../front/build/static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols')
def symbols_autocomplete():
    return jsonify(['Facebook', 'Google'])

@app.route('/quote')
def last_day_quote():
    return jsonify({'test': 'test'})

if __name__ == '__main__':
    app.run()