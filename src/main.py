"""
Job Classifier — Python Microservice

Microserviço de extração de dados de vagas de emprego.
Responsável por scraping, classificação e exportação.
"""

import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router

# Carregar variáveis de ambiente
load_dotenv()

# Criar app
app = FastAPI(
    title="Job Classifier — Python Microservice",
    description="Microserviço de extração de dados de vagas de emprego",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(router)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "job-classifier-python"}


# Iniciar servidor
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
