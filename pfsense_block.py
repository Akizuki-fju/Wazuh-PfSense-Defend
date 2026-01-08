#!/var/ossec/framework/python/bin/python3
# Wazuh Active Response to pfSense (SSH Block)
# Usage: This script is called by Wazuh Manager to block IP on pfSense via SSH.

import sys
import json
import time
import paramiko

# --- Configuration ---
PFSENSE_IP = "192.168.56.1"
PFSENSE_USER = "admin"
PFSENSE_PASS = "pfsense" 

def send_log(msg):
    log_file = "/var/ossec/logs/active-responses.log"
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} active-response/pfsense: {msg}\n")

def main():
    try:
        # 1. Read input from Wazuh
        input_data = sys.stdin.read()
        alert = json.loads(input_data)
        
        # 2. Extract command and source IP
        command = alert.get("command")
        src_ip = alert.get("parameters", {}).get("alert", {}).get("data", {}).get("srcip")

        if not src_ip:
            return 

        # 3. Define Firewall Command (easyrule)
        # We focus on 'add' (block) action here
        if command == "add":
            cmd = f"/usr/local/bin/easyrule block wan {src_ip}"
            
            # 4. Execute via SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(PFSENSE_IP, username=PFSENSE_USER, password=PFSENSE_PASS)
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            
            send_log(f"Executed: {cmd} | Result: {output}")
            ssh.close()

    except Exception as e:
        send_log(f"Error: {str(e)}")

if __name__ == "__main__":
    main()