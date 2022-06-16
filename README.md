**#CentOS Server 자동 배포 스크립트**
---

# 수동 설치 필요한 사항  
-
## PYTHON MODULE ISNTALL (SU)  
aiohttp==3.7.4.post0\
aiosignal==1.2.0\
async-timeout==4.0.1\
attrs==21.2.0\
bidict==0.21.4\
certifi==2021.10.8\
charset-normalizer==2.0.9\
et-xmlfile==1.1.0\
frozenlist==1.2.0\
idna==3.3\
kafka-python==2.0.2\
multidict==5.2.0\
openpyxl==3.0.9\
PyMySQL==1.0.2\
python-dotenv==0.19.2\
python-engineio==4.3.0\
python-socketio==5.5.0\
requests==2.26.0\
sysv-ipc==1.1.0\
typing_extensions==4.0.1\
urllib3==1.26.7\
yarl==1.7.2\


pip3 install --upgrade pip  
pip3 install kafka-python  
pip3 install python-socketio  
pip3 install pymysql  
pip3 install openpyxl  
pip3 install sysv-ipc  
pip3 install aiohttp  
pip3 install requests
pip3 install python-dotenv

##SELINUX DISABLED (SU)  
selinux state : sestatus  
nano /etc/selinux/config   ##SELINUX=disabled  
reboot  
  
##SSHD CONFIG (SU)  
nano /etc/ssh/sshd_config   
GSSAPIAuthentication no  
UseDNS no  
systemctl restart sshd  
  
##CRONTAB  
mtp4.py <네트워크 및 장치 상태 모니터링>  
mtp4.py 업데이트 필요
  
##CREATE TCS_DATABASE  
create_tcs_database.sql  
  
