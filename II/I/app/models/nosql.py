import redis
import pika
import threading

redis_client = redis.Redis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)


def create_car(carid):  # redis'e id için hash ekleyecek
    if is_car_exists(carid):
        return False
    return redis_client.hset(carid, carid, carid) == 1


def is_car_exists(carid):  # redis'te id için hash var mı bakacak
    return redis_client.exists(carid) == 1


def add_car_data(carid, date, lat, lang):  # verilen bilgiler için araca veri ekleyecek
    return redis_client.hset(carid, date, str(lat) + "," + str(lang)) == 1


def get_car_first_date(carid):
    first_date = get_car_last_date(carid)
    if redis_client.exists(carid):
        dates = redis_client.hkeys(carid)
        if len(dates) > 1:
            for date in dates:
                if date == carid:
                    continue
                first_date = date if date < first_date else first_date
    else:
        redis_client.hset(carid, carid, carid)
    return first_date


def get_car_last_date(carid):
    last_date = "0000-00-00 00:00"
    if redis_client.exists(carid):
        dates = redis_client.hkeys(carid)
        if len(dates) > 1:
            for date in dates:
                last_date = date if date > last_date else last_date
    else:
        redis_client.hset(carid, carid, carid)
    return last_date


def get_car_data(carid, date_start, date_end=None):  # o tarihteki verileri çekcek
    if is_car_exists(carid):
        if date_end is not None:
            datas = []
            dates = redis_client.hkeys(carid)
            for date in dates:
                if date_start <= date <= date_end:
                    datas.append([date, redis_client.hget(carid, date)])
            only_latlang = []
            datas = sorted(datas, key=lambda x: x[0])
            for v in datas:
                v = v[1].split(",")
                only_latlang.append([v[0], v[1]])
            return only_latlang

        else:
            return redis_client.hget(carid, date_start)
    return False


# RABBITMQ MESSAGE RECEIVING
class PikaReceiver:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange="datas", exchange_type='fanout')

    def consume(self, callback):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange="datas", queue=queue_name)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


def start_consumer():
    def callback(_, __, ___, body):
        datas = body.decode().split(",")
        add_car_data(datas[3], datas[0], datas[1], datas[2])
        print("CONSUMED:", datas[3], datas[0], datas[1], datas[2])

    with PikaReceiver() as consumer:
        consumer.consume(callback=callback)


consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()
