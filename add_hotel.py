import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

# name = ""
# hotelId = name.lower().replace(" ", "-").replace(",", "")
# rating = 
# price = ""
# description = """

# """
# thumbnail = ""
# images = ""
# address = ""
# location = ""
# trivagoLink = ""

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Hotels (
                name,
                hotelId,
                rating,
                price,
                description,
                thumbnail,
                images,
                address,
                location,
                trivagoLink
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name,
            hotelId,
            rating,
            price,
            description,
            thumbnail,
            images,
            address,
            location,
            trivagoLink,
        ))
        database.commit()
