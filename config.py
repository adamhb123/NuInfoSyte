"""
Defines application configuration variables
"""
import os
from distutils.util import strtobool

# Flask Config
DEBUG: bool = strtobool(os.environ.get("DEBUG", "False"))
IP: str = os.environ.get("NUINFOSYTE_IP", "localhost")
PORT: str = os.environ.get("NUINFOSYTE_PORT", "3000")
PROTOCOL: str = os.environ.get("NUINFOSYTE_PROTOCOL", "http://")
# SERVER_NAME: str = os.environ.get("NUINFOSYTE_SERVER_NAME", f"{IP}:{PORT}")

# NuInfoSyte Config
DISABLE_WEBSITE: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_WEBSITE", "False"))
DISABLE_API: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_API", "False"))
DISABLE_BETABRITE_TRANSMISSION: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_BETABRITE_TRANSMISSION", "False"))
# See flask limiter docs for usable syntax for these rate limits
WEB_RATE_LIMIT = "50/day"
API_RATE_LIMIT = "30/minute"

# OpenID Connect SSO config
SECRET_KEY = os.environ.get("NUINFOSYS_SECRET_KEY", "poopfart")
OIDC_ISSUER = os.environ.get("NUINFOSYTE_OIDC_ISSUER", "https://sso.csh.rit.edu/auth/realms/csh")
OIDC_REDIRECT_URI = os.environ.get("NUINFOSYTE_OIDC_REDIRECT_URI", PROTOCOL+IP+":"+PORT+"/authentication/callback")
OIDC_CLIENT_CONFIG = {
    "client_id": os.environ.get("NUINFOSYTE_OIDC_CLIENT_ID", "react-boilerplate"),
    "client_secret": os.environ.get("NUINFOSYTE_OIDC_CLIENT_SECRET", ""),
    "post_logout_redirect_uris": [os.environ.get("NUINFOSYTE_OIDC_LOGOUT_REDIRECT_URI", "amongus")]
}
