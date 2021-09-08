"""
Defines application configuration variables
"""
import os
from distutils.util import strtobool

# Flask Config
DEBUG: bool = strtobool(os.environ.get("DEBUG", "False"))
IP: str = os.environ.get("NUINFOSYTE_IP", "0.0.0.0")
PORT: str = os.environ.get("NUINFOSYTE_PORT", "6969")
PROTOCOL: str = os.environ.get("NUINFOSYTE_PROTOCOL", "http://")
# SERVER_NAME: str = os.environ.get("NUINFOSYTE_SERVER_NAME", f"{IP}:{PORT}")

# NuInfoSyte Config
DISABLE_WEBSITE: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_WEBSITE", "False"))
DISABLE_API: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_API", "False"))
DISABLE_BETABRITE_TRANSMISSION: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_BETABRITE_TRANSMISSION", "False"))
# See flask limiter docs for usable syntax for these rate limits
WEB_RATE_LIMIT = "50/day"
API_RATE_LIMIT = "1/second"
