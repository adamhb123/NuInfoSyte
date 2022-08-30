from flask import render_template, request, session
from flask_pyoidc.user_session import UserSession
from NuInfoSyte import app, auth, nis_middleware, limiter


def setup_web_routes() -> None:
    @auth.oidc_logout
    @app.route('/logout')
    def logout() -> str:
        return "You've been successfully logged out!"

    @auth.oidc_auth("default")
    @limiter.limit(app.config["WEB_RATE_LIMIT"])
    @app.route("/", methods=['GET', 'POST'])
    def index() -> str:
        # Serve index
        if request.method == "GET":
            user_session = UserSession(session)
            return render_template(
                "index.html",
                preferred_username=user_session.userinfo["preferred_username"],
                mode_dict=nis_middleware.get_modes(),
                color_dict=nis_middleware.get_colors()
            )

        # Handle form submission
        elif request.method == "POST":
            animations = request.get_json()
            if animations and not app.config["DISABLE_BETABRITE_TRANSMISSION"]:
                for animation in animations:
                    app.logger.info(f"Adding animation: {animation}")
                    nis_middleware.add_animation(
                        animation['text'], animation['mode'], animation['color'])
                nis_middleware.send_animations()
                return render_template(
                    'index.html',
                    mode_dict=nis_middleware.get_modes(),
                    color_dict=nis_middleware.get_colors()
                )


if not app.config['DISABLE_WEBSITE']:
    setup_web_routes()
