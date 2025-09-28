import pandas as pd
import os
from datetime import date, timedelta
from bib import ler_sql, query_postgres
from bib_graf import salvar_grafico_pizza,salvar_grafico_barras, salvar_grafico_linhas

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

# Criando gráficos do report

volume_booking = (
    df_relat[
        ~df_relat["Booking Status"].isin(["Cancelled by Driver", "Cancelled by Customer"])
    ]
    .groupby("Date")
    .size()
    .reset_index(name="counts")
)

print('Gerando info...\n')

cancel_reason = df_relat.groupby("Reason for cancelling by Customer").size().reset_index(name='counts')

payment_method = df_relat.groupby("Payment Method")['Booking Value'].sum().reset_index()

vehicle_type = df_relat.groupby("Vehicle Type")['Customer Rating'].mean().reset_index()

theme = CAM_SAVE_IMG+r'\Tema.json'

print('Criando gráficos...\n')

salvar_grafico_barras(df=payment_method, save_path=CAM_SAVE_IMG+r'\barra.png', title="Revenue by Payment Method",theme=theme)

salvar_grafico_pizza(df=cancel_reason, save_path=CAM_SAVE_IMG+r'\pizza.png', title="Cancellation Reasons",theme=theme)

salvar_grafico_linhas(df=volume_booking, save_path=CAM_SAVE_IMG+r'\linha.png', title="Booking Volume Over Time",theme=theme)

salvar_grafico_barras(df=vehicle_type, save_path=CAM_SAVE_IMG+r'\barra_2.png', title="Vehicle Type and Customer Rating",theme=theme)

print('Gráficos criados\n')