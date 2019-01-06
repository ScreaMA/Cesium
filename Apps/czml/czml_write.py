# coding=utf-8
import mysql.connector
import time
from czml import czml
def init():
    packet1 = czml.CZMLPacket(id='document',version='1.0')
    doc.packets.append(packet1)
# Generate packet_document
# function to create packet
def create(ICAO,longitude,latitude,height):
    packet2 = czml.CZMLPacket(id = ICAO)
    lb = czml.Label(text=ICAO,show=True)
    lb.scale=0.5
    #lb.pixelOffset = {'cartesian2':[20,-20]}
    packet2.label=lb
    packet2.position ={"cartographicDegrees" : [longitude,latitude,height]}
    md = czml.Model()
    md.gltf = "../../Models/a2100.gltf"
    md.maximumScale = 20000
    md.minimumPixelSize = 64
    packet2.model = md
    doc.packets.append(packet2)

#Config Mysql DB
try:
    config = {
    'user': 'root',
    'password': '123456',
    'host': '47.107.248.138',
    'database': 'plane',
    'raise_on_warnings': True
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cnx.autocommit=True
except:
    print("DB ERROR")
else:
    print("DB Connection OK")
sql = "select * from rtl_recv"
while (1):
    time.sleep(1)
    doc = czml.CZML()
    init()
    cursor.execute(sql)
    for obj in cursor:
        ICAO = obj[1]
        longitude = obj[2]
        latitude = obj[3]
        height =obj[4]
        create(ICAO,longitude,latitude,height)
        # Write the CZML document to a file
        filename = "test.czml"
        doc.write(filename)
    print("Update OK!")
