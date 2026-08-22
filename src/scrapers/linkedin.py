"""
Scraper para LinkedIn — Extração de vagas de emprego.
"""

from typing import List
import re

from .base import BaseScraper
from ..models.vaga import Vaga


class LinkedInScraper(BaseScraper):
    """Scraper para vagas do LinkedIn."""

    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def __init__(self):
        super().__init__("LinkedIn")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do LinkedIn."""
        todas_vagas: List[Vaga] = []
        start = 0
        max_paginas = 25  # Limite para não sobrecarregar

        while start < max_paginas * 25:
            params = {
                'keywords': 'desenvolvedor full stack',
                'location': 'Brasil',
                'f_TPR': 'r604800',  # Últimos 7 dias
                'start': start,
            }

            soup = self.get_page(self.BASE_URL, params)
            if not soup:
                break

            cards = soup.find_all('li')
            if not cards:
                break

            for card in cards:
                try:
                    vaga = self._parse_card(card)
                    if vaga:
                        todas_vagas.append(vaga)
                except Exception as e:
                    print(f"Erro ao parsear card: {e}")
                    continue

            start += 25

        print(f"✅ LinkedIn: {len(todas_vagas)} vagas encontradas")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de vaga do LinkedIn."""
        titulo_elem = card.find('h3', class_='base-search-card__title')
        empresa_elem = card.find('h4', class_='base-search-card__subtitle')
        local_elem = card.find('span', class_='job-search-card__location')
        link_elem = card.find('a', class_='base-card__full-link')
        data_elem = card.find('time')

        if not titulo_elem or not link_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        empresa = self.limpar_texto(empresa_elem.text) if empresa_elem else ""
        localizacao = self.limpar_texto(local_elem.text) if local_elem else ""
        link = link_elem.get('href', '').split('?')[0]
        publicado = self.limpar_texto(data_elem.text) if data_elem else ""

        # Extrair job_id do link
        job_id = ""
        match = re.search(r'/view/.*?-(\d+)', link)
        if match:
            job_id = match.group(1)

        tipo = self.classificar_tipo_trabalho(f"{titulo} {localizacao}")

        return Vaga(
            titulo=titulo,
            empresa=empresa,
            localizacao=localizacao,
            publicado=publicado,
            tipo_trabalho=tipo,
            link=link,
            job_id=job_id,
            plataforma="LinkedIn",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        """Parseia HTML raw (não usado diretamente neste scraper)."""
        return []
