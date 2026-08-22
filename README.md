# 🐍 Job Classifier — Microserviço Python

> Microserviço de extração de dados de vagas de emprego via scraping multi-plataforma.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.12-FF6B35)](https://www.crummy.com/software/BeautifulSoup/)

---

## 🚀 Funcionalidades

- **Scraping multi-plataforma**: LinkedIn, Indeed, Jooble, Freelancer, Glassdoor, BNE
- **Classe base abstrata** para fácil adição de novos scrapers
- **Classificação automática** de tipo de trabalho (Remoto/Híbrido/Presencial)
- **Exportação para Excel** com cores por tipo de trabalho
- **API FastAPI** com documentação interativa (Swagger/ReDoc)
- **Background tasks** para execução assíncrona de scraping
- **Deduplicação** automática por campo `link`

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11+ | Runtime |
| FastAPI | 0.115 | Web Framework |
| Uvicorn | 0.30+ | ASGI Server |
| Pydantic | 2.9+ | Validação de dados |
| requests | 2.32+ | HTTP Client |
| BeautifulSoup4 | 4.12+ | HTML Parsing |
| openpyxl | 3.1+ | Excel Export |
| lxml | 5.0+ | XML/HTML Parser |

---

## 📁 Estrutura do Projeto

```
src/
├── scrapers/
│   ├── __init__.py
│   ├── base.py            ← Classe base abstrata
│   ├── linkedin.py        ← Scraper LinkedIn
│   ├── indeed.py          ← Scraper Indeed
│   ├── jooble.py          ← Scraper Jooble
│   ├── freelancer.py      ← Scraper Freelancer
│   ├── glassdoor.py       ← Scraper Glassdoor
│   └── bne.py             ← Scraper BNE Brasil
├── services/
│   ├── __init__.py
│   ├── extractor.py       ← Orquestrador de extração
│   ├── classifier.py      ← Classificação tipo trabalho
│   └── exporter.py        ← Geração de Excel
├── models/
│   ├── __init__.py
│   └── vaga.py            ← Pydantic models
├── api/
│   ├── __init__.py
│   └── routes.py          ← Endpoints FastAPI
└── main.py                ← App FastAPI
```

---

## ⚙️ Configuração

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/masilvaarcs/job-classifier-python.git
cd job-classifier-python

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Iniciar servidor
python -m uvicorn src.main:app --reload --port 8001
```

Acessar: `http://localhost:8001`
Docs: `http://localhost:8001/docs`

---

## 📡 API Endpoints

### Informação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Info do microserviço |
| GET | `/health` | Health check |

### Scraping
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/scraping/{plataforma}` | Scraping de uma plataforma |
| POST | `/scraping/todas` | Scraping de todas as plataformas |
| GET | `/scraping/status` | Status das execuções |

### Dados
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/dados/{plataforma}` | Dados de uma plataforma |
| GET | `/dados` | Todos os dados |

### Processamento
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/classificar` | Classificar lista de vagas |
| POST | `/classificar/{plataforma}` | Classificar vagas extraídas |
| POST | `/exportar/{plataforma}` | Gerar Excel |

### Plataformas Suportadas
- `LinkedIn` — LinkedIn Jobs
- `Indeed` — Indeed Brasil
- `Jooble` — Jooble Brasil
- `Freelancer` — Freelancer.com
- `Glassdoor` — Glassdoor
- `BNE` — Banco Nacional de Empregos

---

## 🔧 Como Adicionar um Novo Scraper

1. Criar arquivo em `src/scrapers/minha_plataforma.py`:

```python
from .base import BaseScraper
from ..models.vaga import Vaga
from typing import List

class MinhaPlataformaScraper(BaseScraper):
    def __init__(self):
        super().__init__("MinhaPlataforma")

    def scrap(self) -> List[Vaga]:
        # Lógica de scraping
        soup = self.get_page("https://exemplo.com/vagas")
        return self.parse_vagas(str(soup))

    def parse_vagas(self, html: str) -> List[Vaga]:
        # Parse do HTML
        return []
```

2. Registrar em `src/services/extractor.py`:

```python
from ..scrapers.minha_plataforma import MinhaPlataformaScraper

SCRAPERS['MinhaPlataforma'] = MinhaPlataformaScraper
```

---

## 📦 Exportação Excel

O Excel é gerado com formatação profissional:
- **Cabeçalho**: Fundo azul escuro (#1e3a5f) com texto branco
- **Linhas**: Cores por tipo de trabalho
  - 🟢 Verde claro: Remoto
  - 🟡 Amarelo claro: Híbrido
  - 🟠 Laranja claro: Presencial
  - ⚪ Cinza: Não identificado
- **Largura**: Ajustada automaticamente
- **Congelamento**: Primeira linha fixa

---

## 📋 Projeto Completo

Este repositório faz parte do projeto **Job Classifier**, composto por:

| Repositório | Tecnologia | Descrição |
|---|---|---|
| [job-classifier-react](https://github.com/masilvaarcs/job-classifier-react) | React + TypeScript | Frontend |
| [job-classifier-api](https://github.com/masilvaarcs/job-classifier-api) | Node.js + Express | API REST |
| [job-classifier-python](https://github.com/masilvaarcs/job-classifier-python) | Python + FastAPI | Microserviço (este repositório) |

---

## 👤 Autor

**Marcos Santos da Silva**
- Desenvolvedor Full Stack Sênior
- [GitHub](https://github.com/masilvaarcs)
- [LinkedIn](https://linkedin.com/in/marcosprogramador)

---

## 📄 Licença

MIT
