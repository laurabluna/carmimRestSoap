from django.shortcuts import render
from rest_framework import viewsets
from .models import Sintoma
from .serializers import SintomaSerializer

class SintomaViewSet(viewsets.ModelViewSet):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class DiagnosticoView(APIView):
    def post(self, request):
        serializer = SintomaSerializer(data=request.data)
        if serializer.is_valid():
            sintomas = [
                serializer.validated_data['sintoma1'],
                serializer.validated_data['sintoma2'],
                serializer.validated_data['sintoma3']
            ]

            soap_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.soap/">
               <soapenv:Header/>
               <soapenv:Body>
                  <ser:diagnosticar>
                     <sintomas>{','.join(sintomas)}</sintomas>
                  </ser:diagnosticar>
               </soapenv:Body>
            </soapenv:Envelope>
            """

            try:
                soap_response = requests.post(
                    url='http://localhost:8001/ws',
                    data=soap_body,
                    headers={"Content-Type": "text/xml"}
                )
                return Response({'resultado': soap_response.text})
            except Exception as e:
                return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)