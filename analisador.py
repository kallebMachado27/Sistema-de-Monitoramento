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
    query = """
        SELECT AVG(cpu_percent) 
        FROM metricas 
        WHERE data_hora >= NOW() - INTERVAL 5 MINUTE
    """
    cursor.execute(query)
    result = cursor.fetchone()
    avg_cpu = result[0]

    # Lógica Principal
    if avg_cpu is not None:
        print(f"[STATUS] Média de CPU (5 min): {avg_cpu:.2f}%")

        # Verifica se a CPU está alta 
        if avg_cpu > 80.0:
            print("[ALERT] CPU acima do limiar crítico (>80%). Iniciando protocolo de recuperação.")
            
            # 1. Chama a  função e captura o retorno (quem morreu?)
            mensagem_log = trigger_mitigation()
            
            # 2. Registra o incidente no banco 
            cursor.execute("INSERT INTO metricas (cpu_percent, mem_percent, disk_percent, descricao) VALUES (-1, 0, 0, %s)", (mensagem_log,))
            conn.commit()
            print("[LOG] Incidente registrado no banco de dados.")
        else:
            print("[STATUS] Sistema operando dentro dos parâmetros normais.")
    else:
        print("[ERROR] Nenhum dado recebido da base de dados.")

    conn.close()

except Exception as e:
    print(f"[ERROR] Erro geral no sistema: {e}")