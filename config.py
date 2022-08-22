"""
Defines application configuration variables
"""
import os
import json
from distutils.util import strtobool
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def stb_envget(envvar: str, default: str) -> bool: return bool(strtobool(
    os.environ.get(envvar, default)))

# Flask ConfigE
DEBUG: bool = stb_envget("DEBUG", "False")
IP: str = os.environ.get("NUINFOSYTE_IP", "localhost")
PORT: str = os.environ.get("NUINFOSYTE_PORT", "3000")
PROTOCOL: str = os.environ.get("NUINFOSYTE_PROTOCOL", "http://")
# SERVER_NAME: str = os.environ.get("NUINFOSYTE_SERVER_NAME", f"{IP}:{PORT}")
# NuInfoSyte Config
DISABLE_WEBSITE: bool = stb_envget("NUINFOSYTE_DISABLE_WEBSITE", "False")
DISABLE_API: bool = stb_envget("NUINFOSYTE_DISABLE_API", "False")
DISABLE_BETABRITE_TRANSMISSION: bool = stb_envget(
    "NUINFOSYTE_DISABLE_BETABRITE_TRANSMISSION", "False")
# NuInfoSys Config
NUINFOSYS_API_IP: str = os.environ.get("NUINFOSYS_API_IP", "localhost")
NUINFOSYS_API_PORT: str = os.environ.get("NUINFOSYS_API_PORT", "6969")

# See flask limiter docs for usable syntax for these rate limits
WEB_RATE_LIMIT = "5/day"
API_RATE_LIMIT = "1/minute"

# OpenID Connect SSO config
SECRET_KEY = os.environ.get("NUINFOSYS_SECRET_KEY", "supersecretfeafeafeafeas")
OIDC_ISSUER = os.environ.get(
    "NUINFOSYTE_OIDC_ISSUER", "https://sso.csh.rit.edu/auth/realms/csh")
OIDC_REDIRECT_URI = os.environ.get(
    "NUINFOSYTE_OIDC_REDIRECT_URI", f"{PROTOCOL}{IP}:{PORT}/authentication/callback")
OIDC_POST_LOGOUT_REDIRECT_URIS = json.loads(os.environ.get(
    "NUINFOSYTE_OIDC_POST_LOGOUT_REDIRECT_URIS", "[]"))
OIDC_CLIENT_ID = os.environ.get(
    "NUINFOSYTE_OIDC_CLIENT_ID", "react-boilerplate")
OIDC_CLIENT_SECRET = os.environ.get("NUINFOSYTE_OIDC_CLIENT_SECRET", "fakesecret")
