Sentinel Linux Monitor

Sistema de monitoramento de servidores Linux com detecção de anomalias via Python.

Como Funciona:
Um script em Bash coleta métricas (CPU, RAM, Disco) a cada minuto e salva no MySQL. Um cliente Python conecta remotamente, analisa os dados e alerta se houver picos de uso.

Correção Automática: 
Ao detectar CPU crítica (>80%), o sistema utiliza SSH (Paramiko) para conectar no servidor e executar comandos de mitigação (ex: matar processos travados) sem intervenção humana.

Instalação:
Abra a pasta Arquivos
pip install -r requirements.txt
Configure o IP e Senha no arquivo analisador.py.
Execute: python analisador.py

Stack:
Linux Server
MySQL
Python 3
paramiko

