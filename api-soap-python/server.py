from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from modelo import prever_diagnostico_e_recomendacao

class ResultadoDiagnostico(ComplexModel):
    diagnostico = Unicode
    recomendacao = Unicode

class DiagnosticoService(ServiceBase):
    @rpc(Integer, Integer, Integer, Integer, Integer, _returns=ResultadoDiagnostico)
    def analisar_sintomas(ctx, dor_abdominal, ciclo_irregular, fadiga, dor_durante_sexo, intestino_preso):
        sintomas = {
            "dor_abdominal": dor_abdominal,
            "ciclo_irregular": ciclo_irregular,
            "fadiga": fadiga,
            "dor_durante_sexo": dor_durante_sexo,
            "intestino_preso": intestino_preso
        }
        diagnostico, recomendacao = prever_diagnostico_e_recomendacao(sintomas)
        return ResultadoDiagnostico(diagnostico=diagnostico, recomendacao=recomendacao)

application = Application(
    [DiagnosticoService],
    tns='soap.carmim.diagnostico',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("Servidor SOAP rodando em http://localhost:8001")
    server = make_server('0.0.0.0', 8001, wsgi_app)
    server.serve_forever()
