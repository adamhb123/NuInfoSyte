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

import config
from NuInfoSyte import app, limiter


def _safe_get(dictionary: dict, key: Any) -> Any: return dictionary[key] if key in dictionary else None

def setup_api_routes() -> None:
    @app.route("/send-animation-single", methods=["PUT"])
    @limiter.limit(config.API_RATE_LIMIT)
    def send_animation_single() -> Response:
        """
        PUT endpoint for handling animation requests containing a single animation
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)
        """

        json = request.get_json()
        text, mode, color = _safe_get(json, "text"), _safe_get(json, "mode"), _safe_get(json, "color")
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
    @limiter.limit(config.API_RATE_LIMIT)
    def send_animation_multi() -> Response:
        """
        PUT endpoint for handling requests containing multiple animations
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)
        """

        json = request.get_json()

        text, mode, color = _safe_get(json, "text"), _safe_get(json, "mode"), _safe_get(json, "color")
        response = {
            "result": "Success",
            "payload": {
                "text": text,
                "mode": mode,
                "color": color
            }
        }
        return jsonify(response)


def setup_web_routes():
    @app.route("/api", methods=["GET"])
    @limiter.limit(config.WEB_RATE_LIMIT)
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
