const express = require('express');
const axios = require('axios');
const { parseStringPromise } = require('xml2js');

const app = express();
app.use(express.json());

const sintomasMapeados = ['dor_abdominal', 'ciclo_irregular', 'fadiga', 'dor_durante_sexo', 'intestino_preso'];

function sintomasParaVetor(sintomasSelecionados) {
  return sintomasMapeados.map(s => sintomasSelecionados.includes(s) ? 1 : 0);
}

app.post('/api/diagnostico', async (req, res) => {
  const { sintomas } = req.body;

  if (!sintomas || !Array.isArray(sintomas)) {
    return res.status(400).json({ error: 'Sintomas inválidos.' });
  }

  const vetor = sintomasParaVetor(sintomas);

  const soapBody = `
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="soap.carmim.diagnostico">
      <soapenv:Header/>
      <soapenv:Body>
        <tns:analisar_sintomas>
          <tns:dor_abdominal>${vetor[0]}</tns:dor_abdominal>
          <tns:ciclo_irregular>${vetor[1]}</tns:ciclo_irregular>
          <tns:fadiga>${vetor[2]}</tns:fadiga>
          <tns:dor_durante_sexo>${vetor[3]}</tns:dor_durante_sexo>
          <tns:intestino_preso>${vetor[4]}</tns:intestino_preso>
        </tns:analisar_sintomas>
      </soapenv:Body>
    </soapenv:Envelope>`;

  try {
    const { data } = await axios.post('http://localhost:8001/', soapBody, {
      headers: { 'Content-Type': 'text/xml' }
    });

    console.log('Resposta SOAP crua:', data);

    const json = await parseStringPromise(data, { explicitArray: true });
    console.log('Resposta JSON:', JSON.stringify(json, null, 2));

    const envelope = json['soapenv:Envelope'] || json['soap:Envelope'] || json['soap11env:Envelope'];
    const body = envelope?.['soapenv:Body']?.[0] || envelope?.['soap:Body']?.[0] || envelope?.['soap11env:Body']?.[0];

    const response = body?.['tns:analisar_sintomasResponse']?.[0];
    const result = response?.['tns:analisar_sintomasResult']?.[0];

    const diagnostico = result?.['tns:diagnostico']?.[0];
    const recomendacao = result?.['tns:recomendacao']?.[0];

    if (!diagnostico || !recomendacao) {
      throw new Error('Dados não encontrados na resposta SOAP.');
    }

    res.json({ diagnostico, recomendacao });

  } catch (error) {
    console.error('Erro ao consultar o serviço SOAP:', error.message);

    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Headers:', error.response.headers);
      console.error('Data:', error.response.data);
    }

    res.status(500).send('Erro ao consultar serviço SOAP');
  }
});

app.listen(3001, () => {
  console.log('Gateway rodando em http://localhost:3001');
});
