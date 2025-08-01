import pika
import json
import uuid

def enviar_sintomas_para_fila(sintomas):
    
    correlation_id = str(uuid.uuid4())

   
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    
    channel.queue_declare(queue='sintomas', durable=True)

  
    mensagem = json.dumps(sintomas)

    
    channel.basic_publish(
        exchange='',
        routing_key='sintomas',
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2, 
            correlation_id=correlation_id,
            reply_to='diagnosticos_resposta'  
        )
    )

    connection.close()

    return correlation_id
