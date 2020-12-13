import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

name = "To Ban Or Not To Ban?"
description = "By Dr. R. Balasubramaniam The recent Deepavali festival saw the Government of Karnataka vacillate between wanting to ban firecrackers and not wanting to ban it. Chief Minister B.S. Yediyurappa initially announced that his Government was considering a ban but went back on this a few days later. The expert committee for managing the COVID pandemic"
thumbnail = "03.jpg"
articleLink = "https://starofmysore.com/to-ban-or-not-to-ban/"

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Articles (
                name,
                description,
                thumbnail,
                articleLink
            ) VALUES (%s, %s, %s, %s)
        """, (
            name,
            description,
            thumbnail,
            articleLink,
        ))
        database.commit()
