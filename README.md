# 🗄️ SQL Server Remote Access — macOS + VS Code

![SQL Server](https://img.shields.io/badge/SQL_Server-2019+-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-11+-000000?style=flat&logo=apple&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-10+-0078D4?style=flat&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-mssql-007ACC?style=flat&logo=visualstudiocode&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-config-ECD53F?style=flat&logo=dotenv&logoColor=black)
![ODBC](https://img.shields.io/badge/ODBC-Driver_18-0078D4?style=flat&logo=microsoft&logoColor=white)

> Guia de configuração para acesso remoto entre instâncias **SQL Server (Windows)** e **VS Code (macOS)**, incluindo automação de consultas via Python.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Contribuição](#contribuição)

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---|---|
| **Conexão Cross-Platform** | Acesso estável ao SQL Server a partir do macOS via TCP/IP |
| **Automação SQL** | Execução de scripts `.sql` externos via Python |
| **Segurança** | Gestão de credenciais via variáveis de ambiente (`.env`) |
| **Visualização** | Resultados formatados em tabelas no terminal |

---

## 🏗️ Arquitetura

A solução estabelece um túnel de comunicação via **TCP/IP** na porta **1433**:

```
macOS (VS Code + Python)  ──(TCP 1433)──▶  Windows (SQL Server)
       │                                          │
  ODBC Driver 18                         Auth Mista (sa)
  pyodbc + python-dotenv                 Firewall liberado
```

| Componente | Detalhe |
|---|---|
| **Servidor (Host)** | Windows + SQL Server com autenticação mista |
| **Cliente** | macOS + VS Code (extensão mssql) + Python 3 (ODBC Driver 18) |
| **Porta** | TCP/IP `1433` |

---

## 🛠️ Instalação

### 1. Configuração do Servidor (Windows)

**a) Habilitar TCP/IP**

No *SQL Server Configuration Manager*, habilite o protocolo TCP/IP e defina a porta `1433` em `IPAll`. Reinicie o serviço SQL Server após a alteração.

**b) Autenticação Mista**

No *SSMS*, altere para "Modo Misto", habilite o usuário `sa` e defina uma senha forte.

**c) Regra de Firewall**

Execute no PowerShell como Administrador:

```powershell
New-NetFirewallRule -DisplayName "SQL Server" -Direction Inbound -LocalPort 1433 -Protocol TCP -Action Allow
```

---

### 2. Configuração do Cliente (macOS)

**a) Extensão VS Code**

Instale a extensão **SQL Server (mssql)** no VS Code.

**b) Dependências Python**

```bash
pip install pyodbc python-dotenv tabulate
```

**c) Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
DB_SERVER=SEU_IP_AQUI
DB_NAME=NOME_DO_BANCO
DB_USER=sa
DB_PASS=SUA_SENHA
```

> ⚠️ **Atenção:** Nunca versione o arquivo `.env`. Adicione-o ao `.gitignore` para proteger suas credenciais.

---

### 3. Execução

Execute o script principal para rodar as queries contidas em `get_comandos.sql`:

```bash
python main_get.py
```

---

## 🤝 Contribuição

1. Realize um **Fork** do projeto
2. Crie uma **Branch** para sua modificação:
   ```bash
   git checkout -b feature/nova-feature
   ```
3. Faça o **commit** das suas alterações:
   ```bash
   git commit -m "feat: descrição da melhoria"
   ```
4. Abra um **Pull Request**

Para bugs e sugestões: [alemiti@gmail.com](mailto:alemiti@gmail.com)
