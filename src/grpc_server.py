"""
Job Classifier — Servidor gRPC nativo do microserviço Python.

Expõe o serviço job.v1.ScrapingService (proto/job/v1/scraping.proto)
na porta 8002. Consumido pelo serviço Node (job-classifier-rpc)
via gRPC nativo (HTTP/2).

Executar: python -m src.grpc_server
"""

import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import grpc

# Stubs gerados pelo grpcio-tools em src/gen (pacote job/v1)
GEN_DIR = Path(__file__).resolve().parent / 'gen'
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from job.v1 import scraping_pb2, scraping_pb2_grpc, vagas_pb2  # noqa: E402

from .services.extractor import Extractor, SCRAPERS  # noqa: E402

extractor = Extractor()


class ScrapingServiceServicer(scraping_pb2_grpc.ScrapingServiceServicer):
    """Implementação do job.v1.ScrapingService."""

    def StartScraping(self, request, context):
        plataforma = request.plataforma or ''

        if plataforma and plataforma not in SCRAPERS:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Plataforma não suportada: {plataforma}. Use: {list(SCRAPERS.keys())} ou vazio para todas.",
            )

        alvo = [plataforma] if plataforma else list(SCRAPERS.keys())

        # Executa o scraping em background (mesmo comportamento do FastAPI)
        for plat in alvo:
            thread = threading.Thread(
                target=self._executar,
                args=(plat,),
                daemon=True,
                name=f"scraping-{plat}",
            )
            thread.start()

        return scraping_pb2.ScrapingServiceStartScrapingResponse(
            iniciado=True,
            mensagem=f"Scraping iniciado para {', '.join(alvo)}",
            plataformas=alvo,
        )

    def GetStatus(self, request, context):
        status = extractor.get_status()
        resp = scraping_pb2.ScrapingServiceGetStatusResponse()
        for plat, info in status.items():
            resp.plataformas.append(
                vagas_pb2.PlataformaStatus(
                    plataforma=plat,
                    status=info.get('status', ''),
                    inicio=info.get('inicio', ''),
                    fim=info.get('fim', ''),
                    vagas_encontradas=info.get('vagas_encontradas', 0),
                    erro=info.get('erro', ''),
                )
            )
        return resp

    @staticmethod
    def _executar(plataforma: str) -> None:
        try:
            extractor.extrair_plataforma(plataforma)
        except Exception as e:  # status de erro é registrado pelo Extractor
            print(f"❌ Erro no scraping de {plataforma}: {e}")


def serve() -> None:
    port = int(os.getenv('GRPC_PORT', '8002'))
    server = grpc.server(
        ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_receive_message_length', 32 * 1024 * 1024),
            ('grpc.max_send_message_length', 32 * 1024 * 1024),
        ],
    )
    scraping_pb2_grpc.add_ScrapingServiceServicer_to_server(
        ScrapingServiceServicer(), server
    )
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    # Sem emoji: o console Windows (cp1252) não suporta caracteres fora do ASCII
    print(f'gRPC Job Classifier (ScrapingService) em http://0.0.0.0:{port}')
    print('Contrato: proto/job/v1/scraping.proto (service job.v1.ScrapingService)')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
