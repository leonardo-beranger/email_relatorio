import matplotlib.pyplot as plt
import json
import pandas as pd
from typing import List, Optional, Union

def carregar_cores(theme_path: Union[str, None]) -> Optional[List[str]]:
    """
    Lê um JSON de tema e retorna uma lista de cores.
    Aceita tanto um JSON que seja uma lista direta de cores quanto um objeto
    com a chave 'dataColors'. Lida com arquivos salvos com UTF-8 BOM.
    """
    if not theme_path:
        return None
    try:
        # 'utf-8-sig' remove o BOM se existir
        with open(theme_path, "r", encoding="utf-8-sig") as f:
            tema = json.load(f)

        if isinstance(tema, list):
            return tema
        if isinstance(tema, dict) and isinstance(tema.get("dataColors"), list):
            return tema["dataColors"]

        raise ValueError("O tema deve ser uma lista de cores ou um objeto com a chave 'dataColors'.")
    except Exception as e:
        print(f"Erro ao carregar o tema: {e}. Usando cores padrão.")
        return None

def salvar_grafico_pizza(df: pd.DataFrame, save_path: str, title='Gráfico de Pizza', theme=None):
    if df.shape[1] < 2:
        raise ValueError("O DataFrame deve conter pelo menos duas colunas: [label, valor].")

    labels = df.iloc[:, 0]
    valores = df.iloc[:, 1]

    cores = carregar_cores(theme) if theme is not None else None

    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=labels, autopct="%1.1f%%", colors=cores)
    plt.title(title)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def salvar_grafico_barras(df: pd.DataFrame, save_path: str, title='Gráfico de Barras', theme=None, horizontal=False):
    if df.shape[1] < 2:
        raise ValueError("O DataFrame deve conter pelo menos duas colunas: [label, valor].")

    df = df.sort_values(by=df.columns[1], ascending=False)
    labels = df.iloc[:, 0]
    valores = df.iloc[:, 1]

    cores = carregar_cores(theme) if theme is not None else None

    plt.figure(figsize=(8, 6))
    if horizontal:
        bars = plt.barh(labels, valores, color=cores)
        plt.xlabel("Valor")
        plt.ylabel("")
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                     f'{bar.get_width():,.2f}', va='center', ha='left')
    else:
        bars = plt.bar(labels, valores, color=cores)
        plt.ylabel("")
        plt.xlabel("Categoria")
        plt.gca().axes.get_yaxis().set_visible(False)
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                     f'{bar.get_height():,.2f}', ha='center', va='bottom')

    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def salvar_grafico_linhas(df: pd.DataFrame, save_path: str, title='Gráfico de Linhas', theme=None):
    if df.shape[1] < 2:
        raise ValueError("O DataFrame deve conter pelo menos duas colunas: [x, y].")

    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    # Define uma única cor (ou None -> usa padrão do Matplotlib)
    cor = None
    if theme is not None:
        cores = carregar_cores(theme)
        if cores:
            cor = cores[0]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', color=cor)
    plt.title(title)
    plt.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
