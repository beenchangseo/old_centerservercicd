

##PYTHON MODULE ISNTALL (SU)
pip3 install --upgrade pip
pip3 install kafka-python
pip3 install python-socketio
pip3 install pymysql
pip3 install openpyxl
pip3 install sysv-ipc
pip3 install aiohttp

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

##CREATE TCS_DATABASE
create_tcs_database.sql