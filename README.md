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

app.debug = True

@app.route("/")
def index_route():
	""" This route does not need authentication or authorization """
	data = {
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
	return jsonify(data)


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


## Details for nerds:

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

It's written in this way so a javascript Fetch() from the browser will always return JSON data, if they include `Content-Type: application/json` which is normally the case.
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

Then make a pull request for a custom HTTP header `X-jsonify: application/json`, I'll be happy to review the PR.