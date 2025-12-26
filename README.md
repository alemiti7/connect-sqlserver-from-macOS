# 🗄️ SQL Server Remote Access (macOS/VS Code)

Guia de configuração para acesso remoto entre instâncias **SQL Server (Windows)** e o **VS Code (macOS)**, incluindo automação de consultas via Python.

## 📌 Sumário

* [Funcionalidades](#funcionalidades)
* [Arquitetura](#arquitetura)
* [Instalação](#instalação)
* [Contribuição](#contribuição)

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
