import flask, time, waitress, mysql.connector, paginate, os, flask_limiter, requests

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

    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("SELECT name, thumbnail, hotelId, rating, price, address FROM Hotels LIMIT 3")
            result = cursor.fetchall()

    topHotels = [{i: j for i, j in zip(["name", "thumbnail", "hotelId", "rating", "price", "address"], row)} for row in result]

    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("SELECT name, description, thumbnail, articleLink  FROM Articles LIMIT 3")
            result = cursor.fetchall()

    topArticles = [{i: j for i, j in zip(["name", "description", "thumbnail", "link"], row)} for row in result]

    return flask.render_template(
        "index.html",
        config = config,
        topPlaces = topPlaces,
        topHotels = topHotels,
        topArticles = topArticles
    )

@app.route("/places", methods = ["GET"])
@limiter.limit("5/second")
def placesToVisit():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("SELECT name, thumbnail, shortDescription, placeId FROM PlacesToVisit")
            result = cursor.fetchall()

    places = [{i: j for i, j in zip(["name", "thumbnail", "description", "placeId", "index"], row + (index,))} for index, row in enumerate(result)]

    placesRows = [[]]
    for index, place in enumerate(places):
        if index % 3 == 0:
            placesRows.append([])
        placesRows[-1].append(place)

    return flask.render_template(
        "places.html",
        config = config,
        places = placesRows
    )

@app.route("/place/<placeId>", methods = ["GET"])
@limiter.limit("5/second")
def getPlaceDetails(placeId):
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("SELECT * FROM PlacesToVisit WHERE placeId = %s", (placeId,))
            result = cursor.fetchone()

    if not result:
        return "<h1>Place not found in database.</h1>", 404

    placeDetails = {
        "name": result[1],
        "placeId": result[2],
        "shortDescription": result[3],
        "description": result[4].strip(),
        "thumbnail": result[5],
        "images": [{"index": index, "image": image} for index, image in enumerate(result[6].split(","))],
        "timings": result[7],
        "address": result[8],
        "location": result[9],
        "googleMapsEmbedUrl": getGoogleMapsEmbedUrl(result[9])
    }
    
    return flask.render_template(
        "place-details.html",
        config = config,
        placeDetails = placeDetails
    )

@app.route("/restrictions-lockdown", methods = ["GET"])
@limiter.limit("1/second")
def restriction():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    response = requests.get("https://www.thrillophilia.com/mysore-tourist-places").text
    restrictions = response.split("<ul>")[1].split("</ul>")[0].replace("</li>", "").strip("<li>").split("<li>")
    quarantineRules = response.split("<ul>")[2].split("</ul>")[0].replace("</li>", "").strip("<li>").split("<li>")

    restrictions = [i.strip(".") + "." for i in restrictions]
    quarantineRules = [i.strip(".") + "." for i in quarantineRules]

    return flask.render_template(
        "restrictions.html",
        config = config,
        restrictions = restrictions,
        quarantineRules = quarantineRules
    )

@app.errorhandler(404)
def not_found(e):
    return "<h1>Under construction.</h1>"

app.run(
    host = config.ip,
    port = config.port,
    debug = True
)
