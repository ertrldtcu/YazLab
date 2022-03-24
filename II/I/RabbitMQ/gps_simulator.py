import sqlite3
import threading
import time

import pika
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)


sqlite = sqlite3.connect("C:\\Users\\edutc\\Desktop\\YazLab\\II\\I\\database.db", check_same_thread=False)
cars = sqlite.cursor().execute("SELECT carid FROM user_car").fetchall()
if cars:
    print("Araç verileri aktarılıyor..")


    def publish_datas(carid):

        rabbit = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = rabbit.channel()

        channel.exchange_declare(exchange='datas', exchange_type='fanout')

        carid = carid[0]

        gps_datas = open("allCars_clean.csv", "r")

        for line in gps_datas:
            line = line.replace("\n", "")
            line_datas = line.split(",")
            if int(line_datas[3]) == carid and redis_client.hexists(carid, line_datas[0]) != 1:
                channel.basic_publish(exchange='datas', routing_key='', body=line.encode())
                print("PUBLISHED:", line_datas[3], line_datas[0], str(line_datas[1]), str(line_datas[2]))
                time.sleep(1)


    for car_id in cars:
        threading.Thread(target=publish_datas, args=(car_id,)).start()
else:
    print("Veritabanında araç bulunamadı..")

sqlite.close()
