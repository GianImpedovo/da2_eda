import pika
import json
import time
import uuid

credentials = pika.PlainCredentials('user_movilidad', 'pass_movilidad')
parameters = pika.ConnectionParameters(host='eda-nlb-6fd7b3b5a64e8d75.elb.us-east-1.amazonaws.com', port=5672, virtual_host='/', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

properties = pika.BasicProperties(
    timestamp= int(time.time()),
    message_id=str(uuid.uuid1())
)

channel.basic_publish(
    exchange='citypass_def',
    routing_key='movilidad.viaje.estado',
    body=json.dumps("hola"),
    mandatory=True,
    properties=properties
)

print("Mensaje de prueba enviado")
connection.close()