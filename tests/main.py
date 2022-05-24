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
		"access_token": "eyJhbGciOC02cnNuNhY4ww8g0rfHJpyESKj9DXGe0_N2IvCoVrfH2c9DXGe_N2IvCoVrfHOq43Xtc3zCi9Q", 
	}
	return jsonify(response)


if __name__ == '__main__':
	# python tests/main.py
	app.run(port=5080, debug=app.debug)