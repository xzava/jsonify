""" Add interactive UI to json output by overriding flask.jsonify

    Will attempt to turn off when a non human user is detected.

    - Turns on when debug mode is True
    - Turns off when a request comes from a user agent that does not look like a browser
    - Turns off if 'Content-Type': 'application/json' ie from javascript


    TODO: minimize the html payload
    TODO: Fix css for line breaks, currently overflow is scroll when it should break if possible.
          - Use white-space: pre-wrap; but I'm unsure if this looks better or not..
          - firefox's version reduces long strings with "longstring...longstrong" with a toggle
    TODO: check this still works when importing from pip
    
    TODO [optional]: add a pop up for session, headers, cookies

    TODO: Test how it works with custom json encoders, as json is the flask version

    USEAGE:
        from flask import Flask
        from jsonify import jsonify
        app = Flask(__name__)


    INSPIRED BY: https://github.com/abodelot/jquery.json-viewer

    FireFox does something similar by default:
     - they allow you to condense long strings
     - they allow you to filter json
     - They allow you to prettyprint the raw json - should already do this with flask

     Other feature are already shared. 
     Of the non shared features save as a file should be included

"""

import typing as t
from os import getenv

from flask import current_app, request, json, render_template, render_template_string


def jsonify(*args: t.Any, **kwargs: t.Any):
    """ UI for interactive json - for human users.

    Wrapper for flask.jsonify

    Features:
        - Respects: content-type: "application/json"
        - by default will only run in debug mode.
        - `export JSONIFY_ALWAYS=1` to run when debug mode is off.
        - If the user agent looks like a browser it will run

    ORIGINAL DOC STRING
    ===================
    Serialize data to JSON and wrap it in a :class:`~flask.Response`
    with the :mimetype:`application/json` mimetype.
    Uses :func:`dumps` to serialize the data, but ``args`` and
    ``kwargs`` are treated as data rather than arguments to
    :func:`json.dumps`.
    1.  Single argument: Treated as a single value.
    2.  Multiple arguments: Treated as a list of values.
        ``jsonify(1, 2, 3)`` is the same as ``jsonify([1, 2, 3])``.
    3.  Keyword arguments: Treated as a dict of values.
        ``jsonify(data=data, errors=errors)`` is the same as
        ``jsonify({"data": data, "errors": errors})``.
    4.  Passing both arguments and keyword arguments is not allowed as
        it's not clear what should happen.
    .. code-block:: python
        from flask import jsonify
        @app.route("/users/me")
        def get_current_user():
            return jsonify(
                username=g.user.username,
                email=g.user.email,
                id=g.user.id,
            )
    Will return a JSON response like this:
    .. code-block:: javascript
        {
          "username": "admin",
          "email": "admin@localhost",
          "id": 42
        }
    The default output omits indents and spaces after separators. In
    debug mode or if :data:`JSONIFY_PRETTYPRINT_REGULAR` is ``True``,
    the output will be formatted to be easier to read.
    .. versionchanged:: 2.0.2
        :class:`decimal.Decimal` is supported by converting to a string.
    .. versionchanged:: 0.11
        Added support for serializing top-level arrays. This introduces
        a security risk in ancient browsers. See :ref:`security-json`.
    .. versionadded:: 0.2
    """
    indent = None
    separators = (",", ":")

    if current_app.config["JSONIFY_PRETTYPRINT_REGULAR"] or current_app.debug:
        indent = 2
        separators = (", ", ": ")

    if args and kwargs:
        raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    # "##############################"
    # "#   JSONFIY OVERRIDE  START  #"
    # "##############################"
    always_on = current_app.config.get("JSONIFY_ALWAYS") or getenv("JSONIFY_ALWAYS", "").lower() == "1" # pending feature: will run when debug mode is both True and False
    content_type = request.headers.get("Content-Type") # application/json
    is_broswer = any(e in request.headers.get('User-Agent', '').lower() for e in {"mozilla", "linux", "apple", "gecko", "chrome", "safari", "firefox", "iphone", "opera", "android"})
    force_json = request.headers.get("X-jsonify") == "application/json"
    
    if current_app.debug and getenv("JSONIFY_VERBOSE", "").lower() == "1":
      print("JSONIFY DEBUG")
      print("#############")
      print("current_app.debug :", current_app.debug)
      print("always_on :", always_on, type(always_on))
      print("JSONIFY_ALWAYS :", bool(getenv("JSONIFY_ALWAYS")), type(bool(getenv("JSONIFY_ALWAYS"))))
      print("content_type :", content_type)
      print("is_broswer :", is_broswer)
      print("")
      print("request.headers :", request.headers)
      print("")
      print("data :", data)
      print("")
      print("")


    if content_type != "application/json" and (always_on or current_app.debug) and is_broswer is True:
        # This will fail in the same way normal jsonify fails - when json.dump can not serialize a object within the dict
        # print("Returning Jsonify UI")
        # return render_template("jsonify.html", data=json.dumps(data, indent=indent, separators=separators))
        html_string = render_template_string(JSONIFY_TEMPLATE_STRING, data=f"{json.dumps(data, indent=indent, separators=separators)}\n")
        return current_app.response_class(f"{html_string}\n", mimetype="text/html")

    # if content_type != "application/json" and (always_on or current_app.debug == False) and is_broswer is True:
        # This will fail in the same way normal jsonify fails - when json.dump can not serialize a object within the dict
        # print("Returning Jsonify UI")
        # return render_template("jsonify.html", data=json.dumps(data, indent=indent, separators=separators))
        # return render_template_string(JSONIFY_TEMPLATE_STRING, data=json.dumps(data, indent=indent, separators=separators))

    # print("Returning Normal JSON")
    # "##############################"
    # "#   JSONFIY OVERRIDE  END    #"
    # "##############################"

    return current_app.response_class(
        f"{json.dumps(data, indent=indent, separators=separators)}\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )


JSONIFY_TEMPLATE_STRING = r"""<!doctype HTML>
<html lang="en">
<head>
    <title>Jsonify</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
      .json-editor-blackbord {
          background: #1c2833;
          color: #fff;
          font-size: 13px;
          font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
      }
      ul.json-dict.collapsed,
      ol.json-array.collapsed {
          display: none;
      }

      a.json-placeholder {
          color: #aaa;
          padding: 0 0.5em;
          text-decoration: none;
          cursor: pointer;
      }

      /* Root element */
      .json-document {
          padding: 1em 2em;
      }

      /* Syntax highlighting for JSON objects */
      ul.json-dict,
      ol.json-array {
          list-style-type: none;
          margin: 0 0 0 1px;
          border-left: 1px dotted #ccc;
          padding-left: 2em;
      }

      .json-string {
          color: #0B7500;
      }

      .json-literal {
          color: #1A01CC;
          font-weight: bold;
      }

      /* Toggle button */
      a.json-toggle {
          position: relative;
          color: inherit;
          text-decoration: none;
      }

      a.json-toggle:focus {
          outline: none;
      }

      a.json-toggle:before {
          font-size: 1.1em;
          color: #c0c0c0;
          content: "\25BC";
          /* down arrow */
          position: absolute;
          display: inline-block;
          width: 1em;
          text-align: center;
          line-height: 1em;
          left: -1.2em;
      }

      a.json-toggle:hover:before {
          color: #aaa;
      }

      a.json-toggle.collapsed:before {
          /* Use rotated down arrow, prevents right arrow appearing smaller than down arrow in some browsers */
          transform: rotate(-90deg);
      }

      /* Collapsable placeholder links */
      a.json-placeholder {
          color: #aaa;
          padding: 0 1em;
          text-decoration: none;
          font-size: 95%
      }

      a.json-placeholder:hover {
          text-decoration: underline;
      }

      body {
          margin: 0 100px;
          font-family: sans-serif;
      }

      p.options label {
          margin-right: 10px;
      }

      p.options input[type=checkbox] {
          vertical-align: middle;
      }

      textarea#json-input {
          width: 100%;
          height: 200px;
      }

      pre#json-renderer {
          border: 1px solid #aaa;
          overflow-x: scroll;
      }

      body {
          margin: 0;
          padding: 0;
          width: 80%;
          margin: 50px auto 100px;
      }

      #json-input {
          display: block;
          width: 100%;
          height: 200px;
      }

      #translate {
          display: block;
          height: 28px;
          margin: 20px 0;
          border-radius: 3px;
          border: 2px solid;
          cursor: pointer;
      }

      #json-display {
          border: 1px solid #000;
          margin: 0;
          padding: 10px 20px;
      }

      /* Syntax highlighting for JSON objects */
      .json-editor-blackbord {
          background: #1c2833;
          color: #fff;
          font-size: 13px;
          font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
      }

      @media screen and (min-width: 1600px) {
          .json-editor-blackbord {
              font-size: 14px;
          }
      }

      ul.json-dict,
      ol.json-array {
          list-style-type: none;
          margin: 0 0 0 1px;
          border-left: 1px dotted #525252;
          padding-left: 2em;
      }

      .json-string {
          /*color: #0B7500;*/
          /*color: #BCCB86;*/
          color: #0ad161;
      }

      .json-literal {
          /*color: #1A01CC;*/
          /*font-weight: bold;*/
          color: #ff8c00;
      }

      .json-url {
          color: #1e90ff;
      }

      .json-property {
          color: #4fdee5;
          line-height: 160%;
          font-weight: 500;
      }

      /* Toggle button */
      a.json-toggle {
          position: relative;
          color: inherit;
          text-decoration: none;
          cursor: pointer;
      }

      a.json-toggle:focus {
          outline: none;
      }

      a.json-toggle:before {
          color: #aaa;
          content: "\25BC";
          /* down arrow */
          position: absolute;
          display: inline-block;
          width: 1em;
          left: -1em;
      }

      a.json-toggle.collapsed:before {
          transform: rotate(-90deg);
          /* Use rotated down arrow, prevents right arrow appearing smaller than down arrow in some browsers */
          -ms-transform: rotate(-90deg);
          -webkit-transform: rotate(-90deg);
      }

      /* Collapsable placeholder links */
      a.json-placeholder {
          color: #aaa;
          padding: 0 1em;
          text-decoration: none;
      }

      a.json-placeholder:hover {
          text-decoration: underline;
      }

      li {
          color: #4fdee5;
          line-height: 140%;
          font-weight: 500;
      }

      .json-literal {
          /* color: #1A01CC; */
          font-weight: normal;
          color: #ff8c00;
      }

      a.json-toggle:before {
          color: #aaa;
          content: "\25BC";
          position: absolute;
          display: inline-block;
          width: 0.6em;
          left: -1em;
          margin-top: 1.3px;
      }

      /*a.collapsed::before {
          margin-top: 0px!important
         }*/

      a.json-toggle.collapsed:before {
          margin-top: 1px !important
      }

      .json-array li {
          line-height: 130%;
      }

      /*#json-renderer > ul > li:nth-child(6) > ul*/
      li ul li {
          line-height: 130%;
      }
    </style>
    <style type="text/css">
      body {
          margin: 0;
          padding: 0;
          /* width: 80%; */
          margin: 50px auto 100px;
      }

      .full-screen {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          top: 0;
          margin: 0;
      }



      span.json-string {
          color: #fbff9f
      }

      a.json-string {
          color: #56acff;
      }

      .json-literal {
          /* color: #1A01CC; */
          font-weight: normal;
          color: #ae9ced;
      }

      .hidden {
          display: none !important;
      }

      .json-bool {
          color: #ff4b60
      }

      .json-null {
          color: #ff4b60
      }

      textarea#json-input {
          position: absolute;
          top: 0;
          bottom: 0;
          left: 0;
          right: 0;
          height: 100vh;
          padding: 2em;
          padding-top: 3em;
          border: none;
      }

      #json-renderer::-webkit-scrollbar-track
      {
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
        border-radius: 10px;
        background-color: #1c2833;
      }

      #json-renderer::-webkit-scrollbar
      {
        width: 10px;
        height: 8px;
        background-color: #1c2833;
      }

      #json-renderer::-webkit-scrollbar-thumb
      {
        border-radius: 6px;
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
        background-color: #555;
      }

      /* @media.smaller Extra small devices (phones, 600px and down) */
      @media only screen and (max-width: 600px) {
          ul.json-dict,
          ol.json-array {
              padding-left: 1.4em;
          }

          a.json-toggle:before {
              /* display: none; */
          } 

          a.json-toggle:hover:before {
              color: #1c2833;
          }
      }
    </style>
    <script type="text/javascript">
      /**
       * json-viewer - vanilla JS
       * @based on: https://github.com/abodelot/jquery.json-viewer
       */
      (function() {
          /**
           * Check if arg is either an array with at least 1 element, or a dict with at least 1 key
           * @return boolean
           * reference: https://github.com/abodelot/jquery.json-viewer
           */
          function isCollapsable(arg) {
              return arg instanceof Object && Object.keys(arg).length > 0;
          }

          /**
           * Check if a string looks like a URL, based on protocol
           * This doesn't attempt to validate URLs, there's no use and syntax can be too complex
           * @return boolean
           * reference: https://github.com/abodelot/jquery.json-viewer
           */
          function isUrl(string) {
              var protocols = ['http', 'https', 'ftp', 'ftps'];
              for (var i = 0; i < protocols.length; ++i) {
                  if (string.startsWith(protocols[i] + '://')) {
                      return true;
                  }
              }
              return false;
          }

          /**
           * Return the input string html escaped
           * @return string
           * reference: https://github.com/abodelot/jquery.json-viewer
           */
          function htmlEscape(s) {
              return s.replace(/&/g, '&amp;')
                  .replace(/</g, '&lt;')
                  .replace(/>/g, '&gt;')
                  .replace(/'/g, '&apos;')
                  .replace(/"/g, '&quot;');
          }

          /**
           * insert a HTML Element after a reference HTML Element
           * @return null
           * reference: 
           */
          function insertAfter(referenceNode, newNode) {
              referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
          }

          /**
           * Transform a json object into html representation
           * @return string
           * reference: https://github.com/abodelot/jquery.json-viewer
           */
          function json2html(json, options) {
              var html = '';
              if (typeof json === 'string') {
                  // Escape tags and quotes
                  json = htmlEscape(json);

                  if (options.withLinks && isUrl(json)) {
                      // TODO: Add more regex for removing local url, inc port :5000/example/example --> /example/example
                      let jsonRemoveLocalUrl = json.replace(/^(http:\/\/localhost)/, "").replace(/^(http:\/\/127\.0\.0\.1)/, "")
                      // console.log(jsonRemoveLocalUrl)
                      html += '<a href="' + jsonRemoveLocalUrl + '" class="json-string" target="_blank" rel="noreferrer noopener">' + jsonRemoveLocalUrl + '</a>';
                  } else {
                      // Escape double quotes in the rendered non-URL string.
                      json = json.replace(/&quot;/g, '\\&quot;');
                      html += '<span class="json-string">"' + json + '"</span>';
                  }
              } else if (typeof json === 'number' || typeof json === 'bigint') {
                  html += '<span class="json-literal">' + json + '</span>';
              } else if (typeof json === 'boolean') {
                  html += '<span class="json-literal json-bool">' + json + '</span>';
              } else if (json === null) {
                  html += '<span class="json-literal json-null">null</span>';
              } else if (json instanceof Array) {
                  if (json.length > 0) {
                      html += '[<ol class="json-array">';
                      for (var i = 0; i < json.length; ++i) {
                          html += '<li>';
                          // Add toggle button if item is collapsable
                          if (isCollapsable(json[i])) {
                              html += '<a href class="json-toggle"></a>';
                          }
                          html += json2html(json[i], options);
                          // Add comma if item is not last
                          if (i < json.length - 1) {
                              html += ',';
                          }
                          html += '</li>';
                      }
                      html += '</ol>]';
                  } else {
                      html += '[]';
                  }
              } else if (typeof json === 'object') {
                  // Optional support different libraries for big numbers
                  // json.isLosslessNumber: package lossless-json
                  // json.toExponential(): packages bignumber.js, big.js, decimal.js, decimal.js-light, others?
                  if (options.bigNumbers && (typeof json.toExponential === 'function' || json.isLosslessNumber)) {
                      html += '<span class="json-literal">' + json.toString() + '</span>';
                  } else {
                      var keyCount = Object.keys(json).length;
                      if (keyCount > 0) {
                          html += '{<ul class="json-dict">';
                          for (var key in json) {
                              if (Object.prototype.hasOwnProperty.call(json, key)) {
                                  key = htmlEscape(key);
                                  var keyRepr = options.withQuotes ?
                                      '<span class="json-string">"' + key + '"</span>' : key;

                                  html += '<li>';
                                  // Add toggle button if item is collapsable
                                  if (isCollapsable(json[key])) {
                                      html += '<a href class="json-toggle">' + keyRepr + '</a>';
                                  } else {
                                      html += keyRepr;
                                  }
                                  html += ': ' + json2html(json[key], options);
                                  // Add comma if item is not last
                                  if (--keyCount > 0) {
                                      html += ',';
                                  }
                                  html += '</li>';
                              }
                          }
                          html += '</ul>}';
                      } else {
                          html += '{}';
                      }
                  }
              }
              return html;
          }

          /**
           * @param json: a javascript object
           * @param options: an optional options hash
           */
          jsonViewer = function(json, options) {
              // Merge user options with default options
              options = Object.assign({}, {
                  collapsed: false,
                  rootCollapsable: true,
                  withQuotes: false,
                  withLinks: true,
                  bigNumbers: false
              }, options);

              // Transform to HTML
              let html = json2html(json, options);
              if (options.rootCollapsable && isCollapsable(json)) {
                  html = '<a href class="json-toggle"></a>' + html;
              }

              // Add html json display
              let element = document.querySelector("pre#json-renderer")
              element.innerHTML = html
              element.classList.add('json-document')

              // Bind click on toggle buttons
              Array.from(element.querySelectorAll('a.json-toggle')).map(e => {
                  e.addEventListener('click', function(event) {
                      event.preventDefault();

                      // Array.from(e.parentElement.querySelectorAll('ul.json-dict')).map( (ee) => {ee.classList.toggle('collapsed')})
                      // Array.from(e.parentElement.querySelectorAll('ol.json-array')).map( (ee) => {ee.classList.toggle('collapsed')})

                      let target = e.nextElementSibling
                      target.classList.toggle('collapsed')
                      e.classList.toggle('collapsed')

                      target.style.display

                      if (!target.classList.contains('collapsed')) {
                          // Remove placeholder
                          target.nextElementSibling.remove();
                      } else {
                          // Add Placeholder
                          let count = target.children.length;
                          let placeholder = count + (count > 1 ? ' items' : ' item');

                          a_tag = document.createElement('a')
                          a_tag.innerText = placeholder
                          a_tag.setAttribute('class', 'json-placeholder')
                          a_tag.setAttribute('onclick', 'this.previousElementSibling.previousElementSibling.click()')

                          insertAfter(target, a_tag)
                      }
                      return false;

                  })

              });
          };
      })();
    </script>
</head>
<body ondragstart="return false;" ondrop="return false;">
    <section>
        <style type="text/css">
          .infoToggle {
              background-color: #026343;
              color: white;
              font-weight: bold;
              margin-left: 0.2em;
              margin-right: 0.2em;
          }

          .infoToggle.closed {
              background-color: #7d0a0a;
              color: white;
              font-weight: bold;
              margin-left: 0.3em;
              margin-right: 0.3em;
          }



          /* @media.smaller Extra small devices (phones, 600px and down) */
          @media only screen and (max-width: 600px) {
              #helpButtons {
                  position: absolute;
                  z-index: 100;
                  right: 5px;
                  top: 10px;
                  display: block;
                  display: flex;
                  user-select: none;
                  -moz-user-select: none;
                  max-width: 50%;
                  align-items: baseline;
              }

              #infoButton {
                display: flex;
                flex-direction: column-reverse;
              }

              #infoToggle {
                align-self: flex-start;
              }
          }

          /* @media.small Small devices (portrait tablets and large phones, 600px and up) */
          @media only screen and (min-width: 600px) {
              #helpButtons {
                  position: absolute;
                  z-index: 100;
                  right: 30px;
                  top: 30px;
                  display: block;
                  display: flex;
                  user-select: none;
                  -moz-user-select: none;
              }
          }

          /* @media.medium Medium devices (landscape tablets, 768px and up) */
          @media only screen and (min-width: 768px) {}

          /* @media.large Large devices (laptops/desktops, 992px and up) */
          @media only screen and (min-width: 992px) {}

          /* @media.larger Extra large devices (large laptops and desktops, 1200px and up) */
          @media only screen and (min-width: 1200px) {}
        </style>
        <div id="helpButtons" style="">
            <!-- <button id="clipboardCopy" data-target="#json-input" style="cursor: pointer;"> clipboardCopy </button> -->
            <div id="infoButton" style="margin-right: 0.1em;">
                <button id="refreshPage" data-target="window" style="cursor: pointer;"> refreshPage</button>
                <button id="clipboardRead" data-target="#json-input" style="cursor: pointer;"> clipboardRead </button>
                <button id="localChange" data-target="#json-viewer" style="cursor: pointer;"> localChange</button>
                <button id="toggleRaw" data-target="#json-viewer" style="cursor: pointer;"> toggleRaw</button>
                <button id="openAll" data-target="a.json-toggle" style="cursor: pointer;"> openAll </button>
                <button id="closeAll" data-target="a.json-toggle" style="cursor: pointer;"> closeAll </button>
                <button id="downloadFile" style="cursor: pointer;">downloadFile
                  <a href="" id="downloadFile_target" style="display: none">click here to download your file</a>
                </button>
                <button id="clipboardCopy" data-target="#json-input" style="cursor: pointer;"> clipboardCopy </button>
            </div>
            <button id="infoToggle" class="infoToggle" data-target="#infoButton" style="cursor: pointer;"> > </button>
            <script type="text/javascript">
              // Copy to clickboard
              document.getElementById('clipboardCopy').addEventListener('click', clipboardCopy);
              document.getElementById('clipboardRead').addEventListener('click', clipboardRead);
              document.getElementById('openAll').addEventListener('click', openAll);
              document.getElementById('closeAll').addEventListener('click', closeAll);
              document.getElementById('infoToggle').addEventListener('click', infoToggle);
              document.getElementById('localChange').addEventListener('click', localChange);
              document.getElementById('toggleRaw').addEventListener('click', toggleRaw);
              document.getElementById('downloadFile').addEventListener('click', () => downloadFile('file text', 'data.json', 'text/json'));
              document.getElementById('refreshPage').addEventListener('click', refreshPage);


              async function clipboardCopy() {
                  let text = document.querySelector(this.dataset.target).value;
                  // let text = document.querySelector("#json-input").value;
                  await navigator.clipboard.writeText(text);
              }

              async function clipboardRead() {
                  let element = document.querySelector(this.dataset.target);
                  // let text = document.querySelector("#json-input").value;
                  let text = await navigator.clipboard.readText();
                  element.innerHTML = text
                  document.querySelector('#json-viewer').click()
              }

              // Array.from(document.querySelectorAll('a.json-toggle')).map( e => e.click())

              async function openAll() {
                  Array.from(document.querySelectorAll('a.json-toggle')).map(e => {
                      if (e.classList.contains("collapsed")) {
                          e.click()
                      }
                  })
              }

              async function closeAll() {
                  Array.from(document.querySelectorAll('a.json-toggle')).map(e => {
                      if (!e.classList.contains("collapsed")) {
                          e.click()
                      }
                  })
                  document.querySelector('a.json-toggle').click()
              }

              async function infoToggle() {
                  document.querySelector(this.dataset.target).classList.toggle("hidden");
                  this.classList.toggle('closed')
              }

              async function localChange() {
                  document.querySelector('#json-viewer').click()
              }

              async function refreshPage() {
                  // document.querySelector('#json-viewer').click()
                  self.location.replace(location['href'])
              }

              async function toggleRaw() {                  
                  document.getElementById("json-renderer").classList.toggle('hidden');
                  document.getElementById("json-input").classList.toggle('hidden');
              }


              document.getElementById('infoToggle').click()
            </script>
            <script type="text/javascript">
              async function downloadFile(text, name, type) {
                var a = document.getElementById("downloadFile_target");
                var text_data = document.getElementById("json-input").value;
                var file = new Blob([text_data], {type: type});
                a.href = URL.createObjectURL(file);
                a.download = name;
                a.click();
              }
            </script>
        </div>
    </section>
    <section>
      <p class="options" style="display: none">
          Options:
          <label title="Generate node as collapsed">
              <input type="checkbox" id="collapsed">Collapse nodes
          </label>
          <label title="Allow root element to be collasped">
              <input type="checkbox" id="root-collapsable" checked>Root collapsable
          </label>
          <label title="Surround keys with quotes">
              <input type="checkbox" id="with-quotes">Keys with quotes
          </label>
          <label title="Generate anchor tags for URL values">
              <input type="checkbox" id="with-links" checked>
              With Links
          </label>
      </p>
      <button id="json-viewer" title="run jsonViewer()" style="display: none">Transform to HTML</button>
    </section>
    <textarea id="json-input" autocomplete="off" class="hidden" spellcheck="false">{{ data }}</textarea>
    <pre id="json-renderer" class="json-editor-blackbord full-screen"></pre>
    <section>
        <style type="text/css">
          @media only screen and (max-width: 600px) {
              #infoSection {
                  position: absolute;
                  z-index: 100;
                  right: 10px;
                  bottom: 10px;
                  display: block;
                  display: flex;
                  color: #c2c2c2;
                  user-select: none;
                  -moz-user-select: none;
                  font-size: 80%
              }
          }

          /* @media.small Small devices (portrait tablets and large phones, 600px and up) */
          @media only screen and (min-width: 600px) {
              #infoSection {
                  position: absolute;
                  z-index: 100;
                  right: 30px;
                  bottom: 30px;
                  display: block;
                  display: flex;
                  color: #c2c2c2;
                  user-select: none;
                  -moz-user-select: none;
              }
          }
        </style>
        <div id="infoSection">
            <small><span id="dateTime"></span></small>
            <script type="text/javascript">
            
              async function getDate() {
                let date = new Date();
                document.getElementById('dateTime').innerText = date.toLocaleString();
              }

            window.onload = getDate();
            </script>
        </div>
    </section>
</body>
<script type="text/javascript">
  (function() {
      function renderJson() {
          try {
              // var input = eval('(' + document.querySelector('#json-input').value + ')');
              var input = JSON.parse(document.querySelector('#json-input').value);
              console.log(document.querySelector('#json-input').value)
          } catch (error) {
              return alert("Cannot eval JSON: " + error);
          }
          var options = {
              collapsed: document.querySelector('#collapsed').checked,
              rootCollapsable: document.querySelector('#root-collapsable').checked,
              withQuotes: document.querySelector('#with-quotes').checked,
              withLinks: document.querySelector('#with-links').checked
          };
          jsonViewer(input, options);
      }

      // Generate on click
      document.querySelector('#json-viewer').addEventListener('click', () => renderJson());

      // Generate on option change
      document.querySelector('p.options input[type=checkbox]').addEventListener('click', () => renderJson());

      // Display JSON sample on page load
      renderJson()
  })();
</script>
</html>"""

"""
## TESTS

export JSONIFY_ALWAYS=0
export FLASK_DEBUG=1

echo ${JSONIFY_ALWAYS}
echo ${DEBUG}


// ## JSON will return
curl "http://127.0.0.1:5052/"


// ## HTML will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" 

// ## JSON will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" \
   -H "Content-Type: application/json"


// Turning debug off
export JSONIFY_ALWAYS=0
export FLASK_DEBUG=0

echo ${JSONIFY_ALWAYS}
echo ${DEBUG}

// ## JSON will return
curl "http://127.0.0.1:5052/"


// ## JSON will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" 

// ## JSON will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" \
   -H "Content-Type: application/json"





# Turning JSONIFY_ALWAYS on

export JSONIFY_ALWAYS=1
export FLASK_DEBUG=0

echo ${JSONIFY_ALWAYS}
echo ${DEBUG}

// ## JSON will return
curl "http://127.0.0.1:5052/"


// ## HTML will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" 

// ## JSON will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" \
   -H "Content-Type: application/json"



export FLASK_DEBUG=1
export JSONIFY_ALWAYS=1

echo ${JSONIFY_ALWAYS}
echo ${DEBUG}

// ## JSON will return
curl "http://127.0.0.1:5052/"


// ## HTML will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" 

// ## JSON will return
curl "http://127.0.0.1:5052/" \
   -A "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" \
   -H "Content-Type: application/json"


"""

"""
// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  console.log(response)
  return response.json(); // parses JSON response into native JavaScript objects
}

postData("http://127.0.0.1:5052/")


async function getData(url = '', data = {}) {
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
  console.log(response)
  return response.json(); // parses JSON response into native JavaScript objects
}

const data = await getData("http://127.0.0.1:5052/")

"""

