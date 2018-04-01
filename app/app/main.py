from flask import Flask
from flask import render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


app = Flask(__name__)
app.config.from_envvar("CONF")


@app.route("/")
def index():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    return render_template('index.html', mymap=mymap)


if __name__ == "__main__":
    GoogleMaps(app)
    # Only for debugging while developing
    app.run(host='0.0.0.0', port=80)
