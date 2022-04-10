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
from NuInfoSys.betabrite import Animation
from NuInfoSyte import app, limiter, nis_middleware


def _safe_get(dictionary: dict, key: Any) -> Any: return dictionary[key] if key in dictionary else None


def _safe_get_all(dictionary: dict, keys: List[Any]) -> Any:
    return [dictionary[key] if key in dictionary else None for key in keys]


def parse_single_animation_payload_json(json: dict) -> dict:
    """
    Parses single animation json from given json dict
    """
    text, mode, color = _safe_get_all(json, ["text", "mode", "color"])
    return {"text": text, "mode": mode, "color": color}


def setup_api_routes() -> None:
    @app.route("/send-animation-single", methods=["PUT"])
    @limiter.limit(config.API_RATE_LIMIT)
    def send_animation_single() -> Response:
        """
        PUT endpoint for handling animation requests containing a single animation
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)
        """
        json = request.get_json()
        payload: dict = parse_single_animation_payload_json(json)
        nis_middleware.add_animation(payload["text"], payload["mode"], payload["color"])
        nis_middleware.send_animations()
        response = {
            "payload": json,
            "result": "Success"
        }
        return jsonify(response)

    @app.route("/send-animation-multi", methods=["PUT"])
    @limiter.limit(config.API_RATE_LIMIT)
    def send_animation_multi() -> Response:
        """
        PUT endpoint for handling requests containing multiple animations
        :return: JSON Response with the payload data sent by the user (essentially formats and mirrors the data)

        DOESN'T CURRENTLY FUNCTION
        """
        json = request.get_json()
        for jval in json:
            parsed: dict = parse_single_animation_payload_json(jval)
            nis_middleware.add_animation(parsed["text"], parsed["mode"], parsed["color"])
        nis_middleware.send_animations()
        response = {
            "payload": json,
            "result": "Success"
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
