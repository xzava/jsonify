
24.05.2022

- Changes the response type bug, now it will always return a flask Response
- Added a flag for debug information `JSONIFY_VERBOSE` use 1 or 0, debug must also be on.
- Changed the styles for mobile screen size, 2 spaces rather than one tab. Turned off the toggle button, as it was to big for mobile. Still works but is invisible 

24.05.2022

- Will add a always on flag (will still turn off to non browsers) ie runs when debug is off
- Will add a header flag to turn off if javascript fetch is requesting the endpoint.
- add the template as a string on this page, so only once file contains everything needed.
- Add timestamp in bottom corner so your knows how old the request is