import argparse
from pathlib import Path
from collections import Counter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False)
    return df


def basic_exploration(df: pd.DataFrame) -> None:
    print("Dimensões:", df.shape)
    print("Tipos:\n", df.dtypes)
    print("Nulos (top 20):\n", df.isnull().sum().sort_values(ascending=False).head(20))
    print("Estatísticas numéricas:\n", df.describe(include=[np.number]))


def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalizar nomes esperados do CORD-19
    expected_cols = {
        "publish_time": "publish_time",
        "title": "title",
        "abstract": "abstract",
        "journal": "journal",
        "source_x": "source",
        "source": "source",
        "authors": "authors",
    }
    # Renomear se existir
    renames = {}
    for col in df.columns:
        if col in expected_cols and expected_cols[col] != col:
            renames[col] = expected_cols[col]
    if renames:
        df = df.rename(columns=renames)

    # Garantir colunas-chave
    for col in ["publish_time", "title", "abstract", "journal", "source"]:
        if col not in df.columns:
            df[col] = np.nan

    # Converter data
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year

    # Limpeza simples de strings
    for col in ["title", "abstract", "journal", "source"]:
        df[col] = df[col].astype("string").str.strip()

    # Contagem de palavras do título/abstract
    df["title_word_count"] = df["title"].fillna("").str.split().apply(len)
    df["abstract_word_count"] = df["abstract"].fillna("").str.split().apply(len)

    return df


def plot_publications_by_year(df: pd.DataFrame, outdir: Path) -> Path:
    counts = df["year"].dropna().value_counts().sort_index()
    plt.figure(figsize=(8, 4))
    sns.barplot(x=counts.index.astype(int), y=counts.values, color="#1f77b4")
    plt.title("Publicações por ano")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    outpath = outdir / "publications_by_year.png"
    plt.savefig(outpath, dpi=150)
    plt.close()
    return outpath


def plot_top_journals(df: pd.DataFrame, outdir: Path, top_n: int = 10) -> Path:
    counts = (
        df["journal"].dropna().replace("", np.nan).dropna().value_counts().head(top_n)
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(y=counts.index, x=counts.values, color="#2ca02c")
    plt.title(f"Top {top_n} periódicos")
    plt.xlabel("Quantidade")
    plt.ylabel("Periódico")
    plt.tight_layout()
    outpath = outdir / "top_journals.png"
    plt.savefig(outpath, dpi=150)
    plt.close()
    return outpath


def plot_source_distribution(df: pd.DataFrame, outdir: Path) -> Path:
    counts = df["source"].dropna().replace("", np.nan).dropna().value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(y=counts.index, x=counts.values, color="#ff7f0e")
    plt.title("Distribuição por fonte")
    plt.xlabel("Quantidade")
    plt.ylabel("Fonte")
    plt.tight_layout()
    outpath = outdir / "source_distribution.png"
    plt.savefig(outpath, dpi=150)
    plt.close()
    return outpath


def generate_title_wordcloud(df: pd.DataFrame, outdir: Path) -> Path:
    titles = df["title"].dropna().str.cat(sep=" ")
    if not titles.strip():
        titles = "no data"
    wc = WordCloud(width=1000, height=600, background_color="white").generate(titles)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    outpath = outdir / "title_wordcloud.png"
    plt.savefig(outpath, dpi=150)
    plt.close()
    return outpath


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Análise simples do CORD-19 metadata.csv")
    parser.add_argument("--input", type=str, required=True, help="Caminho para metadata.csv")
    parser.add_argument(
        "--outdir", type=str, default="outputs/figures", help="Diretório de saída para figuras"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("Carregando dados...")
    df = load_data(csv_path)
    basic_exploration(df)

    print("Limpando e preparando dados...")
    df_clean = clean_and_prepare(df)

    print("Gerando visualizações...")
    p1 = plot_publications_by_year(df_clean, outdir)
    print("Salvo:", p1)
    p2 = plot_top_journals(df_clean, outdir)
    print("Salvo:", p2)
    p3 = plot_source_distribution(df_clean, outdir)
    print("Salvo:", p3)
    p4 = generate_title_wordcloud(df_clean, outdir)
    print("Salvo:", p4)

    print("Concluído.")


if __name__ == "__main__":
    main()


