# Jsonify
UI wrapper for flask's jsonify

[View Demo](https://xzava.github.io/jsonify/demo.html)

Jsonify is a drop in replacement for `flask.jsonify`;
- Only browsers will get the HTML page everyone else will get a normal `flask.jsonify` JSON response.
- UI requires no imports. Pure Javascript.

### before..
<img src="https://xzava.github.io/jsonify/jsonify-before.png"></img>

### after..
<img src="https://xzava.github.io/jsonify/jsonify3.png"></img>

## Installation

```bash
# from github
pip install git+https://github.com/xzava/jsonify.git --upgrade

# from pypi.org (Coming soon)
# pip install jsonify

# or for development
git clone https://github.com/xzava/jsonify.git
cd jsonify
python setup.py develop
```

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
		"price2": True,
		"available":
		{
		  "store": 42,
		  "warehouse2": 600,
		  "warehouse": None
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

### Hideable buttons

<img src="https://xzava.github.io/jsonify/jsonify-buttons3.png"></img>

### HTML response is only for browsers

<img src="https://xzava.github.io/jsonify/jsonify-curl.png"></img>

## Features:

- Interactive JSON UI
- Respects: `content-type: "application/json"`, ie the HTML UI is only shown to browsers
- By default will only run when `app.debug` is True. For programmers.
- `export JSONIFY_ALWAYS=1` to run when debug mode is off. For your users.
- If the user agent looks like a browser it will run, if not it will return the json data
- Turn it off by commenting out the import.


Try it out, Star it if you like it.



## See Also:
> Inspiration from this jquery plugin - with all the jquery removed, styles improved and buttons added, and connected with flask
- [jquery.json-viewer](https://github.com/abodelot/jquery.json-viewer)
> Inspiration also from firefox nightly, they apply a similar UI for json by default.




## Donate:

Making this free and useful is the right thing to do. Consider donating if you find this as useful as I do. 

[<td style="text-align:center"> <img alt="Buymeacoffee logo" src="https://ci5.googleusercontent.com/proxy/bUcfJu5843uyZkufO2ah5B0cSK9zAEiPrnrMmAIrGgdi6Y2nS4VMINilrSPkWV4_wSOkz5kiWzk82Odgt4yAOLQ5zez5BiqBun0PORk6uyTFgx2tLYLMkQfZ=s0-d-e1-ft#https://cdn.buymeacoffee.com/assets/img/email-template/bmc-new-logo.png" style="max-width:100%;width:200px" class="CToWUd"> </td>](https://www.buymeacoffee.com/kaurifund)


## Details for nerds.

Question: How does jsonify know if it should render the HTML or send the JSON response


- Check one: Is the request coming from a user-agent with anything remotely browser in the string?
> Send HTML.

ie

```python
is_broswer = any(e in request.headers['User-Agent'].lower() for e in {"mozilla", "linux", "apple", "gecko", "chrome", "safari", "firefox", "iphone", "opera", "android"})
```


- Check two: Does the headers have a `Content-Type: application/json` - This header is respected and JSON will always be returned.
> Send JSON.

ie

```python
requesting_json = request.headers.get("Content-Type") == "application/json"
```


Suggestions on how to improve detection are welcome.

Its written in this way so a javascript Fetch() from the browser will always return JSON data, if they include `Content-Type: application/json` which is normally the case.
> Return JSON

ie The following javascript will return JSON to this request but HTML to a human page reload.


```js

	async function getData(url='', data={}) {
	  // Default options are marked with *
	  const response = await fetch(url, {
	    method: 'GET', // *GET, POST, PUT, DELETE, etc.
	    mode: 'cors', // no-cors, *cors, same-origin
	    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
	    credentials: 'same-origin', // include, *same-origin, omit
	    headers: {
	      'Content-Type': 'application/json'
	      // 'Content-Type': 'application/x-www-form-urlencoded',
	    },
	    redirect: 'follow', // manual, *follow, error
	    referrerPolicy: 'no-referrer' // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
	    // body: JSON.stringify(data) // body data type must match "Content-Type" header
	  });
	  console.log(response);
	  return response.json(); // parses JSON response into native JavaScript objects
	}

	const data = await getData("http://127.0.0.1:5052/");


```

If for some reason you need to send a fetch/ajax request from the browser and you need to specify a particular `Content-Type` that is not `application/json`.

Then make a pull request for a custom HTTP header `X-jsonify: application/json`, I'll be happy to view the PR.