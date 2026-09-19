"""
Serviço orquestrador de extração de dados.

Coordena a execução de todos os scrapers e salva os resultados.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from src.scrapers.linkedin import LinkedInScraper
from src.scrapers.indeed import IndeedScraper
from src.scrapers.jooble import JoobleScraper
from src.scrapers.freelancer import FreelancerScraper
from src.scrapers.glassdoor import GlassdoorScraper
from src.scrapers.bne import BNEScraper
from src.models.vaga import Vaga


# Mapa de scrapers disponíveis
SCRAPERS = {
    'LinkedIn': LinkedInScraper,
    'Indeed': IndeedScraper,
    'Jooble': JoobleScraper,
    'Freelancer': FreelancerScraper,
    'Glassdoor': GlassdoorScraper,
    'BNE': BNEScraper,
}

# Diretório de saída
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output')


class Extractor:
    """Orquestrador de extração de dados de vagas."""

    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self._status: Dict[str, dict] = {}

    def extrair_plataforma(self, plataforma: str) -> List[Vaga]:
        """Executa scraping de uma plataforma específica."""
        if plataforma not in SCRAPERS:
            raise ValueError(f"Plataforma não suportada: {plataforma}")

        self._status[plataforma] = {
            'status': 'em_andamento',
            'inicio': datetime.now().isoformat(),
            'vagas_encontradas': 0,
        }

        try:
            scraper_class = SCRAPERS[plataforma]
            scraper = scraper_class()
            vagas = scraper.scrap()

            # Salvar JSON
            arquivo = self._salvar_json(plataforma, vagas)

            self._status[plataforma] = {
                'status': 'concluido',
                'inicio': self._status[plataforma]['inicio'],
                'fim': datetime.now().isoformat(),
                'vagas_encontradas': len(vagas),
                'arquivo': arquivo,
            }

            return vagas

        except Exception as e:
            self._status[plataforma] = {
                'status': 'erro',
                'inicio': self._status[plataforma]['inicio'],
                'fim': datetime.now().isoformat(),
                'erro': str(e),
                'vagas_encontradas': 0,
            }
            raise

    def extrair_todas(self) -> Dict[str, List[Vaga]]:
        """Executa scraping de todas as plataformas."""
        resultados: Dict[str, List[Vaga]] = {}

        for plataforma in SCRAPERS.keys():
            try:
                vagas = self.extrair_plataforma(plataforma)
                resultados[plataforma] = vagas
            except Exception as e:
                print(f"❌ Erro ao extrair {plataforma}: {e}")
                resultados[plataforma] = []

        return resultados

    def _salvar_json(self, plataforma: str, vagas: List[Vaga]) -> str:
        """Salva as vagas em um arquivo JSON."""
        arquivo = os.path.join(OUTPUT_DIR, f'vagas_{plataforma.lower()}_todas.json')

        dados = [vaga.model_dump(mode='json') for vaga in vagas]

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=str)

        return arquivo

    def get_status(self) -> Dict[str, dict]:
        """Retorna o status de todas as execuções."""
        return self._status

    def get_dados(self, plataforma: Optional[str] = None) -> List[dict]:
        """Retorna os dados extraídos (JSON)."""
        if plataforma:
            arquivo = os.path.join(OUTPUT_DIR, f'vagas_{plataforma.lower()}_todas.json')
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []

        # Todos os dados
        todos_dados = []
        for plat in SCRAPERS.keys():
            arquivo = os.path.join(OUTPUT_DIR, f'vagas_{plat.lower()}_todas.json')
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    todos_dados.extend(json.load(f))
        return todos_dados

