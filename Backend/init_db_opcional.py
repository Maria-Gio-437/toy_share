import sqlite3
import os

DATABASE_URL = 'database.sqlite'
SCHEMA_URL = 'app/db/schema.sql' 

print("Iniciando a criação do banco de dados...")

# Apaga o banco de dados antigo, se existir
if os.path.exists(DATABASE_URL):
    os.remove(DATABASE_URL)
    print(f"Banco de dados antigo '{DATABASE_URL}' removido.")

try:
    # Conecta ao banco de dados (isso criará o arquivo)
    connection = sqlite3.connect(DATABASE_URL)

    # Abre e lê o arquivo de schema
    with open(SCHEMA_URL) as f:
        connection.executescript(f.read())

    print("Banco de dados criado e tabelas inicializadas com sucesso!")
    print(f"Arquivo '{DATABASE_URL}' criado na pasta atual.")

except FileNotFoundError:
    print(f"Erro: Arquivo de schema não encontrado em '{SCHEMA_URL}'. Verifique o caminho.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    # Fecha a conexão
    if 'connection' in locals() and connection:
        connection.close()