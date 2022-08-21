# Add NuInfoSys to path
from NuInfoSyte import app

if __name__ == "__main__":
    app.run(host=app.config["IP"],
            port=app.config["PORT"], debug=app.config["DEBUG"])
