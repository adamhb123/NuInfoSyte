"""
API Routes
All API-related routes are defined here (along with the api description webpage)
API routes should follow the REST conventions.
In other words, use:
    * GET to retrieve resources
    * POST to create new resources
    * PUT to update existing resources
    * DELETE to delete resources

I've determined other methods to be unnecessary for this application.
"""
from typing import Any, Optional, List, Union, Dict
from dataclasses import dataclass
from flask import render_template, request, jsonify
from flask.wrappers import Response

from NuInfoSyte import app, auth, limiter, nis_middleware

def _safe_get_all(dictionary: Dict, keys: List[Any]) -> Any:
    return [dictionary[key] if key in dictionary else None for key in keys]

@dataclass
class APIResponse:
    successful: bool
    payload: Optional[Union[Dict, List]] = None

    def json(self) -> Dict:
        return {
            "result": "Successful" if self.successful else "Failure",
            "payload": self.payload
        }

    def jsonify(self) -> Response:
        return jsonify(self.json())

class InvalidAnimationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def parse_single_animation_payload_json(animation_json: Dict) -> Dict:
    """
    Parses single animation animation_json from given animation_json dict
    """
    text, mode, color = _safe_get_all(
        animation_json, ["text", "mode", "color"])
    if not all([text, mode, color]):
        raise Exception("Invalid animation_json")
    return {"text": text, "mode": mode, "color": color}


def setup_api_routes() -> None:
    @app.route("/send-animation-single", methods=["PUT"])
    @limiter.limit(app.config["API_RATE_LIMIT"])
    def send_animation_single(animation_json: Optional[Dict] = None) -> Response:
        """
        PUT endpoint for handling animation requests containing a single animation
        :return: animation_json Response with the payload data sent by the user (essentially formats and mirrors the data)
        """
        if animation_json and type(animation_json) == dict:
            payload = parse_single_animation_payload_json(animation_json)
        else:
            request_json = request.get_json()
            payload = request_json if type(request_json) == dict else {}
        if payload and type(animation_json) == dict:
            nis_middleware.add_animation(
                payload["text"], payload["mode"], payload["color"])
            nis_middleware.send_animations()
            response = APIResponse(True, animation_json)
        else:
            response = APIResponse(False)
        return response.jsonify()

    @app.route("/send-animation-multi", methods=["PUT"])
    @limiter.limit(app.config["API_RATE_LIMIT"])
    def send_animation_multi(animation_json: Optional[List] = None) -> Response:
        """
        PUT endpoint for handling requests containing multiple animations
        :return: animation_json Response with the payload data sent by the user (essentially formats and mirrors the data)
        
        DOESN'T CURRENTLY FUNCTION (maybe)
        """
        if not animation_json:
            animation_json = request.get_json()
        if animation_json and type(animation_json) == list:
            for jval in animation_json:
                parsed: dict = parse_single_animation_payload_json(jval)
                nis_middleware.add_animation(
                    parsed["text"], parsed["mode"], parsed["color"])
            nis_middleware.send_animations()
            return APIResponse(True, animation_json).jsonify()
        return APIResponse(False).jsonify()

def setup_web_routes() -> None:
    @app.route("/api", methods=["GET"])
    @limiter.limit(app.config["WEB_RATE_LIMIT"])
    @auth.oidc_auth("default")
    def api_index() -> str:
        """
        [API Index]
        Serves the api page
        :return: rendered api page
        """
        return render_template('api.html')


if not app.config['DISABLE_WEBSITE']:
    setup_web_routes()

if not app.config['DISABLE_API']:
    setup_api_routes()
