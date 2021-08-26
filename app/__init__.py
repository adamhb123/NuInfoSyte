"""Application Entrypoint
Serves web + api
"""
from flask import Flask
import betabrite_middleware

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
from routes import web, api

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
