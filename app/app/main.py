from flask import Flask
from flask import render_template
from flask_googlemaps import GoogleMaps

app = Flask(__name__)


@app.route("/")
def index():
    print(app.config)
    return render_template('index.html')


if __name__ == "__main__":
    app.config.from_envvar("CONF")

    GoogleMaps(app)
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=app.config["DEBUG"], port=80)
