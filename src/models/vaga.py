from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoTrabalho(str, Enum):
    REMOTO = "REMOTO"
    HIBRIDO = "HIBRIDO"
    PRESENCIAL = "PRESENCIAL"
    NAO_IDENTIFICADO = "NAO IDENTIFICADO"


class Vaga(BaseModel):
    """Modelo de dados para uma vaga de emprego."""
    
    titulo: str = Field(..., description="Título da vaga")
    empresa: Optional[str] = Field(default="", description="Nome da empresa")
    localizacao: Optional[str] = Field(default="", description="Localização da vaga")
    salario: Optional[str] = Field(default="", description="Salário oferecido")
    modalidade: Optional[str] = Field(default="", description="Modalidade de trabalho")
    publicado: Optional[str] = Field(default="", description="Data de publicação (texto)")
    data_publicacao: Optional[datetime] = Field(default=None, description="Data de publicação")
    tipo_trabalho: TipoTrabalho = Field(
        default=TipoTrabalho.NAO_IDENTIFICADO,
        description="Tipo: REMOTO, HIBRIDO, PRESENCIAL"
    )
    descricao: Optional[str] = Field(default="", description="Descrição da vaga")
    link: str = Field(..., description="Link da vaga (chave de deduplicação)")
    job_id: Optional[str] = Field(default="", description="ID da vaga na plataforma")
    plataforma: str = Field(..., description="Plataforma de origem")

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Desenvolvedor Full Stack",
                "empresa": "Empresa X",
                "localizacao": "São Paulo, SP",
                "salario": "R$ 8.000-12.000",
                "modalidade": "Home Office",
                "publicado": "há 2 dias",
                "data_publicacao": "2026-08-20T00:00:00",
                "tipo_trabalho": "REMOTO",
                "descricao": "Buscamos desenvolvedor...",
                "link": "https://...",
                "job_id": "abc123",
                "plataforma": "LinkedIn",
            }
        }


class VagaCreate(BaseModel):
    """Modelo para criação de vaga (campos obrigatórios mínimos)."""
    titulo: str
    link: str
    plataforma: str
    empresa: Optional[str] = ""
    localizacao: Optional[str] = ""
    salario: Optional[str] = ""
    modalidade: Optional[str] = ""
    publicado: Optional[str] = ""
    data_publicacao: Optional[str] = None
    tipo_trabalho: Optional[str] = "NAO IDENTIFICADO"
    descricao: Optional[str] = ""
    job_id: Optional[str] = ""


class ScrapingStatus(BaseModel):
    """Status de execução de scraping."""
    plataforma: str
    status: str  # "em_andamento" | "concluido" | "erro"
    vagas_encontradas: int = 0
    inicio: Optional[datetime] = None
    fim: Optional[datetime] = None
    erro: Optional[str] = None


class ScrapingResponse(BaseModel):
    """Resposta de uma operação de scraping."""
    message: str
    plataforma: str
    vagas_encontradas: int = 0
    arquivo_gerado: Optional[str] = None
