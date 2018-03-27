from flask import Flask
from flask import render_template
from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.config.from_envvar("CONF")


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    GoogleMaps(app)
    # Only for debugging while developing
    app.run(host='0.0.0.0', port=80)
