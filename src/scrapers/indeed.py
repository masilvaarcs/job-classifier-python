"""
Scraper para Indeed — Extração de vagas de emprego.
"""

from typing import List

from .base import BaseScraper
from ..models.vaga import Vaga


class IndeedScraper(BaseScraper):
    """Scraper para vagas do Indeed."""

    BASE_URL = "https://br.indeed.com/jobs"

    def __init__(self):
        super().__init__("Indeed")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do Indeed."""
        todas_vagas: List[Vaga] = []
        pagina = 0
        max_paginas = 10

        while pagina < max_paginas:
            params = {
                'q': 'desenvolvedor full stack',
                'l': 'Brasil',
                'start': pagina * 10,
            }

            soup = self.get_page(self.BASE_URL, params)
            if not soup:
                break

            cards = soup.find_all('div', class_='job_seen_beacon')
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

            pagina += 1

        print(f"✅ Indeed: {len(todas_vagas)} vagas encontradas")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de vaga do Indeed."""
        titulo_elem = card.find('h2', class_='jobTitle')
        empresa_elem = card.find('span', 'data-testid="company-name"')
        local_elem = card.find('div', 'data-testid="text-location"')
        link_elem = card.find('a', id='job_id')

        if not titulo_elem or not link_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        empresa = self.limpar_texto(empresa_elem.text) if empresa_elem else ""
        localizacao = self.limpar_texto(local_elem.text) if local_elem else ""
        link = f"https://br.indeed.com{link_elem.get('href', '')}"

        tipo = self.classificar_tipo_trabalho(f"{titulo} {localizacao}")

        return Vaga(
            titulo=titulo,
            empresa=empresa,
            localizacao=localizacao,
            tipo_trabalho=tipo,
            link=link,
            plataforma="Indeed",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        return []
