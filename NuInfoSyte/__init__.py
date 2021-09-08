"""
Application Entrypoint
Serves web + api
"""
from NuInfoSyte import nis_middleware
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_object("config")
limiter = Limiter(
    app,
    key_func=get_remote_address
)
# setup routes
from NuInfoSyte.routes import index, api, error
