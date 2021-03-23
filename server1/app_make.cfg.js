var fs = require('fs');
require('dotenv').config();

const server1_ip = process.env.SERVER1_IP
const server2_ip = process.env.SERVER2_IP
const server3_ip = process.env.SERVER3_IP
const server1_user = process.env.SERVER1_USER
const server2_user = process.env.SERVER2_USER
const server3_user = process.env.SERVER3_USER

var url= './';
var zoo_fileName='zoo.cfg';
var zoo_encoding = 'utf8';
var zoo_data = `tickTime=2000
initLimit=10
syncLimit=5
dataDir=/data/zookeeper
clientPort=2181
server.1=${server1_ip}:2888:3888
server.2=${server2_ip}:2888:3888
server.3=${server3_ip}:2888:3888`
 
fs.writeFile(url+zoo_fileName,zoo_data,zoo_encoding,function(err){
    if(err) console.log('Error'+err);
      else console.log("쓰기완료");
});
/////////////////////////////////////////////////////////////////////////////////
var zookeeper_server_service_fileName='zookeeper-server.service';
var zookeeper_server_service_encoding = 'utf8';
var zookeeper_server_service_data = `[Unit]
Description=zookeeper-server 
After=network.target 
[Service] 
Type=forking 
User=${server1_user}
Group=${server1_user}
SyslogIdentifier=zookeeper-server 
WorkingDirectory=/home/${server1_user}/app/zookeeper
Restart=always 
RestartSec=0s
ExecStart=/home/${server1_user}/app/zookeeper/bin/zkServer.sh start
ExecStop=/home/${server1_user}/app/zookeeper/bin/zkServer.sh stop 
[Install] 
WantedBy=multi-user.target
`;
fs.writeFile(url+zookeeper_server_service_fileName,zookeeper_server_service_data,zookeeper_server_service_encoding,function(err){
    if(err) console.log('Error'+err);
      else console.log("쓰기완료");
});
//////////////////////////////////////////////////////////////////////////////////
var server_properties_fileName='server.properties';
var server_properties_encoding = 'utf8';
var server_properties_data = `broker.id=1
advertised.listeners=PLAINTEXT://${server1_ip}:9092
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
log.dirs=/data/kafka/data1
num.partitions=1
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
log.retention.hours=72
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=${server1_ip}:2181,${server2_ip}:2181,${server3_ip}:2181
zookeeper.connection.timeout.ms=6000
group.initial.rebalance.delay.ms=0
delete.topic.enable=true
auto.create.topics.enable=true
auto.leader.rebalance.enable=true
`;
fs.writeFile(url+server_properties_fileName,server_properties_data,server_properties_encoding,function(err){
    if(err) console.log('Error'+err);
      else console.log("쓰기완료");
});
////////////////////////////////////////////////////////////////////////////////
var zookeeper_properties_fileName='zookeeper.properties';
var zookeeper_properties_encoding = 'utf8';
var zookeeper_properties_data = `dataDir=/data/zookeeper
clientPort=2181
maxClientCnxns=60
admin.enableServer=false
tickTime=2000
initLimit=10
syncLimit=5
server.1=${server1_ip}:2888:3888
server.2=${server2_ip}:2888:3888
server.3=${server3_ip}:2888:3888
`;
fs.writeFile(url+zookeeper_properties_fileName,zookeeper_properties_data,zookeeper_properties_encoding,function(err){
    if(err) console.log('Error'+err);
      else console.log("쓰기완료");
});
//////////////////////////////////////////////////////////////////////////////////
var kafka_server_service_fileName='zookeeper-server.service';
var kafka_server_service_encoding = 'utf8';
var kafka_server_service_data = `[Unit]
Description=kafka-server
After=network.target
[Service]
Type=simple
User=${server1_user}
Group=${server1_user}
SyslogIdentifier=kafka-server
WorkingDirectory=/home/${server1_user}/app/kafka
Restart=no
RestartSec=0s
ExecStart=/home/${server1_user}/app/kafka/bin/kafka-server-start.sh /home/${server1_user}/app/kafka/config/server.properties
ExecStop=/home/${server1_user}/app/kafka/bin/kafka-server-stop.sh
[Install]
WantedBy=multi-user.target
`;
fs.writeFile(url+kafka_server_service_fileName,kafka_server_service_data,kafka_server_service_encoding,function(err){
    if(err) console.log('Error'+err);
      else console.log("쓰기완료");
});