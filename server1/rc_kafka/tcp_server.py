from kafka  import KafkaProducer
from kafka  import KafkaConsumer
from socket import *

import threading
import tcp_thread
import time
import sys

KAFKA_SERVERS  = '172.16.0.21:9092'
API_VERSION    = (0, 10, 1)

IP_ADDRESS     = '172.16.0.21'
PORT_NUM       = 7070
server_address = (IP_ADDRESS, PORT_NUM)

def KafkaConsumerThread(n):
    global control, cmdflag

    # connect kafka consumer
    consumer = KafkaConsumer(
            bootstrap_servers = KAFKA_SERVERS,
            auto_offset_reset = 'latest',
            group_id          = 'consumer02',
            api_version       = API_VERSION)
    consumer.subscribe('control-kafka')
    print("Kafka Consumer Thread Connected ")

    for msg in consumer :
        try:
            jsonData = json.loads(msg.value)
            lcbuf    = jsonData['CTL']
            lcid     = lcbuf[0]             # lcid

            tcp_thread.cmdflag[lcid] = lcid
            tcp_thread.control       = lcbuf

        except Exception as e:
            print ("consumer02 error", e)

if __name__ == "__main__":

    print("LOCAL CONTROLLER : client start")

#    sem = threading.Semaphore(1)
    t = threading.Thread(target=KafkaConsumerThread, args=(0, ))
    t.start()

#    t = threading.Thread(target=tcp_thread.tcp_MonitorThread, args=(0, ))
#    t.start()

    lc_address = ['10.2.0.11','10.2.0.12','10.2.0.13','10.2.0.14','10.2.0.15',
                  '10.2.0.16','10.2.0.17','10.2.0.18','10.2.0.19','10.2.0.20',
                  '10.2.0.21','10.2.0.22','10.2.0.23','10.2.0.24','10.2.0.25',
                  '10.2.0.26','10.2.0.27','10.2.0.28','10.2.0.29','10.2.0.30',
                  '10.2.0.31','10.2.0.32','10.2.0.33','10.2.0.34','10.2.0.35',
                  '10.2.0.36','10.2.0.37','10.2.0.38','10.2.0.39','172.16.0.21']
    try:
        # while True:
        #     conn, addr = server.accept()    # connection request
        #     print(time.strftime('%X', time.localtime()), "client addr = ", addr)
        #
        #     for lcid in range(30):
        #         if addr[0] == lc_address[lcid]: break
        #
        #     t = threading.Thread(target=tcp_thread.tcp_serverThread, args=(lcid + 1, conn))
        #     t.start()
        #

        # for lcid in range(30):
        #     t = threading.Thread(target=tcp_thread.tcp_clientThread, args=(lcid + 1, lc_address[lcid]))
        #     t.start()
        t = threading.Thread(target=tcp_thread.tcp_clientThread, args=(30, '172.16.0.21'))
        t.start()
        print("LOCAL CONTROLLER ip ->", '172.16.0.21')

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt ~~, server socket close")
