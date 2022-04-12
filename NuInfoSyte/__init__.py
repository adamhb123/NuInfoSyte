"""
Application Entrypoint
Serves web + api
"""
import flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession
import config
from NuInfoSyte import nis_middleware

app = flask.Flask(__name__)
app.config.from_object("config")
client_metadata = ClientMetadata(config.OIDC_CLIENT_CONFIG["client_id"],
                                 config.OIDC_CLIENT_CONFIG["client_secret"],
                                 post_logout_redirect_uris=[config.OIDC_REDIRECT_URI])

provider_config = ProviderConfiguration(issuer=config.OIDC_ISSUER,
                                        client_metadata=client_metadata)

auth = OIDCAuthentication({'default': provider_config}, app)
limiter = Limiter(
    app,
    key_func=get_remote_address
)


# setup routes
@app.route("/login")
@auth.oidc_auth("default")
def login():
    user_session = UserSession(flask.session)
    return flask.jsonify(access_token=user_session.access_token,
                         id_token=user_session.id_token,
                         userinfo=user_session.userinfo)


from NuInfoSyte.routes import index, api, error
