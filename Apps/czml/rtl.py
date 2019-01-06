# coding=utf-8
import socket 
import re
import json
import mysql.connector
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
#Truncate Table
cursor.execute("Truncate rtl_recv;")
#Config TCP Scoket
s=socket.socket()
s.connect(('127.0.0.1',31000))
buffer = []
#Config RE pattern 
location_re = r'[0-9]{0,3}\.[0-9]{4,6},[0-9]{0,3}\.[0-9]{4,6}'
ICAO_re = r'[a-zA-Z0-9]{6}'
height_re = r'[0-9]{5}'
date_re = r'[0-9]{4}/[0-9]{2}/[0-9]{2}'
time_re = r'[0-9]{2}:[0-9]{2}:[0-9]{2}'
longitude_re = r'[0-9]{3}\.[0-9]{5,6}'
latitude_re = r'[0-9]{2}\.[0-9]{5,6}'

plane = {}
while True:
    #Receiving msg data
    d = s.recv(1024)
    a = d.decode('utf-8')
    print(d)
    #Search pattern 
    location = re.search(location_re,a)
    ICAO = re.search(ICAO_re,a) 
    height = re.search(height_re,a[50:])
    date = re.search(date_re,a)
    time = re.search(time_re,a)
    longitude = re.search(longitude_re,a)
    latitude = re.search(latitude_re,a)
    if ICAO:
        ICAO_string = ICAO.group()
        try:
            print(plane[ICAO_string])
        except:
            plane[ICAO_string] = 0
            sql = "insert into rtl_recv (ICAO,longitude,latitude,altitude,date,time) values (\'" + ICAO_string + '\','
        else:
            plane[ICAO_string] = 1
            sql = "update rtl_recv set "
    if location:
        location_string = location.group()
        if (not plane[ICAO_string]):
            sql +=longitude.group() + ',' + latitude.group() + ','
        else:
            sql +="longitude=" + longitude.group() + ",latitude=" + latitude.group() + ','
    else:
        if (not plane[ICAO_string]):
            sql +="0,0,"
    if height:
        height_string = height.group()
        if (not plane[ICAO_string]):
            sql +=height_string + ','
        else:
            sql +="altitude=" + height_string +','
    else:
        if (not plane[ICAO_string]):
            sql +="0,"
    if date:
        date_string = date.group()
        if (not plane[ICAO_string]):
            sql +='\'' +date_string + '\','
        else:
            sql +="date=\'" + date_string +'\','
    if time:
        time_string = time.group()
        if (not plane[ICAO_string]):
            sql +='\''+ time_string +'\');'
        else:
            sql +="time=\'" + time_string +'\''
    if (plane[ICAO_string]):
        sql+=" where ICAO=\'"+ICAO_string + '\';'
    print(sql)
    cursor.execute(sql)
    sql = "delete from rtl_recv where (CURRENT_TIMESTAMP-update_time)>20;"
    cursor.execute(sql)
cnx.close()