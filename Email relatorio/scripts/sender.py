import pandas as pd
import os
from datetime import date, timedelta
from bib import enviar_email

# Variáveis utilizadas
## Absolutas
CAM_BASE = os.path.abspath(__file__)
CAM_DIR = os.path.dirname(CAM_BASE)
CAM_IMG = os.path.join(os.path.dirname(CAM_DIR), "img")
CAM_PDF = os.path.join(os.path.dirname(CAM_DIR), "pdf", "relat_corridas.pdf")

# código correto caso os dados sejam alimentados corretamente
# hoje = date.today()

# vigente = hoje.replace(day=1)

# data_ini = (vigente - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')

# data_fim = vigente.strftime('%Y-%m-%d')

# Periodo relatório
data_ini = '2024-12-01'
data_fim = '2025-01-01'

# Destinatários
destinatarios = ["leonardoberangergomes@gmail.com"]            # coloque os e-mails desejados
copia = ["10732175@mackenzista.com","10731860@mackenzista.com","10732452@mackenzista.com"]
# copia = []

# Assunto
assunto = f"Relatório de Corridas - {pd.to_datetime(data_ini).strftime('%m/%Y')} - Uber"

# Corpo do e-mail (HTML)
texto_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; font-size: 14px;">
    <p>Olá,</p>
    <p>Segue em anexo o <b>Relatório de Corridas</b> referente ao período
    <b>{pd.to_datetime(data_ini).strftime('%m/%Y')}</b>.</p>

    <p>O relatório inclui análises detalhadas sobre o número total de corridas,
    taxa de cancelamento, avaliações médias dos clientes, entre outros insights.

    <p>Qualquer dúvida, fico à disposição.</p>
    <p>Abs,</p>
    <p>Time de Dados</p>
  </body>
</html>
"""

# Anexos (o PDF que você acabou de gerar)
caminhos_anexo = [CAM_PDF]

# Chamada
enviar_email(
    destinatarios=destinatarios,
    assunto=assunto,
    texto_html=texto_html,
    copia=copia,
    caminhos_anexo=caminhos_anexo
)