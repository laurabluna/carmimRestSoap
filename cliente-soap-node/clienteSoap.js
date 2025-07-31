const axios = require('axios');
const { parseStringPromise } = require('xml2js');

async function chamarServicoSOAP() {
  const soapBody = `
  <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:tns="soap.carmim.diagnostico">
      <soapenv:Header/>
      <soapenv:Body>
        <tns:analisar_sintomas>
          <tns:dor_abdominal>1</tns:dor_abdominal>
          <tns:ciclo_irregular>0</tns:ciclo_irregular>
          <tns:fadiga>1</tns:fadiga>
          <tns:dor_durante_sexo>0</tns:dor_durante_sexo>
          <tns:intestino_preso>0</tns:intestino_preso>
        </tns:analisar_sintomas>
      </soapenv:Body>
  </soapenv:Envelope>`;

  try {
    const { data } = await axios.post('http://localhost:8001/', soapBody, {
      headers: { 'Content-Type': 'text/xml' }
    });

    console.log('Resposta SOAP crua:\n', data);

    const json = await parseStringPromise(data, { explicitArray: true });

    const envelope = json['soapenv:Envelope'] || json['soap:Envelope'] || json['soap11env:Envelope'];
    const body = envelope?.['soapenv:Body']?.[0] || envelope?.['soap:Body']?.[0] || envelope?.['soap11env:Body']?.[0];

    const response = body?.['tns:analisar_sintomasResponse']?.[0];
    const result = response?.['tns:analisar_sintomasResult']?.[0];

    const diagnostico = result?.['tns:diagnostico']?.[0];
    const recomendacao = result?.['tns:recomendacao']?.[0];

    console.log('Diagnóstico:', diagnostico);
    console.log('Recomendação:', recomendacao);

  } catch (error) {
    console.error('Erro ao chamar serviço SOAP:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
  }
}

chamarServicoSOAP();
