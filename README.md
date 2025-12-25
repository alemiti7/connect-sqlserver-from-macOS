# 🗄️ SQL Server Remote Access from macOS (VS Code)
-- Configuração de acesso remoto via VS Code no macOS para instâncias SQL Server em Windows.

Este guia fornece um passo a passo detalhado sobre como configurar o **Microsoft SQL Server** (instalado em um laptop Windows) para aceitar conexões remotas vindas do **Visual Studio Code** em um ambiente **macOS (Ventura ou superior)**.

## 📋 Pré-requisitos

* Laptop com **Windows** e **SQL Server** instalado (Versão 2025/17.x ou anterior).
* Laptop com **macOS** e **Visual Studio Code** instalado.
* Ambos os dispositivos devem estar na **mesma rede local**.

<img width="1906" height="1074" alt="image" src="https://github.com/user-attachments/assets/49a78675-9605-417a-b22c-8653ba89ffd6" />



---

## 🛠️ Passo 1: Configuração do Servidor (No Windows)

### 1.1 SQL Server Configuration Manager
Para permitir que o SQL Server "escute" conexões de outros computadores, é necessário habilitar o protocolo TCP/IP.

1. No **SQL Server Configuration Manager**, habilite o protocolo **TCP/IP**.

<img width="1273" height="684" alt="image" src="https://github.com/user-attachments/assets/00f2e15b-3099-469c-9f4b-cf7bdd678286" />




2. Nas propriedades do TCP/IP, vá na aba **Endereços IP** e certifique-se de definir a porta **1433** na seção **IPAll**.

<img width="1277" height="687" alt="image" src="https://github.com/user-attachments/assets/8fedf057-e06a-42fe-b98c-51b1d38a79a4" />




3. **Reinicie o serviço** do SQL Server para aplicar as mudanças.

<img width="1186" height="630" alt="image" src="https://github.com/user-attachments/assets/334c7288-5dd4-4c72-9f9e-80401d75a7b6" />

---

### 1.2 Habilitar Autenticação Mista e Usuário `sa`

O VS Code conecta-se mais facilmente via Login SQL.

1. Abra o **SQL Server Management Studio (SSMS)**.
2. Clique com o botão direito no servidor > **Propriedades** > **Segurança** e selecione **Modo de Autenticação do SQL Server e do Windows**.
3. Em **Segurança** > **Logins**, clique com o botão direito no usuário `sa`, defina uma nova senha e, em **Status**, marque como **Habilitado**.

### 1.3 Reiniciar os Serviços

Para que as alterações tenham efeito, reinicie o serviço do SQL Server através do Configuration Manager.

---

## 🛡️ Passo 2: Configuração do Firewall (No Windows)

O Firewall do Windows bloqueará a conexão na porta 1433 a menos que criemos uma regra.

1. Abra o **PowerShell** como Administrador.
2. Execute o comando:
```powershell
New-NetFirewallRule -DisplayName "SQL Server VSCode" -Direction Inbound -LocalPort 1433 -Protocol TCP -Action Allow

```



---

## 💻 Passo 3: Configuração no Cliente (No macOS)

### 3.1 Instalar a Extensão

1. No VS Code, abra a aba de extensões (`Cmd+Shift+X`).
2. Pesquise por **SQL Server (mssql)** da Microsoft e clique em **Install**.
3. Aguarde a extração dos arquivos de serviço.

### 3.2 Criar a Conexão

1. Clique no ícone do **SQL Server** na barra lateral esquerda.
2. Clique no ícone de **+** em **Connections**.
3. Preencha os parâmetros na central de comandos ou no formulário:
* **Server Name:** O endereço IP do seu laptop Windows (ex: `192.168.0.21`).
* **Authentication Type:** `SQL Login`.
* **User Name:** `sa`.
* **Password:** A senha definida anteriormente.
* **Trust Server Certificate:** `True` (Essencial para conexões locais sem SSL oficial).



---

## 🚀 Resultado Final

Se a configuração estiver correta, você verá seu servidor e seus bancos de dados (como o banco `Curso`) listados na barra lateral do macOS.

Para testar, abra uma **New Query** e execute:

```sql
-- No SQL Server, usamos TOP em vez de LIMIT
SELECT TOP 5 * FROM sys.tables;

```
<img width="1573" height="972" alt="image" src="https://github.com/user-attachments/assets/90b836bd-fc83-4c89-951c-344d952f25ac" />



Pressione `Cmd + Shift + E` para ver os resultados na grade lateral.

---

## 💡 Vantagens do VS Code vs SSMS

* **Ambiente Único:** Desenvolva código e gerencie o banco no mesmo editor.
* **Performance:** Interface muito mais rápida e leve que o SSMS no Windows.
* **Exportação:** Exporte resultados para JSON, CSV ou Excel com um clique.

---

## 🐍 Automação com Python

Com o acesso liberado, você pode automatizar tarefas usando Python no seu Mac.

## 🚀 Exemplos prático: 

main_get.py
get_comando.sql

### 📋 O que o script faz:

* **Autenticação Segura:** Utiliza a biblioteca `python-dotenv` para carregar credenciais sensíveis de um arquivo externo, evitando a exposição de senhas no código-fonte.
* **Gestão de Consultas SQL:** Lê comandos SQL diretamente de arquivos `.sql` externos (como o `get_comandos.sql`), facilitando a manutenção de queries complexas.
* **Conexão Robusta:** Utiliza o driver `ODBC 18` para estabelecer uma conexão segura (SSL/TLS) com o banco de dados.
* **Interface no Terminal:** Formata os resultados da consulta em tabelas visuais organizadas (`fancy_grid`) e detecta automaticamente se a saída está sendo exibida no terminal ou redirecionada para um arquivo, ajustando o uso de cores (ANSI) conforme necessário.

---

### 🔐 Configuração do Ambiente (.env)

Para que o script funcione, é **obrigatório** criar um arquivo chamado `.env` na raiz do projeto. 

Configure as seguintes variáveis dentro dele:

```env
DB_SERVER=IP_DO_SQL_SERVER
DB_NAME=NOME_DO_BANCO_A_SER_CONECTADO
DB_USER=sa
DB_PASS=SENHA_DO_USUARIO_sa

```

### 🛠️ Tecnologias Utilizadas:

* **Python 3**
* **pyodbc**: Para conexão com o banco.
* **tabulate**: Para formatação visual dos dados.
* **python-dotenv**: Para gestão de variáveis de ambiente.

---

**Instalação:**

```bash
pip install pyodbc

```

**Script (`main_get.py`):**

```python
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

```
**Script (`get_comandos.sql`):**
---

```sql

SELECT top 5 * FROM dbo.PRODUTOS

```

<img width="1105" height="414" alt="image" src="https://github.com/user-attachments/assets/43f2e5e3-ab23-499c-8486-2b0737e1cc73" />


---

### 🚀 Como Executar

Após configurar o arquivo `.env` e instalar as dependências, basta executar o script principal através do terminal do VS Code:

```bash
python main_get.py

```

* **Execução**: O comando acima inicia o script `main_get.py`, que carrega as configurações e realiza a consulta.
* **Fluxo**: O script lerá as instruções contidas no arquivo `get_comandos.sql` e exibirá os resultados diretamente no seu console.

<img width="1100" height="397" alt="image" src="https://github.com/user-attachments/assets/79e2b91e-4924-41ee-afdd-d18427a659a4" />

---




## 🤝 Formas de contribuir:

- Sugerir melhorias e reportar bugs

📞 Contato:

Alexandre
📧 alemiti@gmail.com
[@alemiti7]([https://github.com/alemiti7]) 😊

---




