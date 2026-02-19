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

graph LR
    classDef server fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef db fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    classDef client fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef alert fill:#ffccbc,stroke:#d84315,stroke-width:2px

    subgraph Linux [Linux Server]
        CRON[Cron Job] --> SCRIPT[robo.sh]
        SCRIPT -->|INSERT| MYSQL[(MySQL)]
    end

    subgraph Windows [Windows Local]
        VSC[VS Code] --> PYTHON[Python Client]
    end

    PYTHON -->|SELECT| MYSQL
    MYSQL -->|Dados| PYTHON
    PYTHON -->|Alerta| ALERT[🚨]

    class CRON,SCRIPT server
    class MYSQL db
    class VSC,PYTHON client
    class ALERT alert
