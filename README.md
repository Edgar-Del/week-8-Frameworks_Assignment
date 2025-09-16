CORD-19 Metadata Explorer

Overview
Simple EDA and a Streamlit app for the CORD-19 `metadata.csv` file.

Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Data
Download `metadata.csv` from the CORD-19 dataset and place it at `data/metadata.csv`.

Run analysis (saves figures to `outputs/figures`)
```bash
python scripts/analyze.py --input data/metadata.csv --outdir outputs/figures
```

Run Streamlit app
```bash
streamlit run app/streamlit_app.py
```

Project structure
- `scripts/analyze.py`: EDA, cleaning, figures
- `app/streamlit_app.py`: Streamlit app
- `data/`: `metadata.csv` (not versioned)
- `outputs/figures/`: generated plots
Frameworks_Assignment — CORD-19 (metadata)

Descrição
Este projeto realiza uma análise exploratória simplificada do arquivo `metadata.csv` do dataset CORD-19 e disponibiliza uma aplicação Streamlit para explorar resultados.

Estrutura
- `data/`: coloque aqui o `metadata.csv` (não versionado)
- `scripts/analyze.py`: script de EDA, limpeza e geração de figuras
- `outputs/figures/`: gráficos e nuvem de palavras gerados
- `app/streamlit_app.py`: app Streamlit
- `notebooks/`: (opcional) notebook de exploração

Pré-requisitos
- Python 3.8+
- `pip` ou `uv`/`pipenv`

Instalação
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Dados
Baixe apenas o `metadata.csv` do desafio CORD-19 e salve em `data/metadata.csv`.

Executar a análise (gera figuras)
```bash
python scripts/analyze.py --input data/metadata.csv --outdir outputs/figures
```

Executar o app Streamlit
```bash
streamlit run app/streamlit_app.py
```

Resultados esperados
- Gráficos: publicações por ano, top periódicos, distribuição por fonte
- Nuvem de palavras de títulos
- Versão limpa dos dados em memória no app

Licença
Uso acadêmico/educacional.

