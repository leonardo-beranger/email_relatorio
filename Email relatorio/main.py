import subprocess
from pathlib import Path
import time
import os
import sys

# Caminho do arquivo atual e pastas
CAM_BASE = Path(__file__).resolve()
CAM_DIR = CAM_BASE.parent

CAM_SCRIPTS = (CAM_DIR / "scripts").resolve()

SCRIPTS = ["graf.py", "pdf.py", "sender.py"]

print(f"Pasta dos scripts: {CAM_SCRIPTS}")
if not CAM_SCRIPTS.is_dir():
    print("ERRO: pasta 'scripts' não existe nesse caminho.")
    raise SystemExit(1)

for name in SCRIPTS:
    caminho = CAM_SCRIPTS / name
    print(f"Executando {caminho}...")

    if not caminho.is_file():
        print(f"Arquivo NÃO encontrado: {caminho}")
        print("Arquivos .py disponíveis em 'scripts':")
        for p in sorted(CAM_SCRIPTS.glob("*.py")):
            print(" -", p.name)
        continue

    try:
        # Use o caminho COMPLETO do script; defina cwd para evitar problemas de import relativo
        subprocess.run([sys.executable, str(caminho)], cwd=str(CAM_SCRIPTS), check=True)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {name}: {e}")

    print('\n')

    time.sleep(1)  # Pequena pausa entre os scripts, se necessário


# Possíveis melhorias de projeto:

## Para melhoria do projeto seria interessnate um Log de execução das automações e o registro desse log para controle de falhas e mapeamento do processo e melhorias futuras.

## Carregar dados tratados de do banco de dados para o os códigos através de uma função evitando repetição de códigos, aumentando eficiência e diminuindo erros.