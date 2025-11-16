import pika
import json
import time
import uuid

credentials = pika.PlainCredentials('user_cultura', 'pass_cultura')
parameters = pika.ConnectionParameters(host='3.80.53.200', port=5672, virtual_host='/', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

properties = pika.BasicProperties(
    timestamp= int(time.time()),
    message_id=str(uuid.uuid1())
)

channel.basic_publish(
    exchange='citypass_def',
    routing_key='cultura.espacio.crear',
    body=json.dumps("hola"),
    mandatory=True,
    properties=properties
)

print("Mensaje de prueba enviado")
connection.close()