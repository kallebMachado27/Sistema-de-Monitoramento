#!/bin/bash

# Configurações do Banco
DB_USER=" "
DB_PASS=" "
DB_NAME=" "
DB_HOST=" "

# 1. Coletar CPU (Uso em %)
# O comando top extrai apenas o uso de CPU idle, e o awk calcula o usado
CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

# 2. Coletar Memória RAM
# Pega o usado / total
MEM=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')

# 3. Coletar Disco
# Pega o uso da partição raiz (/)
DISK=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')

# 4. Inserir no MySQL
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME -e "INSERT INTO metricas (cpu_percent, mem_percent, disk_percent) VAL>
echo "Dados coletados: CPU: $CPU% - RAM: $MEM% - Disco: $DISK%"