# Jsonify
UI wrapper for flask's jsonify

[View Demo](https://xzava.github.io/jsonify/demo.html)

## Getting started

```python

# main.py

from flask import Flask
from jsonify import jsonify

app = Flask(__name__)


@app.route("/")
def index_route():
	""" This route does not need authentication or authorization """
	response = {
		"message": "Hello from a index endpoint! You don't need to be authenticated to see this.",
		"endpoints": [
			"http://localhost/api/public",
			"http://localhost/api/private",
			"http://localhost/api/private-scoped",
			"http://localhost/api/optional",
			"http://localhost/api/optional-scoped",
			"http://localhost/api/optional-scoped",
			"http://localhost/api/multi-scoped",
			"http://localhost/api/optional-multi-scoped"
		],
		"access_token": "OIvCoVC02cnNJhbGciww8g0rfHJpyEuNhYGe0_N2IvCoVrfH2c9DXGe_N2r4eySKj9DXfHOq43Xtc3zCi9Q", 
	}
	return jsonify(response)


if __name__ == '__main__':
	# python main.py
	app.run(port=5080, debug=app.debug)


```

## Features:

- Interactive JSON UI
- Respects: `content-type: "application/json"`, ie the html UI is only shown to browsers
- By default will only run when `app.debug` is True. For programmers.
- `export JSONIFY_ALWAYS=1` to run when debug mode is off. For your users.
- If the user agent looks like a browser it will run, if not it will return the json data
- Turn it off by commenting out the import.
