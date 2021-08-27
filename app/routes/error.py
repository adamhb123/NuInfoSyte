from flask import render_template, request
from typing import Dict
from werkzeug.exceptions import HTTPException

from __main__ import app

# Dict items are in CODE: CUSTOM RESPONSE STRING form
UNIQUE_ERROR_RESPONSES: Dict[int, str] = {
    405: "SUs",
}


def setup_web_errorhandler():
    @app.errorhandler(HTTPException)
    def error(e):
        if request.method == "GET":
            response_string = UNIQUE_ERROR_RESPONSES[e.code] if e.code in UNIQUE_ERROR_RESPONSES else None
            countdown_duration = app.config['COUNTDOWN_DURATION'] if "COUNTDOWN_DURATION" in app.config else 5
            return render_template("error.html", error_code=e.code, custom_response_string=response_string,
                                   error_description=e.description, countdown_duration=countdown_duration,
                                   redirect_link="/api")


if not app.config['DISABLE_WEBSITE']:
    setup_web_errorhandler()
