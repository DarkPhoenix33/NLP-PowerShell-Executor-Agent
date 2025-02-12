import subprocess
import paramiko
import ctypes
import sys

def is_admin():
    """Checks if the script is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def execute_powershell(command):
    """
    Executes a PowerShell command locally with Administrator privileges.
    If not running as an Administrator, it will restart itself with elevated privileges.
    """
    try:
        # If not admin, restart script with elevated privileges
        if not is_admin():
            return elevate_script(command)

        # Properly execute the PowerShell command
        result = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
                                capture_output=True, text=True, shell=True)

        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"

    except Exception as e:
        return f"Local PowerShell execution failed: {str(e)}"

def elevate_script(command):
    """Restarts the script with Administrator privileges and passes the PowerShell command."""
    try:
        # Format the PowerShell command properly
        command_to_run = f"powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"{command}\""
        
        # Run the command as Administrator
        subprocess.run(["powershell.exe", "-Command", f"Start-Process powershell.exe -Verb runAs -ArgumentList '{command_to_run}'"],
                       shell=True)
        
        return "Script restarted with Administrator privileges. Executing command..."
    except Exception as e:
        return f"Failed to elevate privileges: {str(e)}"



    
def execute_remote_powershell(command, server_ip, username, password):
    """
    Executes a PowerShell command on a remote Windows Server via SSH.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=username, password=password)
        
        stdin, stdout, stderr = ssh.exec_command(f"powershell -Command {command}")
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        ssh.close()
        return output if output else f"Error: {error}"
    except Exception as e:
        return f"Remote PowerShell execution failed: {str(e)}"
