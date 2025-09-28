from typing import Optional, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as _canvas
from reportlab.lib import utils
from reportlab.lib import colors
import os

def ler_sql(caminho_arquivo: str):
    """
    Lê um arquivo .sql e retorna o conteúdo como string.
    
    :param caminho_arquivo: Caminho do arquivo .sql
    :return: Conteúdo do arquivo SQL em string
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    return conteudo

def query_postgres(user: str, password: str, host: str, port: int, database: str, query: str, params: Optional[Dict[str, Any]] = None, connect_args: Optional[Dict[str, Any]] = None):
    """
    Executa uma query no PostgreSQL e retorna um DataFrame.

    Parâmetros:
      - user, password, host, port, database: credenciais/endpoint do Postgres
      - query: string SQL completa (pode conter placeholders nomeados, ex: :id)
      - params: dicionário opcional com parâmetros para a query (evita SQL injection)
      - connect_args: args extras para a conexão (ex: {"sslmode": "require"})

    Retorno:
      - pandas.DataFrame com o resultado
    """
    # monta a URL de conexão
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    # argumentos extras (ex.: SSL) se necessário
    connect_args = connect_args or {}

    engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)

    # usa context manager para garantir fechamento adequado
    with engine.connect() as conn:
        # text() permite bind de parâmetros seguro
        df = pd.read_sql(text(query), conn, params=params)
    return df


def enviar_email(destinatarios, assunto, texto_html, copia=[], caminhos_anexo=[]):
    # Configurações do e-mail e do servidor SMTP
    # remetente = 'seu_email@gmail.com' # <- coloque seu e-mail
    # senha = 'senha' # <- coloque sua senha de app, crie uma com essa dica: https://www.youtube.com/watch?v=4Qgz2c7yR7s
    remetente = 'leonardoberangergomes@gmail.com'
    senha = 'mjys wyhy yodx qeax'
     
    try:
        # Criando a mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = ', '.join(destinatarios)
        msg['Cc'] = ', '.join(copia)
        msg['Subject'] = assunto

        # Corpo do e-mail em formato HTML
        msg.attach(MIMEText(texto_html, 'html'))

        # Anexando os arquivos, se fornecidos
        for caminho_anexo in caminhos_anexo:
            anexo = MIMEBase('application', 'octet-stream')
            with open(caminho_anexo, 'rb') as file:
                anexo.set_payload(file.read())
            encoders.encode_base64(anexo)
            anexo.add_header('Content-Disposition', f'attachment; filename={os.path.basename(caminho_anexo)}')
            msg.attach(anexo)

        # Configurando o servidor SMTP do Gmail
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatarios + copia, msg.as_string())
        servidor.quit()

        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar o e-mail: {e}")

def _img_w_h_keep_ratio(img_path, desired_h_cm=1.6):
    img = utils.ImageReader(img_path)
    iw, ih = img.getSize()
    h = desired_h_cm * cm
    w = iw * (h / ih)
    return w, h

def _header(canvas, doc, logo_path):
    """Desenha o cabeçalho com a imagem à esquerda em todas as páginas."""
    canvas.saveState()
    page_w, page_h = A4
    top_padding = 0.5 * cm
    # Tamanho da imagem (altura ~1.6cm, largura proporcional)
    try:
        w, h = _img_w_h_keep_ratio(logo_path, desired_h_cm=1.6)
        x = doc.leftMargin
        y = page_h - h - top_padding
        canvas.drawImage(logo_path, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')
    except Exception:
        # Se der erro na imagem, apenas ignora o logo para não quebrar o PDF
        pass
    canvas.restoreState()

def _make_image_flowable(path, max_w, max_h):
    """
    Cria um flowable Image ajustado a max_w x max_h mantendo proporção.
    Retorna None se o arquivo não existir ou falhar.
    """
    if not path or not os.path.isfile(path):
        return None
    try:
        img_reader = utils.ImageReader(path)
        iw, ih = img_reader.getSize()
        ratio = min(max_w / iw, max_h / ih)
        w = iw * ratio
        h = ih * ratio
        img = Image(path, width=w, height=h)
        return img
    except Exception:
        return None

def criar_pdf_relatorio(
    caminho_logo: str,
    saida_pdf: str,
    titulo_capa: str,
    periodo_ini: str,
    periodo_fim: str,
    total_booking: int,
    total_booking_sucesso: int,
    total_cancelado: int,
    taxa_cancelamento: str,
    rating_media: float,
    # --- novos parâmetros opcionais (caminhos dos gráficos) ---
    caminho_linha: str = None,
    caminho_barra: str = None,
    caminho_pizza: str = None,
    caminho_barra2: str = None,
):
    # Documento
    doc = SimpleDocTemplate(
        saida_pdf,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=3*cm,     # margem maior p/ não colidir com o header
        bottomMargin=2*cm
    )
    page_w, page_h = A4
    avail_w = page_w - doc.leftMargin - doc.rightMargin
    avail_h = page_h - doc.topMargin - doc.bottomMargin

    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        'TitleCenter24',
        parent=styles['Title'],
        fontSize=24,
        alignment=1,
        spaceAfter=1.2*cm
    )
    style_h2 = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        spaceAfter=0.4*cm
    )
    style_body = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        spaceAfter=0.2*cm
    )

    story = []

    # --- CAPA ---
    story.append(Spacer(1, 6*cm))
    story.append(Paragraph(titulo_capa, style_title))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(f"Período: {periodo_ini} a {periodo_fim}", style_body))

    story.append(PageBreak())

    # --- PÁGINA 2: Métricas ---
    story.append(Paragraph("Resumo das Métricas", style_h2))
    story.append(Paragraph(f"Total de bookings (distintos): <b>{total_booking}</b>", style_body))
    story.append(Paragraph(f"Bookings concluídos: <b>{total_booking_sucesso}</b>", style_body))
    story.append(Paragraph(f"Bookings cancelados: <b>{total_cancelado}</b>", style_body))
    story.append(Paragraph(f"Taxa de cancelamento: <b>{taxa_cancelamento}</b>", style_body))
    story.append(Paragraph(f"Rating médio do cliente: <b>{rating_media}</b>", style_body))

    # ---- PÁGINA 3: linha.png ----
    img_linha = _make_image_flowable(
        caminho_linha,
        max_w=avail_w,
        max_h=avail_h - 2*cm
    )
    if img_linha:
        story.append(PageBreak())
        story.append(Paragraph("Evolução das Corridas", style_h2))
        story.append(Spacer(1, 0.3*cm))
        story.append(img_linha)

    # ---- PÁGINA 4: barra.png e pizza.png lado a lado ----
    img_barra = _make_image_flowable(
        caminho_barra2,
        max_w=(avail_w/2) - 0.5*cm,
        max_h=avail_h - 3*cm
    )
    img_pizza = _make_image_flowable(
        caminho_pizza,
        max_w=(avail_w/2) - 0.5*cm,
        max_h=avail_h - 3*cm
    )
    if img_barra or img_pizza:
        story.append(PageBreak())
        story.append(Paragraph("Receita por Método de Pagamento e Motivos de Cancelamento", style_h2))
        story.append(Spacer(1, 0.3*cm))
        # Se faltar alguma imagem, a célula recebe Spacer
        from reportlab.platypus import Spacer as RLSpacer
        cell_left = img_barra if img_barra else RLSpacer(1, 1)
        cell_right = img_pizza if img_pizza else RLSpacer(1, 1)
        t = Table(
            [[cell_left, cell_right]],
            colWidths=[avail_w/2, avail_w/2]
        )
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            # sem bordas; se quiser guias, descomente:
            # ('BOX', (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        story.append(t)

    img_barra2 = _make_image_flowable(
        caminho_barra,
        max_w=avail_w,
        max_h=avail_h - 2*cm
    )
    if img_barra2:
        # story.append(PageBreak())
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("Tipo de Veículo e Rating Médio", style_h2))
        story.append(Spacer(1, 0.3*cm))
        story.append(img_barra2)

    # Build com header em todas as páginas (capa inclusive)
    doc.build(
        story,
        onFirstPage=lambda c, d: _header(c, d, caminho_logo),
        onLaterPages=lambda c, d: _header(c, d, caminho_logo)
    )