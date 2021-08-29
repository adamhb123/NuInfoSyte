"""
Application Entrypoint
Serves web + api
"""
from NuInfoSyte import nis_middleware
from flask import Flask

app = Flask(__name__)
app.config.from_object("config")
# setup routes
from NuInfoSyte.routes import index, api, error

