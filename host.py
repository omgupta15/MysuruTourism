import flask, time, waitress, mysql.connector, paginate, os, flask_limiter

os.system("title Mysuru Tourism Host")

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

class config:
    name = "Mysuru Tourism"
    host = "localhost" # "mysuru.us.to"
    websiteUrl = "http://localhost/" # "https://mysuru.us.to/"
    ip = "127.0.0.1" # "0.0.0.0"
    port = 80 # 2525

def getGoogleMapsEmbedUrl(location):
    return "https://www.google.com/maps/embed/v1/place?key={apiKey}&q={location}".format(
        apiKey = os.environ.get("GoogleMapsEmbedApiKey"),
        location = location.replace(" ", "+")
    )

app = flask.Flask(__name__, static_folder = "resources")
limiter = flask_limiter.Limiter(app, key_func = flask_limiter.util.get_remote_address)

@app.route("/", methods = ["GET"])
@limiter.limit("5/second")
def index():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("SELECT name, thumbnail, shortDescription, placeId FROM PlacesToVisit LIMIT 3")
            result = cursor.fetchall()

    topPlaces = [{i: j for i, j in zip(["name", "thumbnail", "description", "placeId", "index"], row + (index,))} for index, row in enumerate(result)]

    return flask.render_template(
        "index.html",
        config = config,
        topPlaces = topPlaces
    )

app.run(
    host = config.ip,
    port = config.port,
    debug = True
)
