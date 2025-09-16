import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")
st.title("CORD-19 Data Explorer")
st.write("Exploração simples de artigos de pesquisa sobre COVID-19 (arquivo metadata.csv)")


@st.cache_data(show_spinner=False)
def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False)
    # Preparação leve (sincronizada com o script)
    if "source_x" in df.columns and "source" not in df.columns:
        df = df.rename(columns={"source_x": "source"})
    for col in ["publish_time", "title", "abstract", "journal", "source"]:
        if col not in df.columns:
            df[col] = np.nan
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year
    return df


data_path = st.sidebar.text_input("Caminho do metadata.csv", value="data/metadata.csv")

try:
    df = load_data(data_path)
    st.success(f"Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
except Exception as e:
    st.error(f"Falha ao carregar dados: {e}")
    st.stop()

# Filtros
years = sorted([int(y) for y in df["year"].dropna().unique()])
if years:
    min_year, max_year = min(years), max(years)
else:
    min_year, max_year = 2019, 2022

year_range = st.sidebar.slider("Selecione o intervalo de anos", min_year, max_year, (min_year, max_year))
journal_input = st.sidebar.text_input("Filtrar por periódico (contém)", value="")
source_options = ["(todos)"] + sorted([s for s in df["source"].dropna().unique()])
source_sel = st.sidebar.selectbox("Filtrar por fonte", source_options)

mask = (df["year"].between(year_range[0], year_range[1], inclusive="both"))
if journal_input:
    mask &= df["journal"].astype("string").str.contains(journal_input, case=False, na=False)
if source_sel != "(todos)":
    mask &= df["source"].astype("string") == source_sel

df_filt = df.loc[mask].copy()

st.subheader("Amostra de dados filtrados")
st.dataframe(df_filt.head(50))

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Publicações por ano**")
    counts = df_filt["year"].dropna().value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.barplot(x=counts.index.astype(int), y=counts.values, ax=ax, color="#1f77b4")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Quantidade")
    ax.set_title("")
    st.pyplot(fig)

with col2:
    st.markdown("**Top periódicos**")
    top_n = st.slider("Top N", 5, 20, 10, key="top_journals")
    jcounts = (
        df_filt["journal"].dropna().replace("", np.nan).dropna().value_counts().head(top_n)
    )
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(y=jcounts.index, x=jcounts.values, ax=ax2, color="#2ca02c")
    ax2.set_xlabel("Quantidade")
    ax2.set_ylabel("Periódico")
    st.pyplot(fig2)

st.subheader("Distribuição por fonte")
scounts = df_filt["source"].dropna().replace("", np.nan).dropna().value_counts()
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(y=scounts.index, x=scounts.values, ax=ax3, color="#ff7f0e")
ax3.set_xlabel("Quantidade")
ax3.set_ylabel("Fonte")
st.pyplot(fig3)

st.info("Dica: ajuste filtros na barra lateral para explorar os dados.")


