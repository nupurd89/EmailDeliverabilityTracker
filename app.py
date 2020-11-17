import flask
from flask import request, jsonify
from gmail import get_emails
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/api/all', methods=['GET'])
def home():
    return jsonify(get_emails(None))

@app.route('/api/search', methods=['GET'])
def api_search():
    query_parameters = request.args
    fromEmail = query_parameters.get('fromEmail')
    return jsonify(get_emails(fromEmail))

app.run()
