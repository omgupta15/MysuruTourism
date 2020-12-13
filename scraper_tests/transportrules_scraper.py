import requests

response = requests.get("https://www.thrillophilia.com/mysore-tourist-places").text

transport = response.split("<div class=\"tab-heading\">Flights</div>")[1].split("<div id=\"news\" class=\"tabcontent tab-wrap\" tab-active=news>")[0]

print(transport)

flightsInfo = transport.split("<span class=\"tab-content\"><p>")[1].split("</p></span>")[0].strip()
print(flightsInfo)

localTransportInfo = transport.split("<span class=\"tab-content\"><p>")[2].split("</p></span>")[0].strip()
print(localTransportInfo)

print("\n")
