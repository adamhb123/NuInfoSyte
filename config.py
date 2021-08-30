"""
Defines application configuration variables
"""
import os
from distutils.util import strtobool
# Flask Config
DEBUG: bool = strtobool(os.environ.get("DEBUG", "False"))
IP: str = os.environ.get("PACKET_IP", "localhost")
PORT: str = os.environ.get("PACKET_PORT", "6969")
PROTOCOL: str = os.environ.get("NUINFOSYS_PROTOCOL", "https://")
SERVER_NAME: str = os.environ.get("NUINFOSYS_SERVER_NAME", f"{IP}:{PORT}")

# NuInfoSyte Config
DISABLE_WEBSITE: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_WEBSITE", "False"))
DISABLE_API: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_API", "False"))
DISABLE_BETABRITE_TRANSMISSION: bool = strtobool(os.environ.get("NUINFOSYTE_DISABLE_BETABRITE_TRANSMISSION", "False"))
