from zeep import Client

client = Client('http://localhost:8001/?wsdl')
resposta = client.service.ping()
print(resposta)
