# Jsonify
UI wrapper for flask's jsonify

[View Demo](https://xzava.github.io/jsonify/demo.html)

Jsonify is a drop in replacement for `flask.jsonify`;
- Only browsers will get the HTML page everyone else will get a normal `flask.jsonify` JSON response.
- UI requires no imports. Pure Javascript.

<img src="https://xzava.github.io/jsonify/jsonify.png"></img>

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
	  "data": {
	    "id": 1001,
	    "type": "donut",
	    "name": "Cake",
	    "description": "https://en.wikipedia.org/wiki/Doughnut",
	    "price": 2.55,
	    "price2": true,
	    "available":
	    {
	      "store": 42,
	      "warehouse2": 600,
	      "warehouse": null
	    },
	    "toppings": [
	    {
	      "id": 5001,
	      "type": "None"
	    },
	    {
	      "id": 5002,
	      "type": "Glazed"
	    },
	    {
	      "id": 5005,
	      "type": "Sugar"
	    },
	    {
	      "id": 5003,
	      "type": "Chocolate"
	    },
	    {
	      "id": 5004,
	      "type": "Maple"
	    }],
	    "uuids": [
	      "826b23ce-2669-4122-981f-3e2e4429159d",
	      "e32111a0-6a87-49ab-b58f-a01bf8d28ba0",
	      "c055a894-698e-41c0-b85f-7510a7351d9d",
	      "c055a894-698e-41c0-b85f-7510a7351d9d",
	      "c055a894-698e-41c0-b85f-7510a7351d9d",
	      "c055a894-698e-41c0-b85f-7510a7351d9d",
	      "c055a894-698e-41c0-b85f-7510a7351d9d",
	      "c055a894-698e-41c0-b85f-7510a7351d9d"
	    ]
	  }
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


Try it out, Star it if you like it.



## See Also:
Inspiration from this jquery plugin - with all the jquery removed, styles improved and buttons added, and connected with flask
Inspiration also from firefox nightly, they apply a similar UI to json by default.

- [jquery.json-viewer](https://github.com/abodelot/jquery.json-viewer)


## Donate:

Making this free and useful is the right thing to do. Consider donating if you find this as useful as I do. 

[<td style="text-align:center"> <img alt="Buymeacoffee logo" src="https://ci5.googleusercontent.com/proxy/bUcfJu5843uyZkufO2ah5B0cSK9zAEiPrnrMmAIrGgdi6Y2nS4VMINilrSPkWV4_wSOkz5kiWzk82Odgt4yAOLQ5zez5BiqBun0PORk6uyTFgx2tLYLMkQfZ=s0-d-e1-ft#https://cdn.buymeacoffee.com/assets/img/email-template/bmc-new-logo.png" style="max-width:100%;width:200px" class="CToWUd"> </td>](https://www.buymeacoffee.com/kaurifund)

