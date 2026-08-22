"""
Serviço de exportação para Excel.

Gera planilhas formatadas com cores por tipo de trabalho.
"""

import os
from typing import List
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from ..models.vaga import Vaga, TipoTrabalho


# Cores por tipo de trabalho
CORES = {
    TipoTrabalho.REMOTO: PatternFill(start_color='DCfce7', end_color='DCfce7', fill_type='solid'),
    TipoTrabalho.HIBRIDO: PatternFill(start_color='fef9c3', end_color='fef9c3', fill_type='solid'),
    TipoTrabalho.PRESENCIAL: PatternFill(start_color='ffedd5', end_color='ffedd5', fill_type='solid'),
    TipoTrabalho.NAO_IDENTIFICADO: PatternFill(start_color='f3f4f6', end_color='f3f4f6', fill_type='solid'),
}

HEADER_FILL = PatternFill(start_color='1e3a5f', end_color='1e3a5f', fill_type='solid')
HEADER_FONT = Font(name='Calibri', size=11, bold=True, color='FFFFFF')

CABECALHOS = [
    'Título', 'Empresa', 'Localização', 'Salário', 'Modalidade',
    'Tipo', 'Plataforma', 'Publicado', 'Link', 'Descrição',
]


def exportar_excel(vagas: List[Vaga], plataforma: str) -> str:
    """Exporta uma lista de vagas para Excel formatado."""
    wb = Workbook()
    ws = wb.active
    ws.title = f'Vagas {plataforma}'

    # Estilo da borda
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )

    # Cabeçalhos
    for col, cabecalho in enumerate(CABECALHOS, 1):
        cell = ws.cell(row=1, column=col, value=cabecalho)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border

    # Dados
    for row, vaga in enumerate(vagas, 2):
        tipo_cor = CORES.get(vaga.tipo_trabalho, CORES[TipoTrabalho.NAO_IDENTIFICADO])

        dados = [
            vaga.titulo,
            vaga.empresa,
            vaga.localizacao,
            vaga.salario,
            vaga.modalidade,
            vaga.tipo_trabalho.value,
            vaga.plataforma,
            vaga.publicado,
            vaga.link,
            vaga.descricao[:200] if vaga.descricao else '',
        ]

        for col, valor in enumerate(dados, 1):
            cell = ws.cell(row=row, column=col, value=valor)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center', wrap_text=True)

            # Aplicar cor da linha baseada no tipo
            if col == 6:  # Coluna "Tipo"
                cell.fill = tipo_cor

    # Ajustar largura das colunas
    larguras = [40, 25, 25, 15, 15, 15, 12, 15, 50, 60]
    for col, largura in enumerate(larguras, 1):
        ws.column_dimensions[chr(64 + col)].width = largura

    # Congelar primeira linha
    ws.freeze_panes = 'A2'

    # Salvar
    data_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Vagas_{plataforma}_{data_str}.xlsx'
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output', filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    wb.save(filepath)

    return filepath
