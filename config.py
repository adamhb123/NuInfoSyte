import os
from distutils.util import strtobool
# Flask Config
DEBUG = strtobool(os.environ.get("DEBUG", "False"))
IP = os.environ.get("PACKET_IP", "localhost")
PORT = os.environ.get("PACKET_PORT", "6969")
PROTOCOL = os.environ.get("NUINFOSYS_PROTOCOL", "https://")
SERVER_NAME = os.environ.get("NUINFOSYS_SERVER_NAME", f"{IP}:{PORT}")

# NuInfoSys Config
DISABLE_WEBSITE = False
DISABLE_API = False
