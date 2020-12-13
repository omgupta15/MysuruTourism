import flask, time, waitress, mysql.connector, paginate, os, flask_limiter, requests
import html, json, base64, urllib.parse, datetime

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

    response = requests.get(
        "https://www.trivago.in/mysore-94410/hotel",
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }).text

    topHotels = response.split("<h2 class=\"h2\">Top hotels</h2>")[1].split("<div class=\"trvsc_toplist_more trvsc_more_top_hotels\">")[0]
    topHotels = topHotels.split("<a href=\"")[1:]
    result = []

    for hotel in topHotels:
        link = hotel.split("\"")[0]
        thumbnail = "http://" + hotel.split("<img data-src=\"//")[1].split("\"")[0]
        name = hotel.split("<div class=\"trvsc_path_info\"><strong class=\"trvsc_path_name\">")[1].split("</strong>")[0]
        price = hotel.split("&lrm;")[1].split("</strong>")[0]

        result.append((name, thumbnail, price, "Mysuru, Karnataka", link,))

    topHotels = [{i: j for i, j in zip(["name", "thumbnail", "price", "address", "link"], row)} for row in result[:3]]

    response = requests.get("https://starofmysore.com/category/feature-articles/").text
    blogs = response.split("<div class=\"standard_blog\">")[1].split("class=\"alaya_pagenavi\"")[0]
    result = []

    for blog in blogs.split("<article class")[1:]:
        link = blog.split("href=")[1][:blog.split("href=")[1].index("\">")].strip("\"")
        title = blog.split("title=")[2][blog.split("title=")[2].index("\">")+2:].split("</a></h4>")[0]
        date = blog.split("<span class=\"category\">")[2][:blog.split("<span class=\"category\">")[2].index("</span>")]
        description = html.unescape(blog.split("<p>")[-1].split("</p>")[0])
        thumbnail = blog.split("<img width=")[1].split("src=")[1][:blog.split("<img width=")[1].split("src=")[1].index("class=")].strip().strip("\"")
        thumbnail = urllib.parse.quote_plus(thumbnail)

        result.append((title, description, thumbnail, link, date,))

    topArticles = [{i: j for i, j in zip(["name", "description", "thumbnail", "link", "date"], row)} for row in result[:3]]

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

@app.route("/place/<placeId>", methods = ["GET", "POST"])
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

    placeDatabaseId = result[0]

    if method == "GET":
        with getDatabase() as database:
            with database.cursor() as cursor:
                cursor.execute("SELECT name, review, added, rating FROM Reviews WHERE placeId = %s AND NOT blocked", (placeDatabaseId,))
                reviewsResult = cursor.fetchall()

        reviews = [{"name": name, "review": review, "added": datetime.datetime.fromtimestamp(added/1000).strftime("%d %B, %Y"), "rating": rating} for name, review, added, rating in reviewsResult]

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
            "googleMapsEmbedUrl": getGoogleMapsEmbedUrl(result[9]),
            "reviews": reviews
        }
        
        return flask.render_template(
            "place-details.html",
            config = config,
            placeDetails = placeDetails
        )

    elif method == "POST":
        try:
            data = json.loads(data)
            username = str(flask.escape(data["name"]))
            rating = int(data["rating"])
            review = str(flask.escape(data["review"]))
        except:
            return flask.jsonify({
                "success": False,
                "error": "invalid-json"
            })

        if not username or len(username) > 40:
            return flask.jsonify({
                "success": False,
                "error": "invalid-username"
            })

        if rating not in range(1, 11):
            return flask.jsonify({
                "success": False,
                "error": "invalid-rating"
            })

        if not review or len(review) > 10000:
            return flask.jsonify({
                "success": False,
                "error": "invalid-review"
            })

        with getDatabase() as database:
            with database.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Reviews (
                        name,
                        review,
                        added,
                        rating,
                        placeId,
                        blocked
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    username,
                    review,
                    int(time.time()*1000),
                    rating,
                    placeDatabaseId,
                    False,
                ))
                database.commit()

        return flask.jsonify({"success": True})

@app.route("/articles", methods = ["GET"])
@limiter.limit("5/second")
def articles():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    result = []

    for page in ("", "page/2/", "page/3/"):
        response = requests.get("https://starofmysore.com/category/feature-articles/" + page).text
        blogs = response.split("<div class=\"standard_blog\">")[1].split("class=\"alaya_pagenavi\"")[0]

        for blog in blogs.split("<article class")[1:]:
            link = blog.split("href=")[1][:blog.split("href=")[1].index("\">")].strip("\"")
            title = html.unescape(blog.split("title=")[2][blog.split("title=")[2].index("\">")+2:].split("</a></h4>")[0])
            date = blog.split("<span class=\"category\">")[2][:blog.split("<span class=\"category\">")[2].index("</span>")]
            description = html.unescape(blog.split("<p>")[-1].split("</p>")[0])
            thumbnail = blog.split("<img width=")[1].split("src=")[1][:blog.split("<img width=")[1].split("src=")[1].index("class=")].strip().strip("\"")
            thumbnail = urllib.parse.quote_plus(thumbnail)

            result.append((title, description, thumbnail, link, date,))

    articles = [{i: j for i, j in zip(["name", "description", "thumbnail", "link", "date"], row)} for row in result]
    
    articlesRows = [[]]
    for index, article in enumerate(articles):
        if index % 3 == 0:
            articlesRows.append([])
        articlesRows[-1].append(article)

    return flask.render_template(
        "articles.html",
        config = config,
        articles = articlesRows
    )

@app.route("/find-hotels", methods = ["GET"])
@limiter.limit("5/second")
def findHotels():
    return flask.redirect(config.websiteUrl + "hotels")

@app.route("/hotels", methods = ["GET"])
@limiter.limit("5/second")
def hotels():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    response = requests.get(
        "https://www.trivago.in/mysore-94410/hotel",
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }).text

    hotelsList = response.split("<h2 class=\"h2\">Top hotels</h2>")[1].split("<div class=\"trvsc_toplist_more trvsc_more_top_hotels\">")[0]
    hotelsList = hotelsList.split("<a href=\"")[1:]
    result = []

    for hotel in hotelsList:
        link = hotel.split("\"")[0]
        thumbnail = "http://" + hotel.split("<img data-src=\"//")[1].split("\"")[0]
        name = hotel.split("<div class=\"trvsc_path_info\"><strong class=\"trvsc_path_name\">")[1].split("</strong>")[0]
        price = hotel.split("&lrm;")[1].split("</strong>")[0]

        result.append((name, thumbnail, price, "Mysuru, Karnataka", link,))

    hotelsList = [{i: j for i, j in zip(["name", "thumbnail", "price", "address", "link"], row)} for row in result]

    hotelsRows = [[]]
    for index, hotel in enumerate(hotelsList):
        if index % 3 == 0:
            hotelsRows.append([])
        hotelsRows[-1].append(hotel)

    return flask.render_template(
        "hotels.html",
        config = config,
        hotels = hotelsRows
    )

@app.route("/transport", methods = ["GET"])
@limiter.limit("1/second")
def transport():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    response = requests.get("https://www.thrillophilia.com/mysore-tourist-places").text
    transport = response.split("<div class=\"tab-heading\">Flights</div>")[1].split("<div id=\"news\" class=\"tabcontent tab-wrap\" tab-active=news>")[0]

    flightsInfo = [transport.split("<span class=\"tab-content\"><p>")[1].split("</p></span>")[0].strip()]
    localTransportInfo = [transport.split("<span class=\"tab-content\"><p>")[2].split("</p></span>")[0].strip()]

    return flask.render_template(
        "transport.html",
        config = config,
        flightsInfo = flightsInfo,
        localTransportInfo = localTransportInfo
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

@app.route("/about", methods = ["GET"])
@limiter.limit("5/second")
def about():
    args = flask.request.args
    data = flask.request.get_data(as_text = True)
    cookies = flask.request.cookies
    headers = flask.request.headers
    method = flask.request.method
    ip = flask.request.remote_addr

    return flask.render_template(
        "about.html",
        config = config,
        googleMapsEmbedUrl = getGoogleMapsEmbedUrl("Mysore, Karnataka, India")
    )

@app.errorhandler(404)
def not_found(e):
    path = flask.request.path
    if path.startswith("/get-image/"):
        url = urllib.parse.unquote_plus(path[len("/get-image/"):])
        print(url)

        if not url.startswith("https://starofmysore.com/wp-content/uploads"):
            return ""

        response = requests.get(url)

        response = flask.make_response(response.content)
        response.headers.set("Content-Type", "image/jpeg")
        response.headers.set("Content-Disposition", "attachment", filename = "image.jpg")

        return response

    return "<h1>Under construction.</h1>", 404

app.run(
    host = config.ip,
    port = config.port,
    debug = True
)
