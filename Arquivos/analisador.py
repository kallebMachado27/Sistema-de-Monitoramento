import mysql.connector
from datetime import datetime, timedelta

# Conexão com o banco no servidor Linux
db = mysql.connector.connect(
    host="192.168.1.12",
    user="kalleb",
    password="123456",
    database="Monitoramento"
)

cursor = db.cursor()

# Buscar média dos últimos 5 minutos
query = """
    SELECT AVG(cpu_percent) as media_cpu 
    FROM metricas 
    WHERE data_hora >= NOW() - INTERVAL 5 MINUTE
"""
cursor.execute(query)
resultado = cursor.fetchone()
media_cpu = resultado[0]

print(f"Média de CPU nos últimos 5 min: {media_cpu:.2f}%")


if media_cpu > 80.0:
    print("⚠️ ALERTA: CPU CRÍTICA! Acionando protocolo de segurança...")
  
    log_query = "INSERT INTO metricas (cpu_percent, mem_percent, disk_percent) VALUES (-1, 0, 0)"
    cursor.execute(log_query)
    db.commit()
    print("Incidente registrado no banco de dados (CPU = -1 indica alerta).")
else:
    print("Sistema funcionando dentro da normalidade.")

db.close()