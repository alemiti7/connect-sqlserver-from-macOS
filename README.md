# 🗄️ SQL Server Remote Access from macOS (VS Code)
-- Configuração de Acesso Remoto: SQL Server no Windows para VS Code no macOS --

Este guia fornece um passo a passo detalhado sobre como configurar o Microsoft SQL Server (instalado em um laptop Windows) para aceitar conexões remotas vindas do Visual Studio Code em um ambiente macOS (Ventura ou superior).

📋 Pré-requisitos
Laptop com Windows e SQL Server instalado (Versão 2025/17.x ou anterior).

Laptop com macOS e Visual Studio Code instalado.

Ambos os dispositivos devem estar na mesma rede local.

<img width="1909" height="1067" alt="image" src="https://github.com/user-attachments/assets/1314c50b-a8b7-41b9-bd0d-938cb5d962bb" />


---

## 🛠️ 1. Configuração no Windows (Servidor)

### 1.1 SQL Server Configuration Manager
Para permitir que o SQL Server "escute" conexões de outros computadores, é necessário habilitar o protocolo TCP/IP.

1. No **SQL Server Configuration Manager**, habilite o protocolo **TCP/IP**.

<img width="1273" height="684" alt="image" src="https://github.com/user-attachments/assets/00f2e15b-3099-469c-9f4b-cf7bdd678286" />


2. Nas propriedades do TCP/IP, vá na aba **Endereços IP** e certifique-se de definir a porta **1433** na seção **IPAll**.

<img width="1277" height="687" alt="image" src="https://github.com/user-attachments/assets/8fedf057-e06a-42fe-b98c-51b1d38a79a4" />

3. **Reinicie o serviço** do SQL Server para aplicar as mudanças.

<img width="1186" height="630" alt="image" src="https://github.com/user-attachments/assets/334c7288-5dd4-4c72-9f9e-80401d75a7b6" />



### 1.2 Segurança e Login (SSMS)
O SQL Server precisa aceitar conexões via usuário e senha (Autenticação Mista).

1. No **SSMS**, habilite o **Modo de Autenticação do SQL Server e do Windows** nas propriedades do servidor.
2. Em **Segurança > Logins**, habilite o usuário `sa` e defina uma senha forte.

### 1.3 Firewall do Windows
Abra a porta 1433 no Firewall para permitir a entrada do tráfego vindo do Mac. Execute no PowerShell (Admin):
```powershell
New-NetFirewallRule -DisplayName "SQL Server Remote" -Direction Inbound -LocalPort 1433 -Protocol TCP -Action Allow
