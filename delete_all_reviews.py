import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

with getDatabase() as database:
    with database.cursor() as cursor:
        cursor.execute("DELETE FROM Reviews")
        database.commit()
