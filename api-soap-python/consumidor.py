import pika
import json
from modelo import prever_diagnostico_e_recomendacao

def callback(ch, method, properties, body):
    sintomas = json.loads(body.decode())
    print("Mensagem recebida:", sintomas)

    diagnostico, recomendacao = prever_diagnostico_e_recomendacao(sintomas)
    resultado = {
        "diagnostico": diagnostico,
        "recomendacao": recomendacao,
        # Mantém o correlation_id para rastreamento, se existir
        "correlation_id": properties.correlation_id if properties.correlation_id else None
    }
    print("Resultado calculado:", resultado)

    # Publica resultado na fila diagnósticos de resposta
    ch.basic_publish(
        exchange='',
        routing_key='diagnosticos_resposta',
        body=json.dumps(resultado),
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensagem persistente
            correlation_id=properties.correlation_id
        )
    )

    # Confirma o consumo da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declara as filas (caso não existam)
    channel.queue_declare(queue='sintomas', durable=True)
    channel.queue_declare(queue='diagnosticos_resposta', durable=True)

    # Limita a 1 mensagem não confirmada por consumidor para balancear carga
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='sintomas', on_message_callback=callback)

    print("Consumidor RabbitMQ aguardando mensagens na fila 'sintomas'...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
