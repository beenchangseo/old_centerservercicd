from kafka  import KafkaProducer
from socket import *

import json
import sysv_ipc
import time
import threading

KAFKA_SERVERS  = '172.16.0.21:9092'
API_VERSION    = (0, 10, 1)

BUFFER_SIZE    = 1024

lc_msg_array = [[0]*64] * 50
cmdflag    = [0] * 50
control    = [0,0,0,0,0]

def hex_dump(msg, buf):
    for value in buf: msg += " %02X" %value
    print(msg)

def genlrc(buf):
    lrc = 0
    for value in buf: lrc ^= value
    return lrc

def get_command(lc_msg):
    global control

    if control[4]   == 0x10:    # 제어모드 명령
        control += [0,0,0]
    elif control[4] == 0x40:    # clock download
        t = time.localtime()
        control += [t.tm_year % 100, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, t.tm_wday]
    elif control[4] == 0x50:    # 특수 제어
        if (lc_msg[24] & 0x80) == 0: control += [0]*17      # 3색 제어기
        else:                        control += [0]*4
    elif control[4] == 0xA0:    # startup code download
        if (lc_msg[24] & 0x80) == 0: control += [0]*17      # 3색 제어기
    else:
        pass
    return control[4:]

####### make send message
def make_txmsg(lcid, opcode):
    global cmdflag

    sndmsg = [0x7e, 0x7e, 4, lcid, opcode]

    if cmdflag[lcid] != 0:
        cmdflag[lcid] = 0           # clear command flag
        sndmsg[4:] += get_command(lc_msg)
        sndmsg[2]  += len(sndmsg) - 1
        print("[lcid = %d] control -->" %lcid, sndmsg)

    sndmsg.append(genlrc(sndmsg))           # add lrc

    return sndmsg

def rcvmsg_handler(rcvmsg, lc_msg):

    if rcvmsg[4] == 0x13:                   # LC status

        if rcvmsg[2] < 29 or rcvmsg[2] == 32:       # 4색 제어기 ?
            lc_msg[8:8+17] = rcvmsg[5:5+17]         # LC status
            lc_msg[24] |= 0x80                      # 4색 제어기 표시

            lc_msg[26]  =  rcvmsg[11] & 0x01        # detector ch 1
            lc_msg[26] += (rcvmsg[11] & 0x02) << 1  # detector ch 2
            lc_msg[26] += (rcvmsg[11] & 0x04) << 2  # detector ch 3
            lc_msg[26] += (rcvmsg[11] & 0x08) << 3  # detector ch 4

        else:                                       # 3색 제어기
            lc_msg[8:8+25] = rcvmsg[5:5+25]

    elif rcvmsg[4] == 0x15:              # LC status 2
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

    elif rcvmsg[4] == 0x23:              # detector information
        lc_msg[27] = rcvmsg[102]         # vol 1
        lc_msg[28] = rcvmsg[70]          # occ 1
        lc_msg[29] = rcvmsg[103]         # vol 2
        lc_msg[30] = rcvmsg[71]          # occ 2
        lc_msg[31] = rcvmsg[104]         # vol 3
        lc_msg[32] = rcvmsg[72]          # occ 3
        lc_msg[33] = rcvmsg[105]         # vol 4
        lc_msg[34] = rcvmsg[73]          # occ 4

    elif rcvmsg[4] == 0x33:               # split
        lc_msg[35:35+16] = rcvmsg[5:5+16]
        lc_msg[52] = (lc_msg[52] + 1) & 0x7f   # split upload

    elif rcvmsg[4] == 0x43:             # clock upload
        BASE = 4
        lc_msg[1] = rcvmsg[BASE + 1]    # year
        lc_msg[2] = rcvmsg[BASE + 2]    # month
        lc_msg[3] = rcvmsg[BASE + 3]    # day
        lc_msg[4] = rcvmsg[BASE + 4]    # hour
        lc_msg[5] = rcvmsg[BASE + 5]    # min
        lc_msg[6] = rcvmsg[BASE + 6]    # sec
        lc_msg[7] = (lc_msg[7] & 0xf0) + rcvmsg[BASE + 7]  # weekday

    # calculate remain time
    phase = (lc_msg[9] >> 5) + 1
    cycle = lc_msg[20]
    split = 0
    for i in range(phase): split += lc_msg[35 + i]
    if cycle > 0: lc_msg[51] = (cycle + split - lc_msg[18]) % cycle

    return lc_msg

def publish_message(producer, topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode())
#        print("Pulishing - > ", data)
    except Exception as e:
        print('Exception in publishing message ->', e)

def receive_packet(conn, receiveBuffer):
    #
    # rcvmsg = []
    #
    # while True:
    #     receiveBuffer += conn.recv(BUFFER_SIZE)
    #     if len(receiveBuffer) < 6: break
    #
    #     if (receiveBuffer[0] != 0x7e) or (receiveBuffer[1] != 0x7e):
    #         receiveBuffer = receiveBuffer[1:]
    #         break
    #
    #     rxcnt = receiveBuffer[2] + 2
    #     if len(receiveBuffer) < rxcnt:
    #         receiveBuffer += conn.recv(BUFFER_SIZE)
    #         if len(receiveBuffer) < rxcnt: break
    #
    #     if len(receiveBuffer) == rxcnt:
    #         rcvmsg = receiveBuffer
    #         receiveBuffer = []
    #     else:
    #         rcvmsg = receiveBuffer[:rxcnt]
    #         receiveBuffer = receiveBuffer[rxcnt:]
    #
    #     if genlrc(rcvmsg) != 0:
    #         hex_dump("[%s] RXD[Frame_err] :" %time.strftime('%X', time.localtime()), rcvmsg)
    #         rcvmsg = []
    #     break
    #
    # return rcvmsg, receiveBuffer
    repeat = 0
    rcvmsg = []

    while True:
        if len(receiveBuffer) < 6:
            receiveBuffer += conn.recv(256)

        if len(receiveBuffer) < 6:
            time.sleep(0.1)
            repeat += 1
            if repeat < 3: continue

            receiveBuffer = []
            break

        if (receiveBuffer[0] != 0x7e) or (receiveBuffer[1] != 0x7e):
            receiveBuffer = []
            break

        rxcnt = receiveBuffer[2] + 2
        if len(receiveBuffer) < rxcnt:
            time.sleep(0.1)
            repeat += 1
            if repeat < 3: continue

            receiveBuffer = []
            break

        if len(receiveBuffer) == rxcnt:
            rcvmsg = receiveBuffer
            receiveBuffer = []
        elif len(receiveBuffer) > rxcnt:
            rcvmsg = receiveBuffer[:rxcnt]
            receiveBuffer = receiveBuffer[rxcnt:]

        if genlrc(rcvmsg) != 0:
            hex_dump("[%s] RXD[Frame_err] :" %time.strftime('%X', time.localtime()), rcvmsg)
            rcvmsg = []
        break

    return rcvmsg, receiveBuffer

def tcp_serverThread(lcid, conn):
    global lc_msg_array

    lc_msg        = [0] * 64
    lc_msg[0]     = lcid
    receiveBuffer = []
    opcode        = 0x12

    cmdflag[lcid] = 0           # clear command flag

    kafka_producer = KafkaProducer(
                bootstrap_servers = KAFKA_SERVERS,
                api_version       = API_VERSION)

    print("TCP_SERVER_Thread Started & Kafka Connected [lcid = %d]" %lcid)

    rx_memory = sysv_ipc.SharedMemory(0x1000,        flags = sysv_ipc.IPC_CREAT, size = 256)
    s_memory  = sysv_ipc.SharedMemory(0x1000 + lcid, flags = sysv_ipc.IPC_CREAT, size = 128)

    SCAN_TIME = 1

    while threading.main_thread().is_alive():
        time.sleep(SCAN_TIME)

        ####### make send message
        sndmsg  = make_txmsg(lcid, 0x12)    # status dump
        sndmsg += make_txmsg(lcid, 0x42)    # clock upload

        memory = bytearray(s_memory.read())       # shared memory read

        ####### Send to Local
        try:
            conn.send(bytearray(sndmsg))
            if lcid == memory[64]:
                hex_dump("TXD[lcid = %d] :" %lcid, sndmsg)

        except Exception as e:
            print("Send Error [lcid = %d]->" %lcid, e)
            conn.close()
            kafka_producer.close()
            return

        ####### Receive From Local
        while True:
            try:
                time.sleep(0.2)
                rcvmsg, receiveBuffer = receive_packet(conn, receiveBuffer)
                if rcvmsg:
                    lc_msg = rcvmsg_handler(rcvmsg, lc_msg)

                    if rcvmsg[4] > 0xA0:     # DATABASE
                        publish_message(kafka_producer, 'control-response', 'CTL_RPS', rcvmsg[5:-1])
                    else:
                        publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg)

                    if lcid == memory[64]:
                        rx_memory.write(bytearray(rcvmsg))

                    lc_msg[63] = (lc_msg[63] + 1) & 0xff        # increment comm_count
                    lc_msg_array[lcid - 1] = lc_msg

                if len(receiveBuffer) == 0: break

            except Exception as e:
                print("packet error [lcid = %d]->" %lcid, e)

        # write to SharedMemory
        s_memory.write(bytearray(lc_msg))

    print("Main_thread stop -> TCP_Thread stop ~~~[lcid = %d]" %lcid)
    kafka_producer.close()
    conn.close()
    return

def tcp_clientThread(lcid, server_ip):
    global lc_msg_array

    lc_msg        = [0] * 64
    lc_msg[0]     = lcid
    receiveBuffer = []
    opcode        = 0x12

    cmdflag[lcid] = 0           # clear command flag

    kafka_producer = KafkaProducer(
                bootstrap_servers = KAFKA_SERVERS,
                api_version       = API_VERSION)

    print("TCP_SERVER_Thread Started & Kafka Connected [lcid = %d]" %lcid)

    rx_memory = sysv_ipc.SharedMemory(0x1000,        flags = sysv_ipc.IPC_CREAT, size = 256)
    s_memory  = sysv_ipc.SharedMemory(0x1000 + lcid, flags = sysv_ipc.IPC_CREAT, size = 128)

    SCAN_TIME      = 1
    clientConnect  = 0
    server_address = (server_ip, 7070)

    while threading.main_thread().is_alive():
        if clientConnect == 0:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect(server_address)        # 서버와의 연결을 시도
            clientConnect = 1
            print(time.strftime('%X', time.localtime()), "server connected =", server_address)

        time.sleep(SCAN_TIME)

        ####### make send message
        sndmsg  = make_txmsg(lcid, 0x12)    # status dump
        sndmsg += make_txmsg(lcid, 0x42)    # clock upload

        memory = bytearray(s_memory.read())       # shared memory read

        ####### Send to Local
        try:
            client.send(bytearray(sndmsg))
            if lcid == memory[64]:
                hex_dump("TXD[lcid = %d] :" %lcid, sndmsg)
            hex_dump("TXD[lcid = %d] :" %lcid, sndmsg)

        except Exception as e:
            print("Send Error [lcid = %d]->" %lcid, e)
            client.close()
            clientConnect = 0
            continue

        ####### Receive From Local
        while True:
            try:
                time.sleep(0.2)
                rcvmsg, receiveBuffer = receive_packet(client, receiveBuffer)
                if rcvmsg:
                    lc_msg = rcvmsg_handler(rcvmsg, lc_msg)

                    if rcvmsg[4] >= 0xA0:     # startup_code & DATABASE
                        publish_message(kafka_producer, 'control-response', 'CTL_RPS', rcvmsg[5:-1])
                    else:
                        publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg)

                    if lcid == memory[64]:
                        rx_memory.write(bytearray(rcvmsg))

                    lc_msg[63] = (lc_msg[63] + 1) & 0xff        # increment comm_count
                    lc_msg_array[lcid - 1] = lc_msg

                    hex_dump("RXD[lcid = %d] :" %lcid, rcvmsg)

                if len(receiveBuffer) == 0: break

            except Exception as e:
                print("packet error [lcid = %d]->" %lcid, e)

        # write to SharedMemory
        s_memory.write(bytearray(lc_msg))

    print("Main_thread stop -> TCP_Thread stop ~~~[lcid = %d]" %lcid)
    kafka_producer.close()
    client.close()
    return


def tcp_MonitorThread(n):
    global lc_msg_array

    print("Communication Monitor Thread start .....")

    kafka_producer = KafkaProducer(
                bootstrap_servers = KAFKA_SERVERS,
                api_version       = API_VERSION)

    # initial avriable
    comm_count_old = [0] * 50
    err_count      = [0] * 50

    for lcid in range(30):
        comm_count_old[lcid] = lc_msg_array[lcid][63]

    while threading.main_thread().is_alive():
        for lcid in range(30):
            if comm_count_old[lcid] == lc_msg_array[lcid][63]:
                err_count[lcid] += 1
                if err_count[lcid] > 30:
                    if err_count[lcid] == 31:
                        print("comm_fail : lcid = ", lcid + 1)
                        lc_msg_array[lcid][0]  = lcid + 1
                        lc_msg_array[lcid][7] |= 0x40
                        publish_message(kafka_producer, 'local-kafka', 'STS', lc_msg_array[lcid])
                    err_count[lcid] = 99
            else:
                comm_count_old[lcid] = lc_msg_array[lcid][63]
                err_count[lcid]    = 0
        time.sleep(1)

    print("KeyboardInterrupt ~~, Thread stop ~~~")
    kafka_producer.close()
    return
