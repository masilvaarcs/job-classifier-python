"""
Scraper para BNE Brasil — Extração de vagas de emprego.
"""

from typing import List

from .base import BaseScraper
from ..models.vaga import Vaga


class BNEScraper(BaseScraper):
    """Scraper para vagas do BNE (Banco Nacional de Empregos)."""

    BASE_URL = "https://www.bne.com.br/vagas-de-emprego"

    def __init__(self):
        super().__init__("BNE")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do BNE."""
        todas_vagas: List[Vaga] = []

        # Buscar por diferentes termos
        termos = ['desenvolvedor', 'programador', 'analista de sistemas']

        for termo in termos:
            params = {
                'q': termo,
                'where': '',
            }

            soup = self.get_page(self.BASE_URL, params)
            if not soup:
                continue

            cards = soup.find_all('div', class_='card-vaga')
            if not cards:
                cards = soup.find_all('div', class_='vaga-card')

            for card in cards:
                try:
                    vaga = self._parse_card(card)
                    if vaga:
                        todas_vagas.append(vaga)
                except Exception as e:
                    print(f"Erro ao parsear card: {e}")
                    continue

        print(f"✅ BNE: {len(todas_vagas)} vagas encontradas")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de vaga do BNE."""
        titulo_elem = card.find('h2', class_='card-vaga__titulo')
        empresa_elem = card.find('p', class_='card-vaga__empresa')
        local_elem = card.find('p', class_='card-vaga__localizacao')
        link_elem = card.find('a', class_='card-vaga')

        if not titulo_elem or not link_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        empresa = self.limpar_texto(empresa_elem.text) if empresa_elem else ""
        localizacao = self.limpar_texto(local_elem.text) if local_elem else ""
        link = f"https://www.bne.com.br{link_elem.get('href', '')}"

        tipo = self.classificar_tipo_trabalho(f"{titulo} {localizacao}")

        return Vaga(
            titulo=titulo,
            empresa=empresa,
            localizacao=localizacao,
            tipo_trabalho=tipo,
            link=link,
            plataforma="BNE",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        return []
