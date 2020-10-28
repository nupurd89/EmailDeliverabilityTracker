import flask
from flask import request, jsonify
from gmail import get_labels
from gmail import find_email
from gmail import get_emails_search
from gmail import find_specific_list
from gmail import get_emails_all

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
emails= [
		{
			'sender': "luciano@xxxxxxxx.com",
			'subjectLine': "test emails",
			'labels': ["inbox", "updates"],
			'arrivalTime': "10/12/2020 5:43 PM PST"
		},
		{
			'sender': "rob@xxxxxxxx.com",
			'subjectLine': "foo test emails",
			'labels': ["inbox", "updates"],
			'arrivalTime': "10/12/2020 6:43 PM PST"
		},
	]

def get_emails(fromEmail):
	return get_emails_search(fromEmail)

@app.route('/api/all', methods=['GET'])
def home():
    get_emails_all()
    return jsonify(get_emails_all())

@app.route('/api/search', methods=['GET'])
def api_search():
    query_parameters = request.args

    fromEmail = query_parameters.get('fromEmail')
    return jsonify(get_emails(fromEmail))

app.run()
