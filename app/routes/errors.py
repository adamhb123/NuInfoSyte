from flask import redirect, Response
import werkzeug

from __main__ import app


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_method_not_allowed(e) -> Response:
    return redirect("/api", code=405)
