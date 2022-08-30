# Add NuInfoSys to path
from NuInfoSyte import app
from NuInfoSys import server
if __name__ == "__main__":
    server.start()
    app.run(host=app.config["IP"],
            port=app.config["PORT"], debug=app.config["DEBUG"])
