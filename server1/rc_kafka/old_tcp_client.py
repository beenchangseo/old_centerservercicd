from kafka  import KafkaProducer, KafkaConsumer
from socket import *

import json
import sysv_ipc
import time
import threading
import sys
import pymysql

DATABASE_SERVERS = '172.16.0.202'
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
get_Ip_sql = "SELECT ip, Ver_2004 FROM local"
cursor.execute(get_Ip_sql)
rows = cursor.fetchall()
mydb.close()
KAFKA_SERVERS  = '172.16.0.201:9092'
API_VERSION    = (0, 10, 1)

# IP_ADDRESS     = '20.2.13.2'
PORT_NUM       = 7070
# server_address = (IP_ADDRESS, PORT_NUM)

BUFFER_SIZE    = 1024
SCAN_TIME      = 1.0

phase  = 0
sc     = 0
offset = 15
cycle  = 60
nano_det = [0,0,0,0]
thread_alive  = False
opcode = 0

def hex_dump(msg, buf):
    for value in buf: msg += " %02X" %value
    print(msg)

def gen_lrc(buf):
    lrc = 0
    for value in buf: lrc ^= value
    return lrc

def nano_client_thread(HOST, PORT):
    global nano_det, thread_alive

    print("Nano-Server Communication Server Start [ver. 2020.2.28]")
    nano_connection = False

    while thread_alive ==True:
        try:
            if not nano_connection:
                print("NANO connection request (host, port) = ", HOST, PORT)
                nano_client = socket(AF_INET, SOCK_STREAM)
                nano_client.connect((HOST, PORT))
                nano_connection = True

            rcvmsg = nano_client.recv(1024)
            if rcvmsg == None:
                if nano_connection == True: nano_client.close()
                nano_connection = False
                time.sleep(1)
                continue

            hex_dump("RXD : ", rcvmsg)
            nano_det[0] = rcvmsg[5]
            nano_det[1] = rcvmsg[6]

            sndmsg = [0x7e, 0x7e, 4, rcvmsg[3],0x06]
            sndmsg.append(gen_lrc(sndmsg))

            nano_client.send(bytearray(sndmsg))
            hex_dump("TXD : ", sndmsg)

        except Exception as e:
            print("NANO Socket connection Error -> ", e)
            if nano_connection == True: nano_client.close()
            nano_connection = False
            time.sleep(1)
            continue

    nano_client.close()     # ????????? ????????????.

def receive_packet(conn):
    global clientConnect, rcvmsg

    rcvmsg += conn.recv(BUFFER_SIZE)
    if len(rcvmsg) < 6: return rcvmsg

    if rcvmsg[0] != 0x7e or rcvmsg[1] != 0x7e or rcvmsg[2] == 255:
        rcvmsg = []
        return rcvmsg

    repeat = 0
    rxcnt  = rcvmsg[2] + 2
    while len(rcvmsg) < rxcnt:
        # print("this is while loop")
        time.sleep(0.2)
        rcvmsg += conn.recv(BUFFER_SIZE)
        repeat += 1
        print("repeat = ", repeat)
        if repeat > 10: return rcvmsg

    if gen_lrc(rcvmsg[:rxcnt]) != 0:
        hex_dump("[%s] RXD[Frame_err] :" %time.strftime('%X', time.localtime()), rcvmsg)
#        rcvmsg = rcvmsg[rxcnt:]
        rcvmsg = []     # 2021.2.24

    return rcvmsg

def make_txmsg(lcid):
    global memory, opcode

    BASE  = 64
    if memory[BASE] > 0:            # if server_command ?
        count = memory[BASE]
        memory[BASE] = 0
        sndmsg = [0x7e, 0x7e, 4, lcid % 16]
        for i in range(count):
            sndmsg.append(memory[BASE + 1 + i])

        if   sndmsg[4] == 0xB0: sndmsg += [0] * (161 - 57)      # dayplan down
        elif sndmsg[4] == 0xB4: sndmsg += [0] * (80 - 56)       # fuction table down
        elif sndmsg[4] == 0xC4: sndmsg += [0] * (224 - 56)

        sndmsg[2] = len(sndmsg) - 1
        sndmsg.append(gen_lrc(sndmsg))
        hex_dump("[lcid = %d] control_cmd -->" %lcid, sndmsg)
    else:
        # sndmsg = [0x7e, 0x7e, 4, lcid % 16, 0x12, 4 ^ (lcid % 16) ^ 0x12,
        #           0x7e, 0x7e, 4, lcid % 16, 0x42, 4 ^ (lcid % 16) ^ 0x42]
        opcode = (opcode + 1) & 1
        if opcode == 0: sndmsg = [0x7e, 0x7e, 4, lcid % 16, 0x12]
        else:           sndmsg = [0x7e, 0x7e, 4, lcid % 16, 0x42]
        sndmsg.append(gen_lrc(sndmsg))

    return sndmsg

def rcvmsg_handler(rcvmsg):
    global lc_msg, nano_det

    if rcvmsg[4] == 0x13:                   # LC status

        if rcvmsg[2] < 29 or rcvmsg[2] == 32:       # 4??? ????????? ?
            lc_msg[8:8+17] = rcvmsg[5:5+17]         # LC status
            lc_msg[24] |= 0x80                      # 4??? ????????? ??????

            lc_msg[26]  =  rcvmsg[11] & 0x01        # detector ch 1
            lc_msg[26] += (rcvmsg[11] & 0x02) << 1  # detector ch 2
            lc_msg[26] += (rcvmsg[11] & 0x04) << 2  # detector ch 3
            lc_msg[26] += (rcvmsg[11] & 0x08) << 3  # detector ch 4

        else:                                       # 3??? ?????????
            lc_msg[8:8+25] = rcvmsg[5:5+25]
            lc_msg[26]     = nano_det[0] & 0x03

    # calculate remain time
        phase  = (lc_msg[9] >> 5) + 1
        cycle  = lc_msg[20]
        offset = lc_msg[21]
        split  = 0
        for i in range(phase): split += lc_msg[35 + i]
        if cycle > 0:
            lc_msg[59] = (cycle + split - lc_msg[18]) % cycle

    elif rcvmsg[4] == 0x15:                     # LC status 2
        BASE = 5
        lc_msg[1] = rcvmsg[BASE + 50]          # year
        lc_msg[2] = rcvmsg[BASE + 51]          # month
        lc_msg[3] = rcvmsg[BASE + 52]          # day
        lc_msg[4] = rcvmsg[BASE + 53]          # hour
        lc_msg[5] = rcvmsg[BASE + 54]          # min
        lc_msg[6] = rcvmsg[BASE + 55]          # sec
        lc_msg[7] = (lc_msg[7] & 0xf0) + rcvmsg[BASE + 56]  # weekday

        lc_msg[8:8+7]   = rcvmsg[BASE + 2:  BASE +  2 + 7]  # status 1 - 7
        lc_msg[15:15+7] = rcvmsg[BASE + 10: BASE + 10 + 7]  # status 8 - 14
        lc_msg[22:22+7] = rcvmsg[BASE + 18: BASE + 18 + 7]  # status 15 - 21

        lc_msg[35:35+3] = rcvmsg[BASE + 30: BASE + 30 + 3]  # split 1 - 3
        lc_msg[38:38+7] = rcvmsg[BASE + 34: BASE + 34 + 7]  # split 4 - 8, 1 - 2
        lc_msg[45:45+6] = rcvmsg[BASE + 42: BASE + 42 + 6]  # split 3 - 8

        lc_msg[26]      = (rcvmsg[BASE + 61] & 0x03)        # detector 1
        lc_msg[26]     += (rcvmsg[BASE + 62] & 0x03) << 2   # detector 2
        lc_msg[26]     += (rcvmsg[BASE + 63] & 0x03) << 4   # detector 3
        lc_msg[26]     += (rcvmsg[BASE + 64] & 0x03) << 6   # detector 4

    elif rcvmsg[4] == 0x17:             # nano server (detector status)

        if   rcvmsg[3] == 1:
            lc_msg[26] = (lc_msg[26] & 0xFC) + (rcvmsg[5] & 0x03)
        elif rcvmsg[3] == 2:
            lc_msg[26] = (lc_msg[26] & 0xF3) + ((rcvmsg[5] & 0x03) << 2)
        elif rcvmsg[3] == 3:
            lc_msg[26] = (lc_msg[26] & 0xCF) + ((rcvmsg[5] & 0x03) << 4)
        else:
            lc_msg[26] = (lc_msg[26] & 0x3F) + ((rcvmsg[5] & 0x03) << 6)

    elif rcvmsg[4] == 0x23:             # detector information
        lc_msg[27:27+8] = rcvmsg[5+96:5+96+8]   # vol 1-8
        lc_msg[35:35+8] = rcvmsg[5+64:5+64+8]   # occ 1-8

        lc_msg[60] = (lc_msg[60] + 1) & 0x7f   # split upload

    elif rcvmsg[4] == 0x33:             # split
        lc_msg[43 : 43+8] = rcvmsg[5 : 5+8]     # vehicle split

        if rcvmsg[2] > 20:              # if 3??? ??????
            lc_msg[51 : 51+8] = rcvmsg[5+16 : 5+16+8]   # ped time

    elif rcvmsg[4] == 0x43:             # clock upload
        BASE = 4
        lc_msg[1] = rcvmsg[BASE + 1]    # year
        lc_msg[2] = rcvmsg[BASE + 2]    # month
        lc_msg[3] = rcvmsg[BASE + 3]    # day
        lc_msg[4] = rcvmsg[BASE + 4]    # hour
        lc_msg[5] = rcvmsg[BASE + 5]    # min
        lc_msg[6] = rcvmsg[BASE + 6]    # sec
        lc_msg[7] = (lc_msg[7] & 0xf0) + (rcvmsg[BASE + 7] & 0x0f)  # weekday


def publish_message(producer, topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode())
    except Exception as e:
        print('Exception in publishing message ->', e)

# -------------- main routine -----------------------

if len(sys.argv) < 2: lcid = 1
else:                 lcid = int(sys.argv[1]) % 100

if len(sys.argv) >= 3: debug = 1
else:                  debug = 0

print("L/C Communication Server Start [ver. 2020.2.28]")

# lc_address = ['10.2.0.11','10.2.0.12','10.2.0.13','10.2.0.14','10.2.0.15',
#               '10.2.0.16','10.2.0.17','10.2.0.18','10.2.0.19','10.2.0.20',
#               '10.2.0.21','10.2.0.22','10.2.0.23','10.2.0.24','10.2.0.25',
#               '10.2.0.26','10.2.0.27','10.2.0.28','10.2.0.29','10.2.0.30',
#               '10.2.0.31','10.2.0.32','10.2.0.33','10.2.0.34','10.2.0.35',
#               '10.2.0.36','10.2.0.37','10.2.0.38','14.51.232.216','10.2.0.40']

lc_address = []
V_2010     = []
for i in range(len(rows)):
    lc_address.append(rows[i][0])
    V_2010.append(rows[i][1])

if V_2010[lcid - 1] == 1:     # 2010?????? : 3??? ?????????
    thread = threading.Thread(target = nano_client_thread, args=(((lc_address[lcid - 1])[:-1] + '3'), 7080))
    thread_alive  = True
    thread.start()

s_memory  = sysv_ipc.SharedMemory(0x1000 + lcid, flags = sysv_ipc.IPC_CREAT, size = 128)

server_address = (lc_address[lcid - 1], PORT_NUM)
# print ("server_address = ", server_address)

clientConnect = 0

kafka_producer = KafkaProducer(
            bootstrap_servers = KAFKA_SERVERS,
            api_version       = API_VERSION)

logtime   = "00:00:00"
lc_msg    = [0] * 64
lc_msg[0] = lcid
rcvmsg = []

memory = bytearray(s_memory.read())       # shared memory read
for i in range(1, 64): lc_msg[i] = memory[i]
memory[64] = 0
s_memory.write(bytearray(memory))

while True:
    try:
        memory = bytearray(s_memory.read())       # shared memory read
        if memory[127] == 255:
            print("server command -> process terminate ~~")
            memory[127] = 0
            s_memory.write(memory)
            client.close()
            kafka_producer.close()
            sys.exit()

        if clientConnect == 0:
            client = socket(AF_INET, SOCK_STREAM)
            client.settimeout(10)
            print(server_address, "CONNECTION ?????????")
            client.connect(server_address)        # ???????????? ????????? ??????
            clientConnect = 1
            print(time.strftime('%X', time.localtime()), "server connected =", server_address)

        ####### make send message
        sndmsg = make_txmsg(lcid)

        s_memory.write(bytearray(memory))

        client.send(bytearray(sndmsg))
        if lcid == memory[127]: hex_dump("TXD :", sndmsg)
        # hex_dump("TXD :", sndmsg)

        time.sleep(SCAN_TIME)

        ####### Receive From HOST
        # rcvmsg = receive_packet(client)
        rcvmsg += client.recv(BUFFER_SIZE)

        while len(rcvmsg) >= 6:

            if rcvmsg[0] != 0x7e or rcvmsg[1] != 0x7e:
                rcvmsg = rcvmsg[1:]
                continue

            length = rcvmsg[2] + 2
            if len(rcvmsg) < length:
                break

            if gen_lrc(rcvmsg[0 : length]) != 0:
                rcvmsg = rcvmsg[length:]
                continue

#            hex_dump("RXD :", rcvmsg[0 : length])

            if rcvmsg[4] == 0x41 or rcvmsg[4] >= 0x50:      # clock & startup_code & DATABASE
                publish_message(kafka_producer, 'control-response', 'CTL_RPS', rcvmsg[3:rcvmsg[2] + 1])
                hex_dump("[lcid = %d] control_rps -->" %lcid, rcvmsg[:rcvmsg[2] + 2])
            else:
                rcvmsg_handler(rcvmsg)
                publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg)

            if lcid == memory[127]:
                hex_dump("RXD :", rcvmsg[:rcvmsg[2] + 2])

            lc_msg[63] = (lc_msg[63] + 1) & 0xff        # increment comm_count
            lc_msg[7] &= 0xBF                           # clear comm_fail

            rcvmsg = rcvmsg[rcvmsg[2] + 2:]

        # write to SharedMemory
        s_memory.write(bytearray(lc_msg))

    except Exception as e:
        print("Socket connection Error[lcid = %d]->" %lcid, e)
        if (lc_msg[7] & 0x40) == 0:
            lc_msg[7] |= 0x40                       # comm_fail
            print("comm_fail : lcid = ", lcid)
            print(lc_msg)
            publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg)
            s_memory.write(bytearray(lc_msg))        # write to SharedMemory

        clientConnect = 0
        client.close()
        time.sleep(5)
        continue

    except KeyboardInterrupt:
        print("keyboard interrupt~ stop TCP_Client")
        kafka_producer.close()
        client.close()
        thread_alive = False
        sys.exit()
