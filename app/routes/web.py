from flask import render_template, request, jsonify
from __main__ import app
from __main__ import nis_middleware

# ENTIRE SITE NEEDS TO BE REWRITTEN TO HANDLE LISTS OF
# ANIMATIONS
if not app.config['DISABLE_WEBSITE']:
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
            nis_middleware.send_animations()
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
