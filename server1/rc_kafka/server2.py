import time
import socket
import serial
import os
import threading
import sys

#IP_ADDRESS = '192.168.1.202'
IP_ADDRESS = os.popen('ip addr show eth0.2 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
PORT_NUM   = 7070
server_address = (IP_ADDRESS, PORT_NUM)
BUFFER_SIZE = 1024      # byte 1024 byte

connection  = False
thread_True = True
debug       = 1

def prn_dat(msg, buf):
    global debug
    if debug == 0: return
#    msg += time.strftime('[%X]', time.localtime())
    for i in range(len(buf)): msg += (" %X%X" %(buf[i] >> 4, buf[i] & 0xf))
    print(msg)

def gen_lrc(buf):
    lrc = 0
    for value in buf: lrc ^= value
    return (lrc)

def receive_TCP_cmdmsg(conn):
    rcvmsg = conn.recv(3)

    if len(rcvmsg) < 3:   return None
    if rcvmsg[0] != 0x7e: return None
    if rcvmsg[1] != 0x7e: return None

    rcvmsg += conn.recv(rcvmsg[2] + 2 - 3)

    if len(rcvmsg) < (rcvmsg[2] + 2): return None
    if gen_lrc(rcvmsg) != 0: return None

    return (rcvmsg)

def receive_UART_msg(ser):

    time.sleep(0.1)
    if ser.inWaiting() < 3: return None

    rcvmsg = ser.read(3)
    if rcvmsg[0] != 0x7e: return None
    if rcvmsg[1] != 0x7e: return None

    remain_count  = (rcvmsg[2] + 2) - 3
    time.sleep(0.05 + 0.005 * remain_count)
    if ser.inWaiting() < remain_count: return None

    rcvmsg += ser.read(remain_count)

    # if gen_lrc(rcvmsg) != 0:
    #     prn_dat("lrc_err :", rcvmsg)
    #     return None

    return rcvmsg

def serial_read_thread():
    global thread_True, connection, ser, conn

    comm_errcnt = 0

    while thread_True == True:
        try:
            sndmsg = receive_UART_msg(ser)
            if sndmsg:
                conn.send(sndmsg)
                prn_dat("TXD :", sndmsg)
                time.sleep(0.2)
                comm_errcnt = 0
            else:
                comm_errcnt += 1
                if comm_errcnt > 6000:  # 600 sec
                    print("system reboot ~~~")
                    os.system("reboot")

        except Exception as e:
            print("Send Excepttion Interrupt ~~~", e)
            time.sleep(1)

# ----- main routine ------

#if len(sys.argv) < 2: comm_speed = 38400
#else:                 comm_speed = 2400
comm_speed = 2400

print("TCP/IP server start", server_address)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(server_address)
server.settimeout(30)
server.listen(10)

ser = serial.Serial('/dev/ttyS1', baudrate=comm_speed, timeout = 1)
if ser.isOpen() == False:   # serial open
    ser.open()              #
print ("comm port = ", ser.name, "comm_speed = ", comm_speed)        # print Serial port

thread = threading.Thread(target = serial_read_thread)
thread.start()

comm_errcnt = 0

while True:
    try:
#        server.settimeout(10)

        if connection == False:
            print("wait connection ....")
            conn, addr = server.accept()    # connection request
            print("Connection = ", conn.getpeername())
            connection = True
            comm_errcnt = 0

        rcvmsg = conn.recv(1024)
        if rcvmsg:
            prn_dat("RXD :", rcvmsg)
            ser.write(rcvmsg)               # serial write
        else:
            print("receive timeout ~~~ restart connection")
            time.sleep(1)
            conn.close()
            connection = False
            continue

    except Exception as e:
        print("Excepttion Interrupt ~~~", e)
        if connection == True: conn.close()
        time.sleep(1)
        connection = False
        continue

    except KeyboardInterrupt:
        print("KeyboardInterrupt ~~")
        thread_True = False
        if connection == True: conn.close()
        server.close()
        ser.close()
        break