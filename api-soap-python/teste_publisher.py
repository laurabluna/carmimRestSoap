import pika
import json

mensagem = {
    "sintomas": ["dores menstruais", "fadiga", "náusea"]
}

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sintomas', durable=True)

channel.basic_publish(
    exchange='',
    routing_key='sintomas',
    body=json.dumps(mensagem),
    properties=pika.BasicProperties(delivery_mode=2)
)

print("✅ Mensagem enviada com sucesso!")
connection.close()
