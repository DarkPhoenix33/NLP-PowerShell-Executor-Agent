from fastapi import FastAPI
from fastapi import Form
from fastapi.responses import HTMLResponse
from jinja2 import Template
from testapp.groq_ai import convert_nl_to_powershell
from powershell_executor import execute_powershell

app = FastAPI()

# HTML Template for UI
html_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>PowerShell AI Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .container { max-width: 600px; margin: auto; }
        input, button { width: 100%; padding: 10px; margin-top: 10px; }
        pre { background: #f4f4f4; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>PowerShell AI Assistant</h2>
        <form method="post">
            <input type="text" name="query" placeholder="Enter your command..." required>
            <button type="submit">Run</button>
        </form>
        {% if query %}
        <h3>Natural Language Query:</h3>
        <p>{{ query }}</p>
        <h3>Generated PowerShell Command:</h3>
        <pre>{{ ps_command }}</pre>
        <h3>Execution Output:</h3>
        <pre>{{ execution_output }}</pre>
        {% endif %}
    </div>
</body>
</html>
""")

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_template.render()

@app.post("/", response_class=HTMLResponse)
async def run_powershell(query: str = Form(...)):
    # Convert NL to PowerShell
    ps_command = convert_nl_to_powershell(query)
    
    # Execute PowerShell
    execution_output = execute_powershell(ps_command)
    
    return html_template.render(query=query, ps_command=ps_command, execution_output=execution_output)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
