from socket import *
import pymysql
#from multiprocessing import Process, Value, Array, Queue

import time
import lc_protocol

# tcp/ip port define
IP_ADDRESS    = '192.168.1.47'
IP_ADDRESS2   = '192.168.1.29'
PORT_NUM      = 7070

def get_ip_address_port_num(lcid):
    # MySQl connection
    mydb = pymysql.connect(
            host     = "192.168.1.21",
            user     = "root",
            password = "root",
            db       = "tcs_database",
            charset  = "utf8"
            )
    cur  = mydb.cursor()
    cur.execute("SELECT ip, port_num FROM local WHERE id = %d" %lcid)
    data = cur.fetchone()
    mydb.close()
    return data

def socket_connect(client, s_addr):
    try:
        client.connect(s_addr)
        print(time.strftime('%X', time.localtime()), "server connected =", s_addr)
        return 0
    except:
        print("[client] connect error", s_addr)
        client.close()
        return 1

def socket_read(client):       # socet (TCP)
    try:
        return client.recv(1024)
    except:
        print("[client %s]" %time.strftime('%X', time.localtime()), "socket read error")
        client.close()
        return ""

def socket_write(client, buf):       # socet (TCP)
    try:
        client.send( bytearray(buf) )
        return 0
    except:
        print("[client %s]" %time.strftime('%X', time.localtime()), "socket send error")
        client.close()
        return 1

def TCP_LocalProcess(lcid, n1, n2, q):

    lc_msg  = [0] * 32
    command_list = [0x12, 0x32, 0x12, 0x42]
    list         = 0
    opcode       = 0
    control      = []
    socket_error = 1
    producer_msg = 0

    print("[LC-sane2010] TCP/IP Local process started [lcid = %d]" %lcid)

    lc_msg[0]    = lcid

    server_address = get_ip_address_port_num(lcid)
    print ("server_address =", server_address)

    while True:

        if n1.value != 0:
            opcode  = n1.value
            n1.value = 0
            control = n2[:]
            print("SERVER command :", control)
        else:
            opcode = command_list[list]
            list = (list + 1) % 4

        if socket_error == 1:
            client = socket(AF_INET, SOCK_STREAM)
            socket_error = socket_connect(client, server_address)

        control = lc_protocol.make_control_message(opcode, control)
        sndmsg  = lc_protocol.make_txmsg(opcode, control)

        if socket_error == 1:
            continue

        socket_error = socket_write(client, sndmsg)
        if socket_error == 1:
            continue

        rcvmsg = socket_read(client)
        if not rcvmsg:
            print("[TCP/IP-LC] no data")
            socket_error = 1
            continue

        lc_protocol.check_rxmsg(rcvmsg, len(rcvmsg))

        if rcvmsg[4] == 0x13:                    # lc status
#            if rcvmsg[6] != lc_msg[9]: producer_msg = 1
            lc_msg[ 8:8+6]  = rcvmsg[5:5+6]      # lc status
            lc_msg[17:17+6] = rcvmsg[15:15+6]    # cycle, sc, offset, phase hold/omit
            lc_msg[31]      = 0x00               # detector

        if rcvmsg[4] == 0x33:                    # split
            lc_msg[23:23+8] = rcvmsg[5:5+8]

        if rcvmsg[4] == 0x43:                    # rtc
            if rcvmsg[10] != lc_msg[6]: producer_msg = 1
            lc_msg[1:8] = rcvmsg[5:5+7]

        # publicsh to Kafka
        if producer_msg == 1:
            producer_msg = 0
            q.put(lc_msg)

        time.sleep(0.2)
