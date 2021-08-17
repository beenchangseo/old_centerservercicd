# mariaDB + galera clustering (10.5 ver)

# ***mysql.sock err ******************
# cd  /var/lib/mysql
# touch mysql.sock
# cd /tmp/
# ln -s /var/lib/mysql/mysql.sock mysql.sock
# ********************************************

# sudo nano /etc/yum.repos.d/MariaDB.repo
# echo 'xhdtlsqhdks1' | sudo -kS echo "[mariadb]"  >  /etc/yum.repos.d/MariaDB.repo
# echo 'xhdtlsqhdks1' | sudo -kS echo "name = MariaDB" >> /etc/yum.repos.d/MariaDB.repo
# echo 'xhdtlsqhdks1' | sudo -kS echo "baseurl = http://yum.mariadb.org/10.5/centos74-amd64"  >> /etc/yum.repos.d/MariaDB.repo
# echo 'xhdtlsqhdks1' | sudo -kS echo "gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB"  >> /etc/yum.repos.d/MariaDB.repo
# echo 'xhdtlsqhdks1' | sudo -kS echo "gpgcheck=1"  >> /etc/yum.repos.d/MariaDB.repo

echo "[mariadb]"  >  /etc/yum.repos.d/MariaDB.repo
echo "name = MariaDB" >> /etc/yum.repos.d/MariaDB.repo
echo "baseurl = http://yum.mariadb.org/10.5/centos74-amd64"  >> /etc/yum.repos.d/MariaDB.repo
echo "gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB"  >> /etc/yum.repos.d/MariaDB.repo
echo "gpgcheck=1"  >> /etc/yum.repos.d/MariaDB.repo

# [mariadb]
# name = MariaDB
# baseurl = http://yum.mariadb.org/10.5/centos74-amd64
# gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
# gpgcheck=1

echo 'xhdtlsqhdks1' | sudo -kS yum -y install MariaDB
# rpm -qa | grep MariaDB
echo 'xhdtlsqhdks1' | sudo -kS systemctl start mariadb
/usr/bin/mysqladmin -u root password 'xhdtlsqhdks1'
echo 'xhdtlsqhdks1' | sudo -kS systemctl enable mariadb


# mysql -uroot -pxhdtlsqhdks1 < create_root_auth.sql

# <mysql create_root_auth.sql>
# mysql -u root -p
# create user 'atcs01'@'%' identified by 'xhdtlsqhdks1';
# grant all privileges on tcs_database.* to 'atcs01'@'%';
# grant all privileges on *.* to 'root'@'%' identified by 'xhdtlsqhdks1';
# FLUSH privileges;

# galera setting 
echo 'xhdtlsqhdks1' | sudo -kS systemctl stop mariadb

# sudo nano /etc/my.cnf.d/server.cnf
\cp /home/atcs01/centerservercicd/server1/server.cnf /etc/my.cnf.d/server.cnf

# [server]

# [mysqld]

# [galera]
# wsrep_on=ON
# wsrep_provider=/usr/lib64/galera-4/libgalera_smm.so
# wsrep_cluster_address=gcomm://172.16.0.201,172.16.0.202,172.16.0.203
# binlog_format=row
# default_storage_engine=InnoDB
# innodb_autoinc_lock_mode=2

# [embedded]

# [mariadb]

# [mariadb-10.5]

echo 'xhdtlsqhdks1' | sudo -kS sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
echo 'xhdtlsqhdks1' | sudo -kS sudo firewall-cmd --permanent --zone=public --add-port={4567,4568,4444}/tcp
echo 'xhdtlsqhdks1' | sudo -kS sudo firewall-cmd --reload

# galera_new_cluster
