"""
Serviço de classificação de tipo de trabalho.

Classifica vagas como REMOTO, HÍBRIDO ou PRESENCIAL
baseado em keywords e heurísticas.
"""

from typing import List

from ..models.vaga import Vaga, TipoTrabalho


# Keywords para classificação
KEYWORDS_REMOTO = [
    'remoto', 'remote', 'home office', 'teletrabalho', 'wfh',
    'trabalho remoto', 'anywhere', 'global',
]

KEYWORDS_HIBRIDO = [
    'híbrido', 'hybrid', 'semi-presencial', 'flexível',
]

KEYWORDS_PRESENCIAL = [
    'presencial', 'on-site', 'no escritório', 'escritório',
    'office', 'local fixo',
]

# Cidades que indicam presencial
CIDADES_PRESENCIAIS = [
    'gravataí', 'porto alegre', 'poa', 'curitiba', 'são paulo',
    'rio de janeiro', 'belo horizonte', 'brasília', 'salvador',
]


def classificar_tipo(vaga: Vaga) -> TipoTrabalho:
    """Classifica o tipo de trabalho de uma vaga."""
    texto = f"{vaga.titulo} {vaga.descricao} {vaga.modalidade} {vaga.localizacao}".lower()

    # Verificar keywords de remoto
    for kw in KEYWORDS_REMOTO:
        if kw in texto:
            return TipoTrabalho.REMOTO

    # Verificar keywords de híbrido
    for kw in KEYWORDS_HIBRIDO:
        if kw in texto:
            return TipoTrabalho.HIBRIDO

    # Verificar keywords de presencial
    for kw in KEYWORDS_PRESENCIAIS:
        if kw in texto:
            return TipoTrabalho.PRESENCIAL

    # Heurística: se menciona uma cidade específica, provavelmente é presencial
    for cidade in CIDADES_PRESENCIAIS:
        if cidade in vaga.localizacao.lower():
            return TipoTrabalho.PRESENCIAL

    return TipoTrabalho.NAO_IDENTIFICADO


def classificar_lista(vagas: List[Vaga]) -> List[Vaga]:
    """Classifica uma lista de vagas."""
    for vaga in vagas:
        vaga.tipo_trabalho = classificar_tipo(vaga)
    return vagas
