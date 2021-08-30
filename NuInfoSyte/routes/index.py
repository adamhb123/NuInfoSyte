from flask import render_template, request
from NuInfoSyte import app, nis_middleware


def setup_web_routes():
    @app.route("/", methods=['GET', 'POST'])
    def index():
        # Serve index
        if request.method == "GET":
            return render_template('index.html',
                                   mode_dict=nis_middleware.get_modes(),
                                   color_dict=nis_middleware.get_colors(),
                                   position_dict=nis_middleware.get_positions())

        # Handle form submission
        elif request.method == "POST":
            print(request.form)
            animations = request.form.get("animation-list")
            for animation in animations:
                nis_middleware.add_animation(animation.text, animation.mode, animation.color, animation.position)

            return render_template(
                'index.html',
                mode_dict=nis_middleware.get_modes(),
                color_dict=nis_middleware.get_colors(),
                position_dict=nis_middleware.get_positions()
            )


if not app.config['DISABLE_WEBSITE']:
    setup_web_routes()
