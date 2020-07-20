from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/hello/<name>', methods=['POST', 'GET'])
def hello_name(name):
	return render_template('hello_name.html', name=name)


@app.route('/search', methods=['GET'])
def search():
	"Example getting query parameters"
	args = request.args
	if 'q' not in args:
		return 'Missing query', 400

	return 'You searched for {}'.format(args['q'])


@app.route('/submit-form', methods=['POST'])
def submit_form():
	"Example getting form data"
	data = request.form

	if 'name' not in data.keys():
		return 'Missing name', 400

	if 'email' not in data:
		return 'Missing name', 400

	return 'Your name is {}, your email is {}'.format(data['name'], data['email'])


@app.route('/submit-json', methods=['POST'])
def submit_json():
	"Getting JSOn data"
	data = request.json
	if 'name' not in data.keys():
		return 'Missing name', 400


	return jsonify({
		'reversed_name': data['name'][::-1],
		'other_data': 'blah blah blah'
	}), 200


@app.errorhandler(Exception)
def handle_bad_request(e):
	return 'bad request', 400


if __name__ == '__main__':
	app.run(debug=True)
