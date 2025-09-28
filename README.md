# Email Relatório

Automação em Python que extrai dados de um banco PostgreSQL, gera gráficos e um relatório em PDF e, por fim, envia o documento por e-mail. O processo completo é orquestrado pelo arquivo `main.py`, que executa em sequência as etapas de criação dos gráficos, compilação do PDF e envio.

## Visão geral do fluxo
1. **Coleta de dados**: leitura de uma consulta SQL (em `Email relatorio/scripts/sql/uber_data.sql`) e extração dos dados do PostgreSQL.
2. **Tratamento**: filtragem do período desejado e cálculo dos indicadores.
3. **Visualizações**: geração de gráficos em `Email relatorio/img/` para ilustrar volume de corridas, motivos de cancelamento, receita por meio de pagamento e avaliação média por tipo de veículo.
4. **Relatório PDF**: montagem do arquivo `Email relatorio/pdf/relat_corridas.pdf` com capa, indicadores e gráficos.
5. **Envio de e-mail**: disparo do PDF gerado para a lista de destinatários configurada.

## Estrutura do projeto
```
Email relatorio/
├── base_de_dados/        # CSV com dados de exemplo para povoar o banco
├── img/                  # Diretório de saída dos gráficos (também armazena o logo)
├── pdf/                  # Diretório de saída do relatório em PDF
├── main.py               # Ponto de entrada que orquestra toda a automação
└── scripts/
    ├── bib.py            # Funções utilitárias (consulta ao banco, criação do PDF, envio de e-mails)
    ├── bib_graf.py       # Auxiliares para geração de gráficos
    ├── graf.py           # Cria os gráficos a partir dos dados do banco
    ├── pdf.py            # Compila os indicadores e monta o PDF
    ├── sender.py         # Dispara o relatório por e-mail
    └── sql/uber_data.sql # Consulta SQL utilizada no relatório
```

## Pré-requisitos
- Python 3.10 ou superior.
- Servidor PostgreSQL acessível contendo a base `mba_proj` e a tabela `uber_database`.
- Credenciais válidas de e-mail com acesso SMTP (o projeto está configurado para Gmail com senha de app).

As bibliotecas Python utilizadas podem ser instaladas com:
```bash
pip install pandas sqlalchemy psycopg2-binary reportlab matplotlib
```

## Configuração
1. Clone o repositório e acesse a pasta principal:
   ```bash
   git clone <url-do-repositorio>
   cd email_relatorio/Email\ relatorio
   ```
2. Configure a variável de ambiente com a senha do usuário PostgreSQL:
   ```bash
   export password_post="sua_senha"
   # No Windows PowerShell: $Env:password_post = "sua_senha"
   ```
3. Ajuste, se necessário, as credenciais de e-mail definidas em `scripts/bib.py` (`remetente` e `senha`). Para produção recomenda-se carregar esses valores também por variáveis de ambiente.
4. Caso precise alterar o período analisado, atualize as variáveis `data_ini` e `data_fim` em `scripts/graf.py`, `scripts/pdf.py` e `scripts/sender.py`. Há comentários no código indicando como automatizar a seleção do mês anterior.
5. Garanta que o arquivo `Email relatorio/img/Uber-Logo.png` exista ou ajuste o caminho do logo em `scripts/pdf.py`.

### Populando o banco
O diretório `base_de_dados/` contém o CSV `ncr_ride_bookings.csv`, que pode ser utilizado para popular a tabela `uber_database`. Um exemplo simplificado de importação via `psql` seria:
```sql
\copy uber_database FROM 'Email relatorio/base_de_dados/ncr_ride_bookings.csv' DELIMITER ',' CSV HEADER;
```
Adapte os caminhos conforme o ambiente em que o comando for executado.

## Executando a automação
Com o ambiente configurado, execute o pipeline completo a partir da pasta `Email relatorio`:
```bash
python main.py
```
Cada etapa imprime mensagens no terminal indicando o progresso. Os resultados esperados são:
- Gráficos atualizados em `Email relatorio/img/`.
- Relatório final em PDF em `Email relatorio/pdf/relat_corridas.pdf`.
- E-mail enviado aos destinatários informados (caso as credenciais estejam válidas e haja conexão com o servidor SMTP).

Se desejar rodar etapas isoladas, basta executar os scripts dentro de `Email relatorio/scripts/` individualmente (por exemplo, `python graf.py`).

## Boas práticas e segurança
- Não versionar credenciais reais. Utilize variáveis de ambiente ou um gerenciador de segredos.
- Considere habilitar logs de execução para acompanhar sucessos e falhas das automações, conforme sugerido nos comentários do `main.py`.
- Antes de executar em produção, revise limites de envio do provedor de e-mail e políticas de acesso ao banco.

## Licença
Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
