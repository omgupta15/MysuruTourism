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

placesToVisit = [(1, 'Mysore Palace', 'mysore-palace', 'The second most famous attraction in India, first being the Taj Mahal, Mysore Palace is easily one of the most imposing architectural buildings in the country.', 'The second most famous attraction in India, first being the Taj Mahal, Mysore Palace is easily one of the most imposing architectural buildings in the country. It is amazing that the palace was only built in the 20th century and is the fourth structure to be constructed on the same location.\n\nAlso known as Amba Vilas Palace, it is one of the seven palaces in the City of Palaces. Often mistaken for a Gothic structure, the Palace is, in fact, an exemplary showcase of Indo-Saracenic architecture with a blend of Gothic, Rajput, Hindu and Muslim styles and it is one of the famous places to visit in Mysore.\n\nThere are four awe-inspiring arched gates to enter the massive garden area that engulfs the Palace. Some of the important places to visit here are the Ambavilasa, the Durbar Hall, and the Royal Howdah. The Palace is a spectacle come every evening when it is lit with approximately 97,000 lights.', '01.webp', '01.webp,02.jpg,03.jpg,04.jpg,05.jpg,06.jpg', '10:00 AM to 5:30 PM', 'Sayyaji Rao Road, Agrahara, Chamrajpura, Mysuru, Karnataka 570001, India', 'Mysore Palace, Sayyaji Rao Road, Agrahara, Chamrajpura, Mysuru, Karnataka 570001, India'), (2, 'Brindavan Gardens', 'brindavan-gardens', 'It is a major tourist attraction for all the Mysore and KRS dam visitors. It is also regarded as one of the most beautiful gardens in the state of Karnataka.', 'Brindavan Gardens of Mysore is undeniably one of the best terrace gardens in the world. A must sightseeing place of a Mysore tour, Brindavan Garden mesmerizes everyone. It is located about 12km towards the north west of the Mysore city. Brindavan gardens with its illuminated fountains, botanical park, extensive varieties of plants and fulfilled boating, is place for everyone.\n\nEspecially famous for its symmetric design and illuminate terrace gardens, Brindavan Gardens was built by Sir Mirza Ismail, the then diwan of Mysore state. He was the brain behind its modelling and conceptualization. Spread across an area of more than 60 acres, this garden is laid out in three terraces, and ends in a horseshoe shape.\n\nA visit to Brindavan Gardens becomes even more enjoyable with the boat rides. As there is River Cauvery between North Brindavan and South Brindavan facilities for boating are offered by the Karnataka State Tourism Development Corporation. Boating on the serene waters of the river, with the entrancing beauty of Brindavan gardens around you is sure to make a Mysore trip memorable.\n\nAnother popular feature of the Brindavan Gardens are the musical fountains. The fountains are maintained by the water pressure from the dam and are operated through a controller. The musical fountain show presents a harmonized water dance, accompanied by colourful lights and music. For visitors, a rain shelter and gallery has been built. This show organised at the North Brindavan.', '07.jpg', '07.jpg,08.jpg,09.jpg,10.jpg,11.jpg,12.jpg', '6:00 AM to 8:00 PM', 'Krishna Raja Sagara Dam, Srirangapatna, Mandya District, Karnataka, India', 'Brindavan Gardens, Krishna Raja Sagara Dam, Srirangapatna, Mandya District, Karnataka, India'), (3, "St. Philomena's Cathedral", "st.-philomena's-cathedral", 'Initially built as a small church was then reconstructed by Maharaja Krishnaraja Wodeyar. It is one among the largest Cathedrals in the whole of South Asia.', '\nWith the fame of being one of the largest churches in India, this majestic church captivates everyone with its architectural excellence. It also boasts of being the second largest church in Asia. Dedicated to Saint Philomena, St. Philomena’s Church is not only known for its architectural beauty and religious significance; it stands as an exemplary of secular viewpoint and the religious harmony which existed in Mysore. This can be seen from the fact that this church was built by Mysore ruler for the European residents in the city.\n\nConstructed in the Neo-Gothic or the Victorian style, this church draws its inspiration from the Cologne Cathedral of Germany. The church is said to be designed by a French artist Daly. This church has been made in the shape of a cross, with congregation hall also referred as ‘nave’ being the longest end of the cross, the transepts being the two arms of the cross, choir being the crossing and altar being the upper part or the smaller part of the cross.\n\nThe main attraction of the church is its twin spires with a height of 175 feet, which can be spotted even from mile away. The design of spires is similar to those in St. Patrick’s Church which is located in New York. Each spire has a cross adorned on it with a height of 12 feet. The altar presents a captivating view with intricately crafted marble and the statue of St. Philomena which was brought from France. At alar you will find statues of St. Philomena and beneath the altar, in the underground catacomb, relics of St. Philomena have been kept.\n', '13.jpg', '13.jpg,14.jpg,15.jpg,16.jpg,17.jpg', '5:00 AM to 6:00 PM', 'Lashkar Mohalla, Ashoka Road, Mysuru, Karnataka, 570001, India', "St. Philomena's Cathedral, Lashkar Mohalla, Ashoka Road, Mysuru, Karnataka, 570001, India"), (4, 'Sri Chamundeshwari Temple', 'sri-chamundeshwari-temple', 'Located on the top of the peak this is not only a sacred place but also caters to the 360-degree view of the city and one of the famous places to visit in Mysore. Homing the deity of Goddess Durga, devotees from all over the map come here to seek her blessings.', '\nSri Chamundeshwari Temple is about 13 kms from Mysuru, which is a prominent city in Karnataka State, India. Sri Chamundeshwari Temples is famous not only in India but also abroad. Atop of the hill the famous Sri Chamundeswari Temple. ‘Chamundi’ or ‘Durga’ is the fierce form of ‘Shakti’. She is the slayer of demons, ‘Chanda’ and ‘Munda’ and also ‘Mahishasura’, the buffalow-headed monster.\n\nShe is the tutelary deity of the Mysuru Maharajas and the presiding deity of Mysuru. For several centuries they have held the Goddess, Chamundeswari, in great reverence.\n\n‘Skanda Purana’ and other ancient texts mention a sacred place called ‘Trimuta Kshetra’ surrounded by eight hills. Lying on the western side is the Sri Chamundeshwari Temples, one among the eight hills. In the earlier days, the Hill was identified as ‘Mahabaladri’ in honour of God Shiva who resides in the ‘Mahabaleswara Temple’. This is the oldest temple on the hills.\n\nIn the later days, the hill came to be known as ‘Sri Chamundeshwari Temples’ in honour of the Goddess Chamundi, the chief subject of the ‘Devi Mahathme’. The Goddess is believed to be an incarnation of Parvati, the consort of Lord Shiva. A large number of devotees from all over the country and from abroad visit the temple every year. They believe that the Goddess fulfills their desires and aspirations.\n\nSri Chamundeshwari Temples rises to a height of 3,489 feet MSL and is visible from a distance itself while traveling towards Mysuru. There is a good motorable road to the top. Besides from Mysuru side, there is also a motorable road from its rear side, the Nanjangud side. Bus facilities are available to visit the hills. Karnataka State Road Transport Corporation (KSRTC) operates regular bus services every day for the convenience of pilgrims and others.\n', '18.webp', '19.jpg,20.jpg,21.jpg,22.jpg,23.jpg,24.jpg,25.jpg', '7:30 AM to 2:00 PM, 3:30 PM to 6:00 PM, 7:30 PM to 9:00 PM', 'Chamundeshwari Temple, Chamundi Hill, Mysuru, Karnataka 570010, India', 'Sri Chamundeshwari Temple, Chamundi Hill, Mysuru, Karnataka 570010, India')]

for place in placesToVisit:
    with getDatabase() as database:
        with database.cursor() as cursor:
            cursor.execute("INSERT INTO PlacesToVisit VALUES {}".format(place))
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
