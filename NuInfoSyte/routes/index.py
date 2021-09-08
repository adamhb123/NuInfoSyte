from flask import render_template, request

import config
from NuInfoSyte import app, nis_middleware, limiter


def setup_web_routes():
    @app.route("/", methods=['GET', 'POST'])
    @limiter.limit(config.WEB_RATE_LIMIT)
    def index():
        # Serve index
        if request.method == "GET":
            return render_template(
                'index.html',
                mode_dict=nis_middleware.get_modes(),
                color_dict=nis_middleware.get_colors()
            )

        # Handle form submission
        elif request.method == "POST":
            animations = request.get_json()
            if not app.config["DISABLE_BETABRITE_TRANSMISSION"]:
                for animation in animations:
                    app.logger.info(f"Adding animation: {animation}")
                    nis_middleware.add_animation(animation['text'], animation['mode'], animation['color'])
                nis_middleware.send_animations()
            return render_template(
                'index.html',
                mode_dict=nis_middleware.get_modes(),
                color_dict=nis_middleware.get_colors()
            )


if not app.config['DISABLE_WEBSITE']:
    setup_web_routes()
