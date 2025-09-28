import pandas as pd
import os
from datetime import date, timedelta
from bib import ler_sql, query_postgres, criar_pdf_relatorio

# Variáveis utilizadas
## Absolutas
CAM_BASE = os.path.abspath(__file__)
CAM_DIR = os.path.dirname(CAM_BASE)
CAM_SQL = os.path.join(CAM_DIR, "sql", "uber_data.sql")
CAM_SAVE_IMG = os.path.join(os.path.dirname(CAM_DIR), "img")

# credenciais
user = 'postgres'
password = os.getenv('password_post')
host = 'localhost'
port = 5432
database = 'mba_proj'
tabela = 'uber_database'

# código correto caso os dados sejam alimentados corretamente
# hoje = date.today()

# vigente = hoje.replace(day=1)

# data_ini = (vigente - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')

# data_fim = vigente.strftime('%Y-%m-%d')

# Periodo relatório
data_ini = '2024-12-01'
data_fim = '2025-01-01'

print('Iniciando processo de coleta...\n')

# Query que será utilizada
query = ler_sql(CAM_SQL)

print('Importando base de dados...\n')

df = query_postgres(user=user, password=password, host=host, port=5432, database=database, query=query)

print('Tratamento simples...\n')

df = df.astype({
    "Date": "datetime64[ns]"
})

df_relat = df[df['Date'].between(data_ini, data_fim)]

# Criando valores para análise do pdf
# total_booking = df_relat['Booking ID'].count()

# total_booking_sucesso = round(df_relat[df_relat["Booking Status"] == "Completed"]['Booking ID'].count(), 2)

# total_cancelado = round(df_relat[(df_relat["Booking Status"] == "Cancelled by Customer") & (df_relat["Booking Status"] == "Cancelled by Driver")]['Booking ID'].count(),0)

# taxa_cancelamento = str(round((total_cancelado / total_booking) * 100,2)) + '%'

# rating_media = round(df_relat['Customer Rating'].mean(),2)

# Totais
total_booking = df_relat['Booking ID'].nunique()

total_booking_sucesso = df_relat.loc[df_relat["Booking Status"] == "Completed", 'Booking ID'].nunique()

# Cancelados: cliente OU motorista
total_cancelado = df_relat.loc[
    df_relat["Booking Status"].isin(["Cancelled by Customer", "Cancelled by Driver"]),
    'Booking ID'
].nunique()

taxa_cancelamento = f"{round((total_cancelado / total_booking) * 100, 2)}%" if total_booking else "0%"

rating_media = round(df_relat['Customer Rating'].mean(), 2)

# Caminho do logo (coloque o seu)
CAMINHO_LOGO = os.path.join(CAM_SAVE_IMG, "Uber-Logo.png")  # ajuste para o seu arquivo

# Pasta de saída
CAM_SAVE_PDF = os.path.join(os.path.dirname(CAM_DIR), "pdf")

os.makedirs(CAM_SAVE_PDF, exist_ok=True)

CAM_REL_PDF = os.path.join(CAM_SAVE_PDF, "relat_corridas.pdf")

criar_pdf_relatorio(
    caminho_logo=CAMINHO_LOGO,
    saida_pdf=CAM_REL_PDF,
    titulo_capa="Relatório de Corridas",
    periodo_ini=pd.to_datetime(data_ini).strftime('%m/%Y'),
    periodo_fim=pd.to_datetime(data_fim).strftime('%m/%Y'),
    total_booking=total_booking,
    total_booking_sucesso=total_booking_sucesso,
    total_cancelado=total_cancelado,
    taxa_cancelamento=taxa_cancelamento,
    rating_media=rating_media,
    caminho_linha=os.path.join(CAM_SAVE_IMG, "linha.png"),
    caminho_barra=os.path.join(CAM_SAVE_IMG, "barra.png"),
    caminho_pizza=os.path.join(CAM_SAVE_IMG, "pizza.png"),
    caminho_barra2=os.path.join(CAM_SAVE_IMG, "barra_2.png"),
)

print(f"PDF gerado em: {CAM_REL_PDF}")
