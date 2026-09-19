"""
Scraper para Glassdoor — Extração de vagas de emprego.
"""

from typing import List

from .base import BaseScraper
from src.models.vaga import Vaga


class GlassdoorScraper(BaseScraper):
    """Scraper para vagas do Glassdoor."""

    BASE_URL = "https://www.glassdoor.com/Job/brasil-desenvolvedor-full-stack-jobs-SRCH_IL.0,6_IN36_KO7,31.htm"

    def __init__(self):
        super().__init__("Glassdoor")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do Glassdoor."""
        todas_vagas: List[Vaga] = []

        soup = self.get_page(self.BASE_URL)
        if not soup:
            print("⚠️ Glassdoor: Não foi possível acessar o site (proteções anti-bot)")
            return []

        cards = soup.find_all('li', class_='JobsList_jobListItem__wjTHv')
        if not cards:
            cards = soup.find_all('li', attrs={'data-test': 'jobListing'})

        for card in cards:
            try:
                vaga = self._parse_card(card)
                if vaga:
                    todas_vagas.append(vaga)
            except Exception as e:
                print(f"Erro ao parsear card: {e}")
                continue

        print(f"✅ Glassdoor: {len(todas_vagas)} vagas encontradas")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de vaga do Glassdoor."""
        titulo_elem = card.find('a', class_='JobCard_jobTitle__GLyJ1')
        empresa_elem = card.find('div', class_='EmployerProfile_compactEmployerName__LE242')
        local_elem = card.find('div', class_='JobCard_jobLocation__bsqjU')
        link_elem = card.find('a', class_='JobCard_jobTitle__GLyJ1')

        if not titulo_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        empresa = self.limpar_texto(empresa_elem.text) if empresa_elem else ""
        localizacao = self.limpar_texto(local_elem.text) if local_elem else ""
        link = f"https://www.glassdoor.com{link_elem.get('href', '')}" if link_elem else ""

        tipo = self.classificar_tipo_trabalho(f"{titulo} {localizacao}")

        return Vaga(
            titulo=titulo,
            empresa=empresa,
            localizacao=localizacao,
            tipo_trabalho=tipo,
            link=link,
            plataforma="Glassdoor",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        return []


