"""
Rotas do microserviço Python.

Endpoints para scraping, classificação e exportação de dados.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks

from ..models.vaga import Vaga, ScrapingResponse, ScrapingStatus
from ..services.extractor import Extractor, SCRAPERS
from ..services.classifier import classificar_lista, classificar_tipo
from ..services.exporter import exportar_excel

router = APIRouter()
extractor = Extractor()


@router.get("/")
async def info():
    """Informações do microserviço."""
    return {
        "name": "Job Classifier — Python Microservice",
        "version": "1.0.0",
        "description": "Microserviço de extração de dados de vagas de emprego",
        "plataformas": list(SCRAPERS.keys()),
        "endpoints": {
            "scraping": "/scraping/{plataforma}",
            "scraping_todas": "/scraping/todas",
            "status": "/scraping/status",
            "dados": "/dados/{plataforma}",
            "classificar": "/classificar",
            "exportar": "/exportar/{plataforma}",
        },
    }


@router.post("/scraping/{plataforma}")
async def scraping_plataforma(plataforma: str, background_tasks: BackgroundTasks):
    """Executa scraping de uma plataforma específica."""
    if plataforma not in SCRAPERS:
        raise HTTPException(
            status_code=400,
            detail=f"Plataforma não suportada: {plataforma}. Use: {list(SCRAPERS.keys())}"
        )

    # Executar em background
    background_tasks.add_task(extractor.extrair_plataforma, plataforma)

    return ScrapingResponse(
        message=f"Scraping iniciado para {plataforma}",
        plataforma=plataforma,
    )


@router.post("/scraping/todas")
async def scraping_todas(background_tasks: BackgroundTasks):
    """Executa scraping de todas as plataformas."""
    background_tasks.add_task(extractor.extrair_todas)

    return {
        "message": "Scraping iniciado para todas as plataformas",
        "plataformas": list(SCRAPERS.keys()),
    }


@router.get("/scraping/status")
async def scraping_status():
    """Retorna o status das execuções de scraping."""
    return extractor.get_status()


@router.get("/dados/{plataforma}")
async def dados_plataforma(plataforma: str):
    """Retorna os dados extraídos de uma plataforma."""
    dados = extractor.get_dados(plataforma)
    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para {plataforma}"
        )
    return {"plataforma": plataforma, "total": len(dados), "vagas": dados}


@router.get("/dados")
async def dados_todos():
    """Retorna todos os dados extraídos."""
    dados = extractor.get_dados()
    return {"total": len(dados), "vagas": dados}


@router.post("/classificar")
async def classificar_dados(vagas: List[Vaga]):
    """Classifica o tipo de trabalho de uma lista de vagas."""
    vagas_classificadas = classificar_lista(vagas)
    return {"total": len(vagas_classificadas), "vagas": vagas_classificadas}


@router.post("/classificar/{plataforma}")
async def classificar_plataforma(plataforma: str):
    """Classifica as vagas já extraídas de uma plataforma."""
    dados = extractor.get_dados(plataforma)
    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para {plataforma}"
        )

    vagas = [Vaga(**d) for d in dados]
    vagas_classificadas = classificar_lista(vagas)

    return {
        "plataforma": plataforma,
        "total": len(vagas_classificadas),
        "vagas": [v.model_dump(mode='json') for v in vagas_classificadas],
    }


@router.post("/exportar/{plataforma}")
async def exportar_plataforma(plataforma: str):
    """Gera planilha Excel de uma plataforma."""
    dados = extractor.get_dados(plataforma)
    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para {plataforma}"
        )

    vagas = [Vaga(**d) for d in dados]
    arquivo = exportar_excel(vagas, plataforma)

    return {
        "message": f"Planilha gerada com sucesso",
        "plataforma": plataforma,
        "arquivo": arquivo,
        "total": len(vagas),
    }
