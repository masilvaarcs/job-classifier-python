"""
Scraper para Jooble — Extração de vagas de emprego.
"""

from typing import List

from .base import BaseScraper
from ..models.vaga import Vaga


class JoobleScraper(BaseScraper):
    """Scraper para vagas do Jooble."""

    BASE_URL = "https://br.jooble.org/"

    def __init__(self):
        super().__init__("Jooble")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do Jooble."""
        todas_vagas: List[Vaga] = []

        params = {
            'q': 'desenvolvedor full stack',
            'loc': 'Brasil',
        }

        soup = self.get_page(self.BASE_URL, params)
        if not soup:
            print("⚠️ Jooble: Não foi possível acessar o site")
            return []

        cards = soup.find_all('article', class_='serp-item')
        if not cards:
            cards = soup.find_all('div', class_='vacancy-item')

        for card in cards:
            try:
                vaga = self._parse_card(card)
                if vaga:
                    todas_vagas.append(vaga)
            except Exception as e:
                print(f"Erro ao parsear card: {e}")
                continue

        print(f"✅ Jooble: {len(todas_vagas)} vagas encontradas")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de vaga do Jooble."""
        titulo_elem = card.find('a', class_='serp-item__title')
        empresa_elem = card.find('span', class_='serp-item__company')
        local_elem = card.find('span', class_='serp-item__location')
        link_elem = card.find('a', class_='serp-item__title')

        if not titulo_elem or not link_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        empresa = self.limpar_texto(empresa_elem.text) if empresa_elem else ""
        localizacao = self.limpar_texto(local_elem.text) if local_elem else ""
        link = link_elem.get('href', '')

        tipo = self.classificar_tipo_trabalho(f"{titulo} {localizacao}")

        return Vaga(
            titulo=titulo,
            empresa=empresa,
            localizacao=localizacao,
            tipo_trabalho=tipo,
            link=link,
            plataforma="Jooble",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        return []
