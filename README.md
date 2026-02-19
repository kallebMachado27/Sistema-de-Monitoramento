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

