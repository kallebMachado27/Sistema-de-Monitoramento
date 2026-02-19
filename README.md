Sentinel Linux Monitor

Sistema de monitoramento de servidores Linux com detecção de anomalias via Python.

Como Funciona:
Um script em Bash coleta métricas (CPU, RAM, Disco) a cada minuto e salva no MySQL. Um cliente Python conecta remotamente, analisa os dados e alerta se houver picos de uso.

Instalação:
Abra a pasta Arquivos
pip install -r requirements.txt
Configure o IP e Senha no arquivo analisador.py.
Execute: python analisador.py

Stack:
Linux Server
MySQL
Python 3

graph LR    %% Define os estilos (cores)    classDef server fill:#e1f5fe,stroke:#01579b,stroke-width:2px,stroke-dasharray: 5 5;    classDef db fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;    classDef client fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;    classDef alert fill:#ffccbc,stroke:#d84315,stroke-width:2px,color:#d84315;    %% Define os blocos    subgraph Servidor [Linux Server (Remoto)]        direction TB        CRON[Cron Job<br/>(Agendador)]        SCRIPT[robo.sh<br/>(Bash Script)]        MYSQL[(MySQL<br/>db_monitoramento)]    end    subgraph Local [Sua Máquina (Windows)]        VSC[VS Code]        PYTHON[analisador.py<br/>(Python Client)]    end        ALERT[🚨 Alerta de Risco]    %% Define as conexões (fluxo)    CRON -->|A cada 1 min| SCRIPT    SCRIPT -->|INSERT (Dados)| MYSQL        VSC -->|Executa| PYTHON    PYTHON -->|Conexão TCP/IP<br/>(Lê Dados)| MYSQL    MYSQL -->|Retorna Média| PYTHON    PYTHON -->|Se CPU > 80%| ALERT    %% Aplica as cores nos blocos    class CRON,SCRIPT server;    class MYSQL db;    class VSC,PYTHON client;    class ALERT alert;
