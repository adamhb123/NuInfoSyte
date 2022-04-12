"""
Application Entrypoint
Serves web + api
"""
from flask import Flask, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from NuInfoSyte import nis_middleware

app = Flask(__name__)
app.config.from_object("config")
client_metadata = ClientMetadata(app.config["OIDC_CLIENT_CONFIG"]["client_id"],
                                 app.config["OIDC_CLIENT_CONFIG"]["client_secret"],
                                 post_logout_redirect_uris=[app.config["OIDC_REDIRECT_URI"]])

provider_config = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                                        client_metadata=client_metadata)

auth = OIDCAuthentication({'default': provider_config}, app)
limiter = Limiter(
    app,
    key_func=get_remote_address
)

# setup routes

from NuInfoSyte.routes import index, api, error
