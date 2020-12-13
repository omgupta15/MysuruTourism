import mysql.connector, os

def getDatabase():
    return mysql.connector.connect(
        host = "localhost",
        user = os.environ.get("MySQL_username"),
        passwd = os.environ.get("MySQL_password"),
        database = "MysuruTourism"
    )

# name = "Sri Chamundeshwari Temple"
# placeId = name.lower().replace(" ", "-").replace(",", "")
# shortDescription = "Located on the top of the peak this is not only a sacred place but also caters to the 360-degree view of the city and one of the famous places to visit in Mysore. Homing the deity of Goddess Durga, devotees from all over the map come here to seek her blessings."
# description = """
# Sri Chamundeshwari Temple is about 13 kms from Mysuru, which is a prominent city in Karnataka State, India. Sri Chamundeshwari Temples is famous not only in India but also abroad. Atop of the hill the famous Sri Chamundeswari Temple. ‘Chamundi’ or ‘Durga’ is the fierce form of ‘Shakti’. She is the slayer of demons, ‘Chanda’ and ‘Munda’ and also ‘Mahishasura’, the buffalow-headed monster.

# She is the tutelary deity of the Mysuru Maharajas and the presiding deity of Mysuru. For several centuries they have held the Goddess, Chamundeswari, in great reverence.

# ‘Skanda Purana’ and other ancient texts mention a sacred place called ‘Trimuta Kshetra’ surrounded by eight hills. Lying on the western side is the Sri Chamundeshwari Temples, one among the eight hills. In the earlier days, the Hill was identified as ‘Mahabaladri’ in honour of God Shiva who resides in the ‘Mahabaleswara Temple’. This is the oldest temple on the hills.

# In the later days, the hill came to be known as ‘Sri Chamundeshwari Temples’ in honour of the Goddess Chamundi, the chief subject of the ‘Devi Mahathme’. The Goddess is believed to be an incarnation of Parvati, the consort of Lord Shiva. A large number of devotees from all over the country and from abroad visit the temple every year. They believe that the Goddess fulfills their desires and aspirations.

# Sri Chamundeshwari Temples rises to a height of 3,489 feet MSL and is visible from a distance itself while traveling towards Mysuru. There is a good motorable road to the top. Besides from Mysuru side, there is also a motorable road from its rear side, the Nanjangud side. Bus facilities are available to visit the hills. Karnataka State Road Transport Corporation (KSRTC) operates regular bus services every day for the convenience of pilgrims and others.
# """
# thumbnail = "18.webp"
# images = "19.jpg,20.jpg,21.jpg,22.jpg,23.jpg,24.jpg,25.jpg"
# timings = "7:30 AM to 2:00 PM, 3:30 PM to 6:00 PM, 7:30 PM to 9:00 PM"
# address = "Chamundeshwari Temple, Chamundi Hill, Mysuru, Karnataka 570010, India"
# location = "Sri Chamundeshwari Temple, Chamundi Hill, Mysuru, Karnataka 570010, India"

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
