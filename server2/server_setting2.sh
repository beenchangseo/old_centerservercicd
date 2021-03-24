## server setting script start point ##

# python3.8 version install #
cd ~
echo 'xhdtlsqhdks1' | sudo -kS yum -y groupinstall 'Development Tools'
echo 'xhdtlsqhdks1' | sudo -kS yum -y install zlib zlib-devel libffi-devel
echo 'xhdtlsqhdks1' | sudo -kS yum -y install openssl openssl-devel
curl -O https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz
tar zxvf Python-3.8.1.tgz
cd Python-3.8.1
echo 'xhdtlsqhdks1' | sudo -kS ./configure
echo 'xhdtlsqhdks1' | sudo -kS make
echo 'xhdtlsqhdks1' | sudo -kS make install


# nodejs 12.x version install #
cd ~
echo 'xhdtlsqhdks1' | curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -
echo 'xhdtlsqhdks1' | sudo -kS yum -y install nodejs

# git clone server setting forder (1,2,3)]
cd ~
cd /home/atcs02/centerservercicd/server1
npm install dotenv
node app_make.cfg.js
#########################################


# zookeeper server install & setting #
cd ~
echo 'xhdtlsqhdks1' | sudo -kS yum -y install java-1.8.0-openjdk
mkdir /home/atcs02/app
cd /home/atcs02/app
wget https://archive.apache.org/dist/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz
tar zxf zookeeper-3.4.14.tar.gz
ln -s zookeeper-3.4.14 zookeeper
echo 'xhdtlsqhdks1' | sudo -kS mkdir -p /data/zookeeper
echo 'xhdtlsqhdks1' | sudo -kS chown -R atcs02:atcs02 /data
echo 1 > /data/zookeeper/myid 
# [zoo.cfg] file setting
\cp /home/atcs02/centerservercicd/server1/zoo.cfg /home/atcs02/app/zookeeper/conf/zoo.cfg

# zookeeper server firewall setting
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --permanent --zone=public --add-port=2181/tcp 
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --permanent --zone=public --add-port=2888/tcp 
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --permanent --zone=public --add-port=3888/tcp
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --reload


# [zookeeper-server.service] file setting
echo 'xhdtlsqhdks1' | sudo -kS cp /home/atcs02/centerservercicd/server1/zookeeper-server.service /usr/lib/systemd/system/zookeeper-server.service



echo 'xhdtlsqhdks1' | sudo -kS systemctl daemon-reload
echo 'xhdtlsqhdks1' | sudo -kS systemctl enable zookeeper-server.service

# kafka server install & setting #
cd /home/atcs02/app
wget https://archive.apache.org/dist/kafka/1.0.0/kafka_2.11-1.0.0.tgz
tar zxf kafka_2.11-1.0.0.tgz
ln -s kafka_2.11-1.0.0 kafka
echo 'xhdtlsqhdks1' | sudo -kS mkdir -p /data/kafka
echo 'xhdtlsqhdks1' | sudo -kS mkdir -p /data/kafka/data1
echo 'xhdtlsqhdks1' | sudo -kS chown -R atcs02:atcs02 /data
echo 1 > /data/kafka/myid


# [server.properties] file setting
\cp /home/atcs02/centerservercicd/server1/server.properties /home/atcs02/app/kafka/config/server.properties
# [zookeeper.properties] file setting
\cp /home/atcs02/centerservercicd/server1/zookeeper.properties /home/atcs02/app/kafka/config/zookeeper.properties
# kafka server firewall setting 
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --permanent --zone=public --add-port=9092/tcp
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --reload


# [kafka-server.service] file setting 
echo 'xhdtlsqhdks1' | sudo -kS cp /home/atcs02/centerservercicd/server1/kafka-server.service /usr/lib/systemd/system/kafka-server.service
echo 'xhdtlsqhdks1' | sudo -kS systemctl daemon-reload
echo 'xhdtlsqhdks1' | sudo -kS systemctl enable kafka-server.service
echo 'xhdtlsqhdks1' | sudo -kS systemctl stop kafka-server.service
echo 'xhdtlsqhdks1' | sudo -kS systemctl stop zookeeper-server.service



echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --zone=public --permanent --add-port=7070/tcp
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --zone=public --permanent --add-port=3000/tcp
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --zone=public --permanent --add-port=9000/tcp
echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --zone=public --permanent --add-port=5901/tcp

echo 'xhdtlsqhdks1' | sudo -kS firewall-cmd --reload


