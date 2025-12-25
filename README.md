# 🗄️ SQL Server Remote Access from macOS (VS Code)
-- Configuração de Acesso Remoto: SQL Server no Windows para VS Code no macOS

Este guia fornece um passo a passo detalhado sobre como configurar o **Microsoft SQL Server** (instalado em um laptop Windows) para aceitar conexões remotas vindas do **Visual Studio Code** em um ambiente **macOS (Ventura ou superior)**.

## 📋 Pré-requisitos

* Laptop com **Windows** e **SQL Server** instalado (Versão 2025/17.x ou anterior).
* Laptop com **macOS** e **Visual Studio Code** instalado.
* Ambos os dispositivos devem estar na **mesma rede local**.

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

---

## 🛠️ Passo 1: Configuração do Servidor (No Windows)

### 1.1 Habilitar Protocolo TCP/IP

O SQL Server, por padrão, não permite conexões de rede. Precisamos ativar o protocolo TCP/IP.

1. Abra o **SQL Server Configuration Manager**.
2. Vá em **Configuração de Rede do SQL Server** > **Protocolos para MSSQLSERVER**.
3. Clique com o botão direito em **TCP/IP** e selecione **Habilitar**.
4. Nas propriedades de **TCP/IP**, vá na aba **Endereços IP**, role até **IPAll** e defina a **Porta TCP** como `1433`. Certifique-se de que "Portas TCP Dinâmicas" esteja vazio.

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

Pressione `Cmd + Shift + E` para ver os resultados na grade lateral.

---

## 💡 Vantagens do VS Code vs SSMS

* **Ambiente Único:** Desenvolva código e gerencie o banco no mesmo editor.
* **Performance:** Interface muito mais rápida e leve que o SSMS no Windows.
* **Exportação:** Exporte resultados para JSON, CSV ou Excel com um clique.

---

### Dicas para as Imagens no GitHub:

Ao subir para o seu repositório:

1. Crie uma pasta chamada `/images`.
2. Renomeie suas fotos para nomes descritivos (ex: `firewall_config.png`, `vscode_connection.png`).
3. No arquivo `README.md`, aponte para elas usando o código: `![Descrição](images/nome_da_imagem.png)`.
