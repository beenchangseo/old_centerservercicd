from kafka import KafkaConsumer, KafkaProducer

import json
import sysv_ipc
import sys
import threading
import time

KAFKA_SERVERS  = '172.16.0.201:9092'
API_VERSION    = (0, 10, 1)

def hex_dump(msg, buf):
    for value in buf: msg += " %02X" %value
    print(msg)

def shm_write(lcid, control, db_memory, s_memory):
    memory = bytearray(s_memory.read())         # shared memory read

    memory[64] = len(control)
    memory[65: 65 + memory[64]] = control

    if memory[65]  == 0x40:         # clock download
        t = time.localtime()
        memory[66:66+7] = [t.tm_year % 100, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, t.tm_wday]
        memory[64] += 7

    s_memory.write(memory)
    hex_dump("[lcid=%d] control -> " %lcid, memory[64 : 65 + memory[64]])

def publish_message(producer, topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode())
    except Exception as e:
        print('Exception in publishing message ->', e)

def tcp_MonitorThread(n):
    global shmkey

    print("Communication Monitor Thread start .....")

    kafka_producer = KafkaProducer(
                bootstrap_servers = KAFKA_SERVERS,
                api_version       = API_VERSION)

    # initial avriable
    err_count  = [0] * 50
    comm_count = [0] * 50
    lc_msg     = [0] * 64

    while threading.main_thread().is_alive():

        for lcid in range(10):
            memory = bytearray(shmkey[lcid].read())       # shared memory read
#            print("comm_count[lcid=%d] = "%(lcid+1), memory[63])
            if memory[63] == comm_count[lcid]:
                err_count[lcid] += 1
            else:
                err_count[lcid]  = 0
                comm_count[lcid] = memory[63]

            if err_count[lcid] > 30:
                if err_count[lcid] == 61:
                    print("comm_fail : lcid = ", lcid+1)
                    lc_msg[0:8] = memory[0:8]
                    lc_msg[0] = lcid+1
                    lc_msg[7] |= 0x40
                    publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg)
                    err_count[lcid] = 99

        time.sleep(1)

    print("KeyboardInterrupt ~~, TCP_Monotor Thread stop ~~~ [lcid=%d]" %lcid)
    kafka_producer.close()
    return

if __name__ == "__main__":

    # connect kafka consumer
    consumer = KafkaConsumer(
            bootstrap_servers = KAFKA_SERVERS,
            auto_offset_reset = 'latest',
            group_id          = 'consumer05',
            api_version       = API_VERSION)
    consumer.subscribe('control-kafka')
    print("Kafka Consumer Thread Connected ")

    # get SharedMemory key
    # shmkey = []
    # for lcid in range(30):
    #     shmkey.append(sysv_ipc.SharedMemory(0x1000 + lcid))
    #     print("lcid = %d" %lcid, shmkey[lcid])

    # t = threading.Thread(target=tcp_MonitorThread, args=(lcid, ))
    # t.start()

    s_memory  = sysv_ipc.SharedMemory(0x1000, flags = sysv_ipc.IPC_CREAT, size = 512)

    # read control command
    for msg in consumer :
        try:
            jsonData = json.loads(msg.value)
            control  = jsonData['CTL']
            lcid     = control[0]

            print("code=%x" %control[4], control[:20])

            memory = bytearray(s_memory.read())         # shared memory read

            # while(memory[0]): time.sleep(0.1)

            memory[0 :] = control
            s_memory.write(memory)

#            print("[lcid=%d] control -> " %(control[0], control[4]), control)

            # if control[4]  == 0x40:         # clock download
            #     t = time.localtime()
            #     memory[66:66+7] = [t.tm_year % 100, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, t.tm_wday]
            #     memory[64] += 7

        except Exception as e:
            print ("consumer05 error", e)
