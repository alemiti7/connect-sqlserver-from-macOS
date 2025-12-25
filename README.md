# 🗄️ SQL Server Remote Access from macOS (VS Code)
-- Configuração de Acesso Remoto: SQL Server no Windows para VS Code no macOS

Este guia fornece um passo a passo detalhado sobre como configurar o **Microsoft SQL Server** (instalado em um laptop Windows) para aceitar conexões remotas vindas do **Visual Studio Code** em um ambiente **macOS (Ventura ou superior)**.

## 📋 Pré-requisitos

* Laptop com **Windows** e **SQL Server** instalado (Versão 2025/17.x ou anterior).
* Laptop com **macOS** e **Visual Studio Code** instalado.
* Ambos os dispositivos devem estar na **mesma rede local**.

<img width="1909" height="1067" alt="image" src="https://github.com/user-attachments/assets/1314c50b-a8b7-41b9-bd0d-938cb5d962bb" />


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

**Instalação:**

```bash
pip install pyodbc

```

**Script de Exemplo (`export_data.py`):**

```python
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.0.21;" # IP do seu laptop Windows
    "DATABASE=Curso;"      # Seu banco de dados
    "UID=sa;"
    "PWD=SuaSenhaAqui;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # No SQL Server, usamos TOP em vez de LIMIT
    cursor.execute("SELECT TOP 5 * FROM sys.tables")
    for row in cursor:
        print(row)
    conn.close()
except Exception as e:
    print(f"Erro: {e}")

```

---

## 🚀 Dicas de Expansão

1. **Scripts de Firewall:** Adicione um arquivo `.ps1` no repositório para automatizar a abertura de portas no Windows.
2. **Cheat Sheet SQL:** Inclua uma lista de diferenças entre T-SQL e outros bancos (ex: `TOP` vs `LIMIT`).
3. **Backup Automatizado:** Documente scripts Python para gerar backups diários do banco para o macOS.
4. **Monitoramento:** Crie um alerta que verifica se o serviço do SQL Server está ativo no servidor remoto.

---




