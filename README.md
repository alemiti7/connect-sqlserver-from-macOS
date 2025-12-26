# 🗄️ SQL Server Remote Access (macOS/VS Code)

Guia de configuração para acesso remoto entre instâncias **SQL Server (Windows)** e o **VS Code (macOS)**, incluindo automação de consultas via Python.

## 📌 Sumário

* [Funcionalidades](#funcionalidades)
* [Arquitetura](https://www.google.com/search?q=%23-arquitetura)
* [Instalação](https://www.google.com/search?q=%23-instala%C3%A7%C3%A3o)
* [Contribuição](https://www.google.com/search?q=%23-contribui%C3%A7%C3%A3o)
* [Licença](https://www.google.com/search?q=%23-licen%C3%A7a)

---

## 🚀 Funcionalidades

* **Conexão Cross-Platform:** Acesso estável ao SQL Server via macOS.
* **Automação SQL:** Execução de scripts `.sql` externos via Python.
* **Segurança:** Gestão de credenciais via variáveis de ambiente (`.env`).
* **Visualização:** Formatação de resultados em tabelas no terminal.

## 🏗️ Arquitetura

A solução estabelece um túnel de comunicação via **TCP/IP** na porta **1433**.

* **Servidor (Host):** Windows + SQL Server (Auth Mista).
* **Cliente:** macOS + VS Code (Extensão mssql) + Python 3 (Driver ODBC 18).

## 🛠️ Instalação

### 1. Configuração do Servidor (Windows)

1. **TCP/IP:** No *SQL Server Configuration Manager*, habilite o protocolo TCP/IP e defina a porta `1433` em `IPAll`. Reinicie o serviço.
2. **Auth:** No *SSMS*, mude a autenticação para "Modo Misto". Habilite o usuário `sa` e defina uma senha.
3. **Firewall:** Execute no PowerShell (Admin):
```powershell
New-NetFirewallRule -DisplayName "SQL Server" -Direction Inbound -LocalPort 1433 -Protocol TCP -Action Allow

```



### 2. Configuração do Cliente (macOS)

1. **VS Code:** Instale a extensão **SQL Server (mssql)**.
2. **Dependências Python:**
```bash
pip install pyodbc python-dotenv tabulate

```


3. **Variáveis de Ambiente:** Crie um arquivo `.env` na raiz:
```env
DB_SERVER=SEU_IP_AQUI
DB_NAME=NOME_DO_BANCO
DB_USER=sa
DB_PASS=SUA_SENHA

```



### 3. Execução

Execute o script principal para rodar as queries contidas em `get_comandos.sql`:

```bash
python main_get.py

```

## 🤝 Contribuição

1. Realize um **Fork** do projeto.
2. Crie uma **Branch** para sua modificação (`git checkout -b feature/nova-feature`).
3. Abra um **Pull Request**.

Para bugs e sugestões: [alemiti@gmail.com](mailto:alemiti@gmail.com).
