# consumidor_rest.py
import pika
from flask import Flask, jsonify
import threading
import json

app = Flask(__name__)

respostas = {}

def callback(ch, method, properties, body):
    print("Mensagem recebida na fila resposta")
    correlation_id = properties.correlation_id or 'default'
    respostas[correlation_id] = json.loads(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumidor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='diagnosticos_resposta', durable=True)
    channel.basic_consume(queue='diagnosticos_resposta', on_message_callback=callback)
    print("Consumidor REST aguardando mensagens na fila 'diagnosticos_resposta'...")
    channel.start_consuming()

@app.route('/resultado/<correlation_id>', methods=['GET'])
def get_resultado(correlation_id):
    resultado = respostas.get(correlation_id)
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({"erro": "Resultado não encontrado"}), 404

if __name__ == '__main__':
    threading.Thread(target=start_consumidor, daemon=True).start()
    app.run(port=5000)
