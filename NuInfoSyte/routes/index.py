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
            text = request.form.get("text-input")
            mode = request.form.get("mode-input")
            color = request.form.get("color-input")
            position = request.form.get("pos-input")
            nis_middleware.add_animation(text, mode, color, position)
            return render_template(
                'index.html',
                text_input=text,
                mode_input=mode,
                color_input=color,
                position_input=position,
                mode_dict=nis_middleware.get_modes(),
                color_dict=nis_middleware.get_colors(),
                position_dict=nis_middleware.get_positions()
            )


if not app.config['DISABLE_WEBSITE']:
    setup_web_routes()
