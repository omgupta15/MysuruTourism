import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

# name = ""
# placeId = name.lower().replace(" ", "-").replace(",", "")
# shortDescription = ""
# description = """
#
# """
# thumbnail = ""
# images = ""
# timings = ""
# address = ""
# location = ""

######################################################################################

# name = input("Enter Place Name: ")
# placeId = name.lower().replace(" ", "-").replace(",", "")
# shortDescription = input("Enter Short Description: ")
# description = input("Enter description: ")
# thumbnail = input("Enter thumbnail file name: ")
# images = input("Enter image file names (Separated by coma): ")
# timings = input("Enter timings: ")
# address = input("Enter address: ")
# location = input("Enter location for Google Map Embed: ")

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PlacesToVisit (
                name,
                placeId,
                shortDescription,
                description,
                thumbnail,
                images,
                timings,
                address,
                location
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name,
            placeId,
            shortDescription,
            description,
            thumbnail,
            images,
            timings,
            address,
            location
        ))
        database.commit()
