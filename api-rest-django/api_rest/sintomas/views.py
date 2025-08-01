import json
import pika
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
import requests
from .serializers import SintomaSerializer
from .models import Sintoma
from services.rabbitmq import enviar_sintomas_para_fila


class EnviarSintomasView(APIView):
    def post(self, request):
        sintomas = request.data  
        if not sintomas:
            return Response({'erro': 'Nenhum sintoma fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        correlation_id = enviar_sintomas_para_fila(sintomas)
        return Response({'correlation_id': correlation_id}, status=status.HTTP_202_ACCEPTED)

class SintomasAPIView(APIView):
    def post(self, request):
        sintomas = request.data
        correlation_id = enviar_sintomas_para_fila(sintomas)

        return Response({"correlation_id": correlation_id}, status=status.HTTP_202_ACCEPTED)

def publicar_sintomas(sintomas):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sintomas', durable=True)
        mensagem = json.dumps(sintomas)
        channel.basic_publish(
            exchange='',
            routing_key='sintomas',
            body=mensagem,
            properties=pika.BasicProperties(delivery_mode=2)  # mensagem persistente
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao publicar na fila RabbitMQ: {e}")

def publicar_resposta(resposta):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='diagnosticos_resposta', durable=True)
        mensagem = json.dumps(resposta)
        channel.basic_publish(
            exchange='',
            routing_key='diagnosticos_resposta',
            body=mensagem,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao publicar resposta no RabbitMQ: {e}")

class SintomaViewSet(viewsets.ModelViewSet):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class DiagnosticoView(APIView):
    def post(self, request):
        serializer = SintomaSerializer(data=request.data)
        if serializer.is_valid():
            dor_abdominal = int(serializer.validated_data.get('sintoma1', 0))
            ciclo_irregular = int(serializer.validated_data.get('sintoma2', 0))
            fadiga = int(serializer.validated_data.get('sintoma3', 0))
            dor_durante_sexo = 0
            intestino_preso = 0

            sintomas_dict = {
                "dor_abdominal": dor_abdominal,
                "ciclo_irregular": ciclo_irregular,
                "fadiga": fadiga,
                "dor_durante_sexo": dor_durante_sexo,
                "intestino_preso": intestino_preso,
            }

            # Publica na fila RabbitMQ os sintomas
            publicar_sintomas(sintomas_dict)

            # Monta XML SOAP
            soap_body = f'''<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="soap.carmim.diagnostico">
                <soapenv:Header/>
                <soapenv:Body>
                    <tns:analisar_sintomas>
                        <dor_abdominal>{dor_abdominal}</dor_abdominal>
                        <ciclo_irregular>{ciclo_irregular}</ciclo_irregular>
                        <fadiga>{fadiga}</fadiga>
                        <dor_durante_sexo>{dor_durante_sexo}</dor_durante_sexo>
                        <intestino_preso>{intestino_preso}</intestino_preso>
                    </tns:analisar_sintomas>
                </soapenv:Body>
            </soapenv:Envelope>'''

            try:
                soap_response = requests.post(
                    url='http://localhost:8001/',
                    data=soap_body.encode('utf-8'),
                    headers={"Content-Type": "text/xml; charset=utf-8"}
                )
                print("Resposta SOAP completa:\n", soap_response.text)

                # Extrair dados do XML SOAP para dict resposta
                root = ET.fromstring(soap_response.content)
                ns = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'soap.carmim.diagnostico'}

                body = root.find('soapenv:Body', ns)
                response = body.find('.//tns:analisar_sintomasResponse', ns)
                resultado = response.find('.//tns:analisar_sintomasResult', ns)

                diagnostico = resultado.find('tns:diagnostico', ns).text
                recomendacao = resultado.find('tns:recomendacao', ns).text

                resposta = {
                    'diagnostico': diagnostico,
                    'recomendacao': recomendacao
                }

                # Publica a resposta na fila RabbitMQ para o consumidor REST
                publicar_resposta(resposta)

                return Response({'resultado': resposta})

            except Exception as e:
                return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
