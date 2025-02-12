from powershell_executor import execute_powershell

command = "Get-IISAppPool | Where-Object { $_.State -eq 'Started' }"
output = execute_powershell(command)

print("PowerShell Output:\n", output)
