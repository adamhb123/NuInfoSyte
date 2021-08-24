"""API Routes
All API-related routes are defined here.
"""
from flask import render_template, request, jsonify
import config
from __main__ import app

# All input data is received as a query string
if not config.DISABLE_API:
    @app.route("/send-animation", methods=["POST"])
    def send_animation():
        """[API Method]
        POST endpoint for handling singular animation requests
        """
        text = request.args.get("text")
        mode = request.args.get("mode")
        color = request.args.get("color")
        position = request.args.get("position")
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

