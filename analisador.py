import mysql.connector
import paramiko
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES DO BANCO DE DADOS ---
DB_CONFIG = {
    'host': " ",      
    'user': " ",      
    'password': " ",  
    'database': " "   
}

# --- CONFIGURAÇÕES DE ACESSO REMOTO (SSH) ---
SSH_CONFIG = {
    'hostname': " ",  
    'port': 22,
    'username': " ", 
    'password': " "  
}

# --- FUNÇÃO DE MITIGAÇÃO AUTOMÁTICA ---
def trigger_mitigation():
    print("[INFO] Investigando processo pesado no servidor...")
    nome_processo = "Desconhecido"
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**SSH_CONFIG)

        # 1. Comando para descobrir quem está gastando mais CPU
        cmd_investigar = "ps aux --sort=-%cpu | head -n 2 | tail -n 1 | awk '{print $11}'"
        
        stdin, stdout, stderr = client.exec_command(cmd_investigar)
        nome_processo = stdout.read().decode().strip()
        
        if not nome_processo:
            print("[WARNING] Nenhum processo crítico encontrado para matar.")
            client.close()
            return "Nenhum processo"

        # 2. Comando para matar o processo encontrado
        cmd_matar = f"pkill {nome_processo}"
        stdin, stdout, stderr = client.exec_command(cmd_matar)
        
        error = stderr.read().decode()
        
        if error and "no process found" not in error:
            print(f"[WARNING] Retorno: {error}")
        else:
            print(f"[SUCCESS] Processo '{nome_processo}' eliminado com sucesso.")

        client.close()
        
        # Retorna o nome para gravar no banco
        return f"Morto processo: {nome_processo}"

    except Exception as e:
        print(f"[ERROR] Falha na mitigação: {e}")
        return f"Erro: {str(e)}"

# --- MONITORAMENTO PRINCIPAL ---
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Consulta média dos últimos 5 minutos
        # Consulta média dos últimos 5 minutos para TODOS os indicadores
    query = """
        SELECT 
            AVG(cpu_percent), 
            AVG(mem_percent), 
            AVG(disk_percent) 
        FROM metricas 
        WHERE data_hora >= NOW() - INTERVAL 5 MINUTE
    """
    cursor.execute(query)
    result = cursor.fetchone()
    
    # "Desempacota" os dados (um em cada variável)
    avg_cpu, avg_ram, avg_disk = result

    # Lógica Principal
    # Define os limites críticos para cada recurso
    LIMITE_CPU = 80.0
    LIMITE_RAM = 90.0
    LIMITE_DISCO = 90.0

    # Variável para saber o motivo do alerta
    motivo = "Normal"

    # Verifica cada recurso individualmente (OR = OU)
    if avg_cpu > LIMITE_CPU:
        motivo = "CPU Crítica"
    elif avg_ram > LIMITE_RAM:
        motivo = "Memória Cheia"
    elif avg_disk > LIMITE_DISCO:
        motivo = "Disco Cheio"
    
    # Status na tela
    print(f"[STATUS] CPU: {avg_cpu:.2f}% | RAM: {avg_ram:.2f}% | Disco: {avg_disk:.2f}%")

    # Se encontrar um problema (motivo != Normal), ativa a ação
    if motivo != "Normal":
        print(f"[ALERT] Disparado por: {motivo}. Iniciando protocolo de recuperação.")
        
        # Executa a mitigação e captura o log de volta
        mensagem_log = trigger_mitigation()
        
        # Grava no banco (agora com o motivo no registro)
        texto_descricao = f"{motivo} - {mensagem_log}"
        cursor.execute("INSERT INTO metricas (cpu_percent, mem_percent, disk_percent, descricao) VALUES (-1, 0, 0, %s)", (texto_descricao,))
        conn.commit()
        print("[LOG] Incidente registrado no banco de dados.")
    else:
        print("[STATUS] Sistema operando dentro dos parâmetros normais.")

    conn.close()

except Exception as e:
    print(f"[ERROR] Erro geral no sistema: {e}")