import pyodbc
import os
import sys
from dotenv import load_dotenv
from tabulate import tabulate

# 1. Carrega as variáveis de ambiente
load_dotenv()

def read_sql_file(file_name):
    """Lê o conteúdo de um arquivo .sql na mesma pasta do script."""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo {file_name} não encontrado na pasta principal.")
        return None

def connect_and_execute():
    # Detecta se a saída vai para o terminal (isatty) para decidir se usa cores
    # Isso evita que códigos como [36m apareçam em arquivos redirecionados (>)
    use_colors = sys.stdout.isatty()

    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Só imprime no console se não estiver salvando em arquivo
        if use_colors:
            print(f"\n✅ Conectado com sucesso ao banco: {database}")

        file_name = 'get_comandos.sql'
        query = read_sql_file(file_name)

        if query:
            # --- INTERFACE DE EXECUÇÃO ---
            print("\n" + "="*60)
            print("🚀 INICIANDO CONSULTA SQL") # Sem 'f' para evitar Ruff(F541)
            print(f"📂 Arquivo: {file_name}")
            print("-" * 60)
            
            sql_clean = "\n".join([line for line in query.splitlines() if line.strip()])
            
            # Aplica cor apenas se for exibição direta no terminal
            if use_colors:
                print(f"\033[36m{sql_clean}\033[0m") 
            else:
                print(sql_clean)
                
            print("="*60 + "\n")
            
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            if rows:
                print("📊 RESULTADOS DA CONSULTA:")
                # fancy_grid mantém as molduras bonitas em arquivos TXT (UTF-8)
                print(tabulate(rows, headers=columns, tablefmt="fancy_grid"))
                print(f"\n✅ Total de registros: {len(rows)}")
            else:
                print("\n⚠️ Consulta executada, mas não retornou dados.")

        conn.close()

    except Exception as e:
        print(f"\n❌ Erro ao processar: {e}")

if __name__ == "__main__":
    connect_and_execute()