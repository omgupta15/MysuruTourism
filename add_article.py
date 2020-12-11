import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

name = ""
description = ""
thumbnail = ""
articleLink = ""

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
