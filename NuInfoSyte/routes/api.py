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
from typing import Any, List

from flask import render_template, request, jsonify, Response

from NuInfoSyte import app


def _safe_get(dictionary: dict, key: Any) -> Any: return dictionary[key] if key in dictionary else None


def _safe_get_all(dictionary: dict, keys: List[Any]) -> Any:
    return [dictionary[key] if key in dictionary else None for key in keys]


def setup_api_routes() -> None:
    @app.route("/send-animation-single", methods=["PUT"])
    def send_animation_single() -> Response:
        """
        POST endpoint for handling animation requests containing a single animation
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)
        """

        json = request.get_json()
        text, mode, color, position = _safe_get_all(json, ["text", "mode", "color", "position"])
        response = {
            "result": "Success",
            "payload": {
                "text": text,
                "mode": mode,
                "color": color,
                "position": position
            }
        }
        return jsonify(response)

    @app.route("/send-animation-multi", methods=["PUT"])
    def send_animation_multi() -> Response:
        """
        POST endpoint for handling requests containing multiple animations
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)
        """

        json = request.get_json()

        text, mode, color, position = _safe_get_all(json, ["text", "mode", "color", "position"])
        response = {
            "result": "Success",
            "payload": {
                "text": text,
                "mode": mode,
                "color": color,
                "position": position
            }
        }
        return jsonify(response)


def setup_web_routes():
    @app.route("/api", methods=["GET"])
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
