import requests

response = requests.get(
    "https://www.trivago.in/mysore-94410/hotel",
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }).text

topHotels = response.split("<h2 class=\"h2\">Top hotels</h2>")[1].split("<div class=\"trvsc_toplist_more trvsc_more_top_hotels\">")[0]
topHotels = topHotels.split("<a href=\"")[1:]

for hotel in topHotels:
    link = hotel.split("\"")[0]
    thumbnail = "http://" + hotel.split("<img data-src=\"//")[1].split("\"")[0]
    name = hotel.split("<div class=\"trvsc_path_info\"><strong class=\"trvsc_path_name\">")[1].split("</strong>")[0]
    price = hotel.split("&lrm;")[1].split("</strong>")[0]
    
    print(f"""{name}
Link: {link}
Thumbnail: {thumbnail}
Price: {price}
""")
