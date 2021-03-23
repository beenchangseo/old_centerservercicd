from kafka  import KafkaProducer, KafkaConsumer
import json
import time
import sys

KAFKA_SERVERS  = '192.168.1.222:9092'
API_VERSION    = (0, 10, 1)

kafka_producer = KafkaProducer(
            bootstrap_servers = KAFKA_SERVERS,
            api_version       = API_VERSION)

def publish_message(producer, topic_name, key, value):
    try:
        data = { key : value }
        producer.send(topic_name, json.dumps(data).encode())
    except Exception as e:
        print('Exception in publishing message ->', e)


for i in range(100):
    print(i,'publish')
    publish_message(kafka_producer, 'test', 'test_key', [0x7e, 0x7e, 4, 1+i, 0x12, 0x12])
    time.sleep(2)
