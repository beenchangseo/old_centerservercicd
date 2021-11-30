from kafka import KafkaProducer
from kafka import KafkaConsumer

import pymysql
import json
import sysv_ipc
import time

KAFKA_SERVERS    = '172.16.0.202:9092'
API_VERSION      = (0, 10, 1)
DATABASE_SERVERS = '172.16.0.202'

MAX_LC_COUNT = 5

comm_errcnt  = [1] * 100
comm_fail    = [-1] * 100
report_cycle = [0] * 100

pass_time   = 0

def put_event_log(cursor, log_time, device, id, event_code, event_status):

    print("PC-mysql : event-log  [id = %d]" %(id), log_time, event_code, event_status)

    try:
        querry = """INSERT INTO event_log(log_time, device, id, event_code, event_status)
            VALUES(%s, %d, %d, %d, %d)""" %(log_time, device, id, event_code, event_status)
        cursor.execute(querry)
    except Exception as e:
        print('Exception in putting event_log')
        print(e)

def put_cycle_log(cursor, lcbuf):
    global report_cycle

    lcid = lcbuf[0] - 1

    ## 21.11.30 코드 수정 ##
    # if report_cycle[lcid] == lcbuf[60]: return
    # report_cycle[lcid] = lcbuf[60]                

    ## 21.11.30 코드 수정 ##
    if lcbuf[61] == 0x23 : 
        log_time = "'20%02d-%02d-%02d %02d:%02d:%02d'" %(lcbuf[1], lcbuf[2], lcbuf[3], lcbuf[4], lcbuf[5], lcbuf[6])
        cycle    = lcbuf[19]
        offset   = lcbuf[21]
        split    = lcbuf[43:43+16]      # split 1-8, ped_time 1-8

        vol      = lcbuf[27:27+8]
        occ      = lcbuf[35:35+8]

        if cycle == 0: return

        print("PC-mysql : cycle_log  [id = %d]" %(lcid + 1), log_time, cycle, offset, split[0:8], split[8:16])
        print("PC-mysql : detect_log [id = %d]" %(lcid + 1), log_time, vol, occ)

        try:
            querry = """INSERT INTO cycle_log(log_time, id, cycle, offset, split_1, split_2, split_3, split_4, split_5, split_6, split_7, split_8,
                    ped_1, ped_2, ped_3, ped_4, ped_5, ped_6, ped_7, ped_8)
                    VALUES(%s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)""" %(log_time, lcid + 1, cycle, offset,
                    split[0], split[1], split[2],   split[3],  split[4],  split[5],  split[6],  split[7],
                    split[8], split[9], split[10], split[11], split[12], split[13], split[14], split[15])
            cursor.execute(querry)

            querry = """INSERT INTO detect_log(log_time, id, vol_1, occ_1, vol_2, occ_2, vol_3, occ_3, vol_4, occ_4,
                    vol_5, occ_5, vol_6, occ_6, vol_7, occ_7, vol_8, occ_8)
                    VALUES(%s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)""" %(log_time, lcid + 1,
                    vol[0], occ[0], vol[1], occ[1], vol[2], occ[2], vol[3], occ[3],
                    vol[4], occ[4], vol[5], occ[5], vol[6], occ[6], vol[7], occ[7])
            cursor.execute(querry)

        except Exception as e:
            print('Exception in putting cycle_log')
            print(e)

def publish_message(producer, topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode())
    except Exception as e:
        print('Exception in publishing message')
        print(e)

def check_lc_event(cursor, lcbuf, kafka_producer):
    global lc_status

    lcid = lcbuf[0] - 1

    current  = (lcbuf[7] >> 4) + (lcbuf[8] & 0xe0)  # code 0  - 7
    current += (lcbuf[11]) << 8                     # code 8  - 15
    current += (lcbuf[12] & 0x8f) << 16             # code 16 - 23

    xor     = lc_status[lcid] ^ current
    lc_status[lcid] = current

    t = time.localtime()
    log_time = "'%04d-%02d-%02d %02d:%02d:%02d'" %(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    for i in range(32):
        if xor & 0x000001:
            event_code  = i
            event_state = current & 0x000001
            put_event_log(cursor, log_time, 2, lcid + 1, event_code, event_state)
            publish_message(kafka_producer, 'event-log', 'LOG', [log_time, 2, lcid + 1, event_code, event_state])

        current = current >> 1
        xor     = xor >> 1

    return


if __name__ == '__main__':

    # MySQl connection
    mydb = pymysql.connect(
            host              = DATABASE_SERVERS,
            port              = 3306,
            user              = "atcs02",
            password          = "xhdtlsqhdks1",
            db                = "tcs_database",
            charset           = "utf8"
            )
    cursor  = mydb.cursor()

    # Connect KafkaConsumer
    consumer = KafkaConsumer(
            bootstrap_servers = KAFKA_SERVERS,
            auto_offset_reset = 'latest',
            group_id          = 'consumer01',
            api_version       = API_VERSION )
    consumer.subscribe(['local-kafka'])

    # Connect KafkaProducer
    kafka_producer = KafkaProducer(
            bootstrap_servers = KAFKA_SERVERS,
            api_version       = API_VERSION)
    print("connecting kafka ~~")

    # logging Server Start
    t = time.localtime()
    log_time = "'%04d-%02d-%02d %02d:%02d:%02d'" %(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    print("MySQL Server started ", log_time)

    put_event_log(cursor, log_time, 1, 1, 99, 1)
    mydb.commit()

    publish_message(kafka_producer, 'event-log', 'LOG', [log_time, 1, 1, 99, 1])

    # initial variable
    lc_status = [0] * 50
    for lcid in range(30):
        s_memory = sysv_ipc.SharedMemory(0x1001 + lcid, flags = sysv_ipc.IPC_CREAT, size = 128)
        memory = s_memory.read()
        lc_status[lcid]    = (memory[7] >> 4) + (memory[8] & 0xe0)    # code 0  - 7
        lc_status[lcid]   += (memory[11] << 8)                        # code 8  - 15
        lc_status[lcid]   += (memory[12] & 0x8f) << 16                # code 16 - 23
        report_cycle[lcid] = memory[60]

    for msg in consumer :
        try:
            jsonData = json.loads(msg.value)

            lcbuf = jsonData['STS']
            check_lc_event(cursor, lcbuf, kafka_producer)
            put_cycle_log(cursor, lcbuf)
            mydb.commit()

        except Exception as e:
            print(e)
            continue

    mydb.close()
