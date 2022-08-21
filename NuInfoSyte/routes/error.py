from flask import render_template, session
from flask_pyoidc.user_session import UserSession
from typing import Dict
from werkzeug.exceptions import HTTPException
from NuInfoSyte import app, auth

# Dict items are in CODE: UNIQUE RESPONSE STRING form
UNIQUE_ERROR_RESPONSES: Dict[int, str] = {
    404: "Not found, check ignition",
    405: "Method not allowed, touch grass",
}

def setup_web_errorhandler() -> None:
    @auth.oidc_auth("default")
    @app.errorhandler(HTTPException)
    def error(e: HTTPException) -> str:
        response_string = UNIQUE_ERROR_RESPONSES[e.code] if e.code in UNIQUE_ERROR_RESPONSES else "None"
        countdown_duration = app.config['COUNTDOWN_DURATION'] if "COUNTDOWN_DURATION" in app.config else 5
        user_session = UserSession(session)
        return render_template("error.html", error_code=e.code, unique_response_string=response_string,
                                error_description=e.description, countdown_duration=countdown_duration,
                                redirect_link="/api", preferred_username=user_session.userinfo["preferred_username"])

if not app.config['DISABLE_WEBSITE']:
    setup_web_errorhandler()
