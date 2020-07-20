## Web dev basics
Install requirements (ideally in a virtual env)  

`$ python3 -m venv venv`  
`$ source venv/bin/activate`  

`$ pip install -r requirements.txt`


Run example app   
`$ python app.py`

### HTTP requests
- Client/server dichotomy
- Client sends a http **request** to server, server sends a http **response** to the client

- Several HTTP methods, most common are:
	- GET - for retrieving data
	- POST - for submitting data

- When visiting a website, your browser is sending a GET request and recieving a response (with HTML)

- Send HTTP requests from command-line with `curl`
	- e.g. `$ curl https://www.google.ca`
	- `$ curl --help` for more info
	- `$ tldr curl`


- python `requests` library  
```python
import requests
requests.get('https://www.google.ca')
```

- can send text/HTML, json, JS, CSS, and more!

- Common to request data in JSON format
from API **endpoints** (or **routes**)  
	- `$ curl https://jsonplaceholder.typicode.com/posts`

```python
import requests
response = requests.get('https://jsonplaceholder.typicode.com/posts')
posts = response.json()
```

- **Note**: your browser can also fetch and display JSON

### A simple server with Flask
- Server = computer listening for HTTP requests
- Flask is a Python module that abstracts away a lot of boiler plate

```python
from flask import Flask

app = Flask(__app__)

@app.route('/')
def index():
	return 'Hello, world!'
```
- `$ flask run` will look for file named `app.py`
- Change default by setting `FLASK_APP` env variable
- Run in debug mode by setting `FLASK_ENV=development` (restarts server when you make changes)
- Alternativley, to run with `$ python app.py`
```python
if __name__ == '__main__':
	app.run(debug=True)
```

- `$ curl http://localhost:5000` (look at server logs)


#### Allowed methods
```python
@app.route('/submit', methods=['POST'])
def submit():
	return 'Only post allowed!'
```

#### Status codes
https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#2xx_Success
- 200s = success
- 300s = redirect
- 400s = bad request
	- 403 = forbidden
	- 404 = not found
- 500s = server error


#### Handling errors
- Flask auto adds error page for you  
`$ curl http://localhost:5000/another-route`
- Can customize error handling: https://flask.palletsprojects.com/en/1.1.x/errorhandling/
```python
@app.errorhandler(Exception)
def handle_bad_request(e):
	return 'Bad request', 400
```


### Sending data in a request

##### Dynamic routes
```python
@app.route('/hello/<name>', methods=['POST', 'GET'])
def hello_name(name):
	return 'Hello {}'.format{name}
```

#### Query params
- can send data in GET requests in url with query-params (everything following ?)  
https://ca.indeed.com/jobs?q=data+science&l=remote
- accessible through Flask's `request` object

```Python
@app.route('/search', methods=['GET'])
def search():
	args = request.args
	print(args)
	if 'q' not in args:
		return 'Missing query', 400

	return 'You searched for {}'.format(args['q'])
```

#### Request headers
- Header fields: https://en.wikipedia.org/wiki/List_of_HTTP_header_fields
- Metadata for the request
- Can inspect in browser console

```python
import requests
response = requests.get('https://google.com')
dir(response)
response.headers
response.content
```

##### Example with `User-Agent` Header

- SM web app is [SPA](https://en.wikipedia.org/wiki/Single-page_application)  
- single page that is dynamically updated with different content  

`curl https://app.sharpestminds.com/mentor-bio/russell-pollari`  
Normally returns JS

but can listen for user agent and return cached version:  
`curl https://app.sharpestminds.com/mentor-bio/russell-pollari -A googlebot`

-A is short for adding user-agent, could also do  
`curl -H 'User-Agent: googlebot' https://app.sharpestminds.com/mentor-bio/russell-pollari`


#### Sending form data
```python
@app.route('/submit-form', methods=['POST'])
def submit_form():
	data = request.form
	print(data)
	if 'name' not in data:
		return 'Missing name', 400

	if 'email' not in data:
		return 'Missing name', 400

	return 'Your name is {}, your email is {}'.format(data['name'], data['email'])
```

`curl -d "name=russell&email=russell@sharpestminds.com" http://localhost:5000/submit-form`

#### Sending and returning JSON data
```python
@app.route('/submit-json', methods=['POST'])
def submit_json():
	data = request.json
	print(data)
	if 'name' not in data:
		return 'Missing name', 400

	return jsonify({
		'reversed_name': data['name'][::-1],
		'other_data': 'blah blah blah'
	}), 200
```

`curl -d '{"name":"russell"}' -H 'Content-Type: application/json' http://localhost:5000/submit-json`



### HTML
- HTML, header (title, scripts, tags)
- body = what you see
- elements ``<p>, <a>, <table>``
	- attributes `class` `id` `href`

- Flask lets you pass variables to html templates
```python
@app.route('/hello/<name>', methods=['POST', 'GET'])
def hello_name(name):
	return render_template('hello_name.html', name=name)
```

templates/hello_name.html
```HTML
<html>
	<body>
		Hello, {{ name }}
	</body>
<html>
```


### CSS
- `<h3 style="color: green;">`
- Or `<style>` tag in header   
```html
<style>
	h3 { color: green; }
</style>
```
- can use class attribute instead of specific element
```HTML
<h4 class="title" />
```
```html
<style>
	.title { color: red }
</style>
```
- Inspect element and edit styles from browser

- Most common to link to external stylesheet (usually as static asset) `/static/styles.css`
```HTML
  <link rel="stylesheet" href="/static/styles.css">
```
- Can be hosted elsewhere. e.g. [Bootstrap](https://getbootstrap.com/) is good for getting pretty styles out the gate:
```html
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
```
- e.g. style a button
	- https://getbootstrap.com/docs/4.5/components/buttons/#examples
	```html
	<button class="btn btn-primary">
		Submit
	</button>
	```

### JavaScript
- Browsers's have JS compilers
- "event" driven
- can manipulate HTML through [DOM](https://en.wikipedia.org/wiki/Document_Object_Model#Web_browsers)
```HTML
<script>
		function handleButtonClick() {
			alert('You clicked a button!')
		}

		function handleNameChange(value) {
			console.log(value);
			document.getElementById("show-name").innerHTML = value;
		}
</script>
```
```HTML
<input id="name" oninput="handleNameChange(this.value)"></input>
<p id="show-name"></p>
<button class="btn btn-primary" onclick="handleButtonClick()">Submit</button>
```

- usually external script with src attribute
`<script src="/static/script.js"></script>`


### Sending requests from browers

#### Simple form submission
```HTML
<form action="/submit-form" method="POST">
	<input name="name" />
	<button>
		Submit
	</button>
</form>
```

#### AJAX
- Fetch data from server without refreshing page
- AJAX https://www.w3schools.com/js/js_ajax_intro.asp
- `XMLHttpRequest`
- `$.ajax` (jquery) https://api.jquery.com/jquery.ajax/
- new API for Browsers `fetch` https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

e.g. send a request to /submit-json and print the response in the console
```js
fetch('/submit-json', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json'
	},
	body: JSON.stringify({
		'name': 'Russell'
	})
}).then(response => {
	return response.json()
}).then(result => {
	console.log(result);
});
```


### MISC
- many browsers have different features (JS, HTML, CSS), can check availability per
browser  
https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
