"""
Scraper para Freelancer — Extração de projetos.
"""

from typing import List

from .base import BaseScraper
from ..models.vaga import Vaga, TipoTrabalho


class FreelancerScraper(BaseScraper):
    """Scraper para projetos do Freelancer."""

    BASE_URL = "https://www.freelancer.com/jobs/"

    def __init__(self):
        super().__init__("Freelancer")

    def scrap(self) -> List[Vaga]:
        """Executa o scraping do Freelancer."""
        todas_vagas: List[Vaga] = []

        params = {
            'query': 'desenvolvimento web',
        }

        soup = self.get_page(self.BASE_URL, params)
        if not soup:
            print("⚠️ Freelancer: Não foi possível acessar o site")
            return []

        cards = soup.find_all('div', class_='job-tile')
        if not cards:
            cards = soup.find_all('section', class_='job-tile')

        for card in cards:
            try:
                vaga = self._parse_card(card)
                if vaga:
                    todas_vagas.append(vaga)
            except Exception as e:
                print(f"Erro ao parsear card: {e}")
                continue

        print(f"✅ Freelancer: {len(todas_vagas)} projetos encontrados")
        return todas_vagas

    def _parse_card(self, card) -> Vaga:
        """Parseia um card de projeto do Freelancer."""
        titulo_elem = card.find('a', class_='job-tile-title-link')
        desc_elem = card.find('div', class_='job-tile-description')
        budget_elem = card.find('div', class_='job-tile-budget')

        if not titulo_elem:
            return None

        titulo = self.limpar_texto(titulo_elem.text)
        descricao = self.limpar_texto(desc_elem.text) if desc_elem else ""
        salario = self.limpar_texto(budget_elem.text) if budget_elem else ""
        link = f"https://www.freelancer.com{titulo_elem.get('href', '')}"

        # Freelancer empresas são sempre remoto
        return Vaga(
            titulo=titulo,
            descricao=descricao,
            salario=salario,
            tipo_trabalho=TipoTrabalho.REMOTO,
            link=link,
            plataforma="Freelancer",
        )

    def parse_vagas(self, html: str) -> List[Vaga]:
        return []
