import json 
import requests
from kafka import KafkaProducer 
from time import sleep 

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

for i in range(150):
    # Fetch Bitcoin price data from CoinDesk API
    res = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = json.loads(res.content.decode('utf-8'))
    
    
    print(data)
    # Publish Bitcoin price data to Kafka topic
    producer.send('bitcoin-price-euro', value=data)

    # Wait for 5 seconds before publishing the next message
    sleep(5)

    # Flush Kafka producer to ensure all messages are sent before exiting
    producer.flush()

