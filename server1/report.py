#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility
# -*- coding: utf-8 -*-
import pymysql
from threading import Thread
import subprocess
try:
    import queue
except ImportError:
    import Queue as queue
import re
import requests
import json
import datetime, time

import smtplib, os
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from kafka import KafkaConsumer


# MySQl connection
DATABASE_SERVERS = '172.16.0.102'
REPORT_ARRAY_DATA = []
mydb = pymysql.connect(
        host              = DATABASE_SERVERS,
        port              = 3306,
        user              = "atcs02",
        password          = "xhdtlsqhdks1",
        db                = "tcs_database",
        charset           = "utf8"
        )
cursor  = mydb.cursor()

now = datetime.datetime.now()
nowDatetime = now.strftime("'%Y-%m-%d %H:%M:%S'")

def kafka_consumer(ip):
    buf = []
    consumer = KafkaConsumer(
                bootstrap_servers = ip,
                auto_offset_reset = 'latest',
                enable_auto_commit = True,
                consumer_timeout_ms=5000,
                api_version=(0, 10, 1))
    consumer.subscribe(['log'])
    for msg in consumer :
        jsonData = json.loads(msg.value)
        buf = jsonData['log']
        break
    consumer.close(autocommit=False)
    return buf

# def detect_condition_consumer(ip):
#     buf = [-1, -1, -1, -1]
#     ips = ip.split("'")[1]+':9092'
#     # Kafka consumer
#     consumer = KafkaConsumer(
#                 bootstrap_servers = ips,
#                 auto_offset_reset = 'latest',
#                 enable_auto_commit = False,
#                 consumer_timeout_ms=6000,
#                 api_version=(0, 10, 1))
#     consumer.subscribe(['log'])
#     for msg in consumer :
#         # print(msg)
#         jsonData = json.loads(msg.value)
#         buf = jsonData['log']
#         # print(buf)
#         break
#     consumer.close(autocommit=False)
#     return buf

def send_Mail(report_Mail_Data):
  sndmsg = ''
  for i in range(len(report_Mail_Data)):
    sndmsg += report_Mail_Data[i]
  

  id = 'dbict0701' 
  password = 'dongbu9197**' 
  sendEmail = 'dbict0701@naver.com'
  # destination = ['seochangbin_1@naver.com','iamthemarine@naver.com','gammr@naver.com']
  destination = ['seochangbin_1@naver.com','okfine1000@naver.com','gammr@naver.com']
  subject = '????????? ????????? ???????????? ?????? ?????????' 
  text = sndmsg 
  addrs = destination  # send mail list 

  # login 
  smtp = smtplib.SMTP('smtp.naver.com', 587) 
  smtp.ehlo() 
  smtp.starttls() 
  smtp.login(id, password) 

  # message 
  message = MIMEMultipart() 
  message.attach(MIMEText(text)) 

  # Send 

  message["From"] = sendEmail 
  message['To'] = ", ".join(destination)
  message['Subject'] = subject 
  smtp.sendmail(sendEmail, destination , message.as_string()) 

  smtp.quit()

def network_report_watchdog(cursor):
  report_Mail_Data = []

  report_CheckTime_start = "09:00:00"
  report_CheckTime_start = datetime.datetime.strptime(report_CheckTime_start, "%H:%M:%S")
  report_CheckTime_start = now.replace(hour=report_CheckTime_start.time().hour, minute=report_CheckTime_start.time().minute, second=report_CheckTime_start.time().second, microsecond=0)

  report_CheckTime_end = "09:01:00"
  report_CheckTime_end = datetime.datetime.strptime(report_CheckTime_end, "%H:%M:%S")
  report_CheckTime_end = now.replace(hour=report_CheckTime_end.time().hour, minute=report_CheckTime_end.time().minute, second=report_CheckTime_end.time().second, microsecond=0)


  if (now > report_CheckTime_start and now < report_CheckTime_end):
    ##????????? ?????? ??? ????????? ?????? ????????????
    print("????????? ?????? ?????? !!")
    ## ?????? ????????? ?????? ??????
    querry = "SELECT COUNT(*) FROM network_report_console"
    cursor.execute(querry)
    result = cursor.fetchall()
    rows_count = result[0][0]
    ## ?????? ????????? ??????
    querry = "SELECT id,device_num,ip FROM network_report_console"
    cursor.execute(querry)
    result = cursor.fetchall()
    for rows in range(rows_count):
      querry = """SELECT A.log_time, A.online, A.id,  B.name, A.device, A.ip FROM network_report_console A JOIN local B 
              where A.id=%s AND A.device_num=%s AND A.ip='%s' AND A.id = B.id""" %(result[rows][0],result[rows][1],result[rows][2])
      cursor.execute(querry)
      log_time_AND_online = cursor.fetchall() ## ???????????? ??? ????????? (?????? , ????????? ??????)
      if log_time_AND_online[0][1] == 0: ## ????????? ??????
        diff =  now-datetime.datetime.strptime(str(log_time_AND_online[0][0]), "%Y-%m-%d %H:%M:%S")
        # if (diff.seconds / 3600) > 1:
        if True:
          diff = str(diff).split('.')[0]
          diff = str(diff).split(':')
          diff = diff[0] + '??? ' + diff[1] + '??? ' + diff[2] + '??? ??????'
          # print(log_time_AND_online[0][2],'??? ????????? ', log_time_AND_online[0][3],'1?????? ?????? ?????? ??????')
          print("?????? ?????? ?????? : ",str(diff).split('.')[0])
          report_Mail_Data.append(str(log_time_AND_online[0][2])+'??? '+ str(log_time_AND_online[0][3])+' ?????????  <'+str(log_time_AND_online[0][4])+'> : 1?????? ?????? ?????? ??????\n'+"?????? ?????? ?????? : "+ diff +'\n\n\n')
    # print(report_Mail_Data)
    send_Mail(report_Mail_Data)


def put_network_report_console(cursor, log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode):
  ##?????? ????????? ????????? ?????? ?????? 
  querry = """select EXISTS (select * from network_report_console where id=%s and device_num=%s) as success;"""%(id, device_num)
  # print(querry)
  cursor.execute(querry)
  result = cursor.fetchall()
  if result[0][0] == 0: ##????????? ??????
    ##?????? ????????? ???????????? ?????? ????????? ??????
    querry = """INSERT INTO network_report_console(log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" %(log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode)
    cursor.execute(querry)
  elif result[0][0] == 1: ##?????? ????????? ??????
    # print('?????? ????????? ??????')
    ##????????? ?????? ?????? ?????? ??? ?????????????????? ??????
    if online == 1: ##"ON"
      ##????????? ????????? log_time ??? ?????? & online ??? 'ON'?????? ??????
      # print('????????? ????????? log_time ??? ?????? & online ??? ON?????? ??????')
      querry = """UPDATE network_report_console SET online=%s, log_time=%s, ps_run=%s , can_sts=%s , lmb_sts=%s , det_mode=%s  
                  where id=%s and ip=%s and device_num=%s""" %(online, log_time, ps_run, can_sts, lmb_sts, det_mode, id, ip, device_num)
      cursor.execute(querry)
    elif online == 0: ##"OFF"
      ##???????????? ????????? log_time ??? ?????? X & online ??? 'OFF'?????? ??????
      # print('???????????? ????????? log_time ??? ?????? X & online ??? OFF?????? ??????')
      querry = """UPDATE network_report_console SET online=%s, ps_run=%d , can_sts=%d , lmb_sts=%d , det_mode=%d
                  where id=%s and ip=%s and device_num=%s""" %(online, -1, -1, -1, -1, id, ip, device_num)
      cursor.execute(querry)

def put_network_report(cursor, log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode):
    try:
        querry = """INSERT INTO network_report(log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" %(log_time, id, ip, device, device_num, online, ps_run, can_sts, lmb_sts, det_mode)
        # print(querry)
        cursor.execute(querry)
    except Exception as e:
        # print('Exception in putting event_log')
        print(e)
def set_ips(cursor):
  ips = []
  try:
    querry = """SELECT ip,detector_count FROM local"""
    cursor.execute(querry)
    result = cursor.fetchall()
    print(result)
    for i in range(len(result)):
      network_band = result[i][0].split('.')
      del network_band[3]
      network_band = '.'.join(network_band)+'.'
      ips.append(network_band+'1')
      ips.append(network_band+'2')
      for j in range(result[i][1]):
        ips.append(network_band+str(j*2+3))
        ips.append(network_band+str(j*2+4))
    # print(ips)
    return ips
  except Exception as e:
    print(e)
# some global vars
num_threads = 40
ips_q = queue.Queue()
out_q = queue.Queue()

kakao_msg = ""
# build IP array
ips = []
for i in range(1,200):
  ips.append("192.168.1."+str(i))

ips = set_ips(cursor)
# ips = ["20.2.10.1", "20.2.10.2", "20.2.10.3", "20.2.10.4",
#        "20.2.11.1", "20.2.11.2", "20.2.11.3", "20.2.11.4","20.2.11.5", "20.2.11.6",
#        "20.2.12.1", "20.2.12.2", "20.2.12.3", "20.2.12.4","20.2.12.5", "20.2.12.6", "20.2.12.7", "20.2.12.8",
#        "20.2.13.1", "20.2.13.2", "20.2.13.3", "20.2.13.4","20.2.13.5", "20.2.13.6", "20.2.13.7", "20.2.13.8",
#        "20.2.14.1", "20.2.14.2", "20.2.14.3", "20.2.14.4","20.2.14.5", "20.2.14.6",
#        "20.2.15.1", "20.2.15.2", "20.2.15.3", "20.2.15.4","20.2.15.5", "20.2.15.6",
#        "20.2.16.1", "20.2.16.2", "20.2.16.3", "20.2.16.4","20.2.16.5", "20.2.16.6",
#        "20.2.17.1", "20.2.17.2", "20.2.17.3", "20.2.17.4","20.2.17.5", "20.2.17.6",
#        "20.2.18.1", "20.2.18.2", "20.2.18.3", "20.2.18.4","20.2.18.5", "20.2.18.6",
#        "20.2.19.1", "20.2.19.2", "20.2.19.3", "20.2.19.4","20.2.19.5", "20.2.19.6",
#        "20.2.20.1", "20.2.20.2", "20.2.20.3", "20.2.20.4","20.2.20.5", "20.2.20.6", "20.2.20.7", "20.2.20.8",
# ]

def product_list(intersection, product, ipnum, signal, nowDatetime ):
    

    product_num = 0

    product_list = ["?????????",
                    "?????????",
                    "1??? ??????",
                    "1??? ?????????",
                    "2??? ??????",
                    "2??? ?????????",
                    "3??? ??????",
                    "3??? ?????????",
                    "4??? ??????",
                    "4??? ?????????"
                    ]

    if product == 1 :
      product_num = 12
    elif product == 2:
      product_num = 2
    else :
      product_num = product + 1

    
    if signal :
        # return [str(intersection-9),"'"+str(ipnum)+"'","'"+product_list[product-1]+"'",product-1,"'ON'",nowDatetime]
        ## ???????????? , ????????? ??????, ?????????, ????????????, ?????? ??????, ?????????
        return [nowDatetime, str(intersection-9), "'"+str(ipnum)+"'", "'"+product_list[product-1]+"'", product_num, 1]
        # return str(intersection-9) + " " + str(ipnum) + " " + product_list[product-1] + " ON " + nowDatetime
    else :
        # return [str(intersection-9),"'"+str(ipnum)+"'","'"+product_list[product-1]+"'",product-1,"'OFF'",nowDatetime]
        return [nowDatetime, str(intersection-9), "'"+str(ipnum)+"'", "'"+product_list[product-1]+"'", product_num, 0]
        # return str(intersection-9) + " " + str(ipnum) + " " + product_list[product-1] + " OFF " + nowDatetime
    
# thread code : wraps system ping command
def thread_pinger(i, q):
    
  global kakao_msg

  """Pings hosts in queue"""
  while True:
    # get an IP item form queue
    ip = q.get()
    # ping it
    args=['/bin/ping', '-c', '1', '-W', '1', str(ip)]
    p_ping = subprocess.Popen(args,
                              shell=False,
                              stdout=subprocess.PIPE)
    # save ping stdout
    p_ping_out = str(p_ping.communicate()[0])

    ##?????? ????????? ???
    if (p_ping.wait() != 0):
      m = re.match('(\w{1,3})\.(\w{1,3})\.(\w{1,3})\.(\w{1,3})', str(ip))
      data = product_list(int(m.group(3)), int(m.group(4)), str(ip),False, nowDatetime)
      device_ip = (data[2].split('.')[-1])[0:-1] ## DeviceIP
      
      data.extend([-1,-1,-1,-1])   ## PING ????????? ????????? KAFKA DATA -1??? ??????
      # print(data)

      REPORT_ARRAY_DATA.append(data)
    ##?????? ????????? ???
    else :
      m = re.match('(\w{1,3})\.(\w{1,3})\.(\w{1,3})\.(\w{1,3})', str(ip))
      data = product_list(int(m.group(3)), int(m.group(4)), str(ip),True, nowDatetime)
      device_ip = (data[2].split('.')[-1])[0:-1] ## DeviceIP
      if (device_ip == '3' or device_ip == '5' or device_ip == '7' or device_ip == '9') and len(kafka_consumer(ip)) == 4:
        data.extend(kafka_consumer(ip))
      else:
        data.extend([-1,-1,-1,-1])
      
      # print(data)
      
      REPORT_ARRAY_DATA.append(data)
    q.task_done()

# start the thread pool
for i in range(num_threads):
  worker = Thread(target=thread_pinger, args=(i, ips_q))
  worker.setDaemon(True)
  worker.start()

# fill queue
for ip in ips:
  ips_q.put(ip)

# wait until worker threads are done to exit    
ips_q.join()

# sendKakaoAPI(kakao_msg)

# print result
while True:
  try:
    msg = out_q.get_nowait()
  except queue.Empty:
    break
  print(msg)

# print(REPORT_ARRAY_DATA)
for count in range(len(REPORT_ARRAY_DATA)):
  print(REPORT_ARRAY_DATA[count])
  log_time    = REPORT_ARRAY_DATA[count][0]
  id          = REPORT_ARRAY_DATA[count][1]
  ip          = REPORT_ARRAY_DATA[count][2]
  device      = REPORT_ARRAY_DATA[count][3]
  device_num  = REPORT_ARRAY_DATA[count][4]
  online      = REPORT_ARRAY_DATA[count][5]
  PS_RUN      = REPORT_ARRAY_DATA[count][6]
  CAN_STS     = REPORT_ARRAY_DATA[count][7]
  LMB_STS     = REPORT_ARRAY_DATA[count][8]
  DET_MODE    = REPORT_ARRAY_DATA[count][9]

  put_network_report(cursor, log_time, id, ip, device, device_num, online, PS_RUN, CAN_STS, LMB_STS, DET_MODE)
  put_network_report_console(cursor, log_time, id, ip, device, device_num, online, PS_RUN, CAN_STS, LMB_STS, DET_MODE)
  
network_report_watchdog(cursor)

mydb.commit()
mydb.close()

