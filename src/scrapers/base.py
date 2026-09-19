"""
Classe base abstrata para scrapers de vagas.

Todos os scrapers devem herdar desta classe e implementar
os métodos abstratos `scrap()` e `parse_vagas()`.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from bs4 import BeautifulSoup

from src.models.vaga import Vaga, TipoTrabalho


class BaseScraper(ABC):
    """Classe base para todos os scrapers de vagas."""

    def __init__(self, plataforma: str):
        self.plataforma = plataforma
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        })

    @abstractmethod
    def scrap(self) -> List[Vaga]:
        """Executa o scraping e retorna lista de vagas."""
        pass

    @abstractmethod
    def parse_vagas(self, html: str) -> List[Vaga]:
        """Parseia o HTML e extrai as vagas."""
        pass

    def get_page(self, url: str, params: Optional[dict] = None) -> Optional[BeautifulSoup]:
        """Baixa uma página e retorna o BeautifulSoup."""
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None

    @staticmethod
    def classificar_tipo_trabalho(texto: str) -> TipoTrabalho:
        """Classifica o tipo de trabalho baseado no texto."""
        texto_lower = texto.lower()

        # REMOTO
        if any(kw in texto_lower for kw in [
            'remoto', 'remote', 'home office', 'teletrabalho', 'wfh'
        ]):
            return TipoTrabalho.REMOTO

        # HÍBRIDO
        if any(kw in texto_lower for kw in [
            'híbrido', 'hybrid', 'semi-presencial'
        ]):
            return TipoTrabalho.HIBRIDO

        # PRESENCIAL
        if any(kw in texto_lower for kw in [
            'presencial', 'on-site', 'no escritório', 'escritório'
        ]):
            return TipoTrabalho.PRESENCIAL

        return TipoTrabalho.NAO_IDENTIFICADO

    @staticmethod
    def limpar_texto(texto: Optional[str]) -> str:
        """Remove espaços extras e quebras de linha."""
        if not texto:
            return ""
        return " ".join(texto.split()).strip()
