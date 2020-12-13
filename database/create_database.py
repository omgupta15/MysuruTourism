import mysql.connector, os

def connectToMySQL():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password")
    )

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

with connectToMySQL() as sql:
    with sql.cursor() as cursor:
        cursor.execute("CREATE DATABASE MysuruTourism;")
        sql.commit()

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE PlacesToVisit (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,
                name TEXT,
                placeId LONGTEXT,
                shortDescription TEXT,
                description LONGTEXT,
                thumbnail LONGTEXT,
                images LONGTEXT,
                timings TEXT,
                address TEXT,
                location TEXT
            );
        """)
        database.commit()

# with getDatabase() as database:
#     with database.cursor() as cursor:
#         cursor.execute("""
#             CREATE TABLE Hotels (
#                 id BIGINT PRIMARY KEY AUTO_INCREMENT,
#                 name TEXT,
#                 hotelId LONGTEXT,
#                 rating INT, -- out of 5
#                 price TEXT,
#                 description LONGTEXT,
#                 thumbnail LONGTEXT,
#                 images LONGTEXT,
#                 address TEXT,
#                 location TEXT,
#                 trivagoLink LONGTEXT
#             )
#         """)
#         database.commit()

# with getDatabase() as database:
#     with database.cursor() as cursor:
#         cursor.execute("""
#             CREATE TABLE Articles (
#                 id BIGINT PRIMARY KEY AUTO_INCREMENT,
#                 name TEXT,
#                 description LONGTEXT,
#                 thumbnail LONGTEXT,
#                 articleLink LONGTEXT
#             )
#         """)
#         database.commit()

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE Reviews (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,
                name TEXT,
                review LONGTEXT,
                added BIGINT,
                rating INT,
                placeId BIGINT,
                blocked BOOLEAN
            )
        """)
        database.commit()
