from kafka import KafkaConsumer
import json
import sys

consumer = KafkaConsumer(
            bootstrap_servers = '192.168.1.221:9092',
            auto_offset_reset = 'latest',
            group_id = 'consumer1',
            api_version=(0, 10, 1))
consumer.subscribe(['local-kafka'])

for msg in consumer :
    jsonData = json.loads(msg.value)
    try:
        buf = jsonData['STS']
        print(buf)
    except Exception as e:
        pass
