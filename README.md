# 🗄️ SQL Server Remote Access from macOS (VS Code)

Este guia prático documenta o processo de configuração para conectar o **Visual Studio Code no macOS Ventura** a uma instância do **SQL Server instalada em um laptop Windows** na mesma rede local.

<img width="1654" height="972" alt="image" src="https://github.com/user-attachments/assets/4eda3cfe-52a3-4ac6-921d-fb23f0f951f9" />

---

## 🛠️ 1. Configuração no Windows (Servidor)

### 1.1 SQL Server Configuration Manager
Para permitir que o SQL Server "escute" conexões de outros computadores, é necessário habilitar o protocolo TCP/IP.

1. No **SQL Server Configuration Manager**, habilite o protocolo **TCP/IP**.
2. Nas propriedades do TCP/IP, vá na aba **Endereços IP** e certifique-se de definir a porta **1433** na seção **IPAll**.
3. **Reinicie o serviço** do SQL Server para aplicar as mudanças.

### 1.2 Segurança e Login (SSMS)
O SQL Server precisa aceitar conexões via usuário e senha (Autenticação Mista).

1. No **SSMS**, habilite o **Modo de Autenticação do SQL Server e do Windows** nas propriedades do servidor.
2. Em **Segurança > Logins**, habilite o usuário `sa` e defina uma senha forte.

### 1.3 Firewall do Windows
Abra a porta 1433 no Firewall para permitir a entrada do tráfego vindo do Mac. Execute no PowerShell (Admin):
```powershell
New-NetFirewallRule -DisplayName "SQL Server Remote" -Direction Inbound -LocalPort 1433 -Protocol TCP -Action Allow
