import os
from fastapi import FastAPI, Request
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from testapp.groq_ai import convert_nl_to_powershell
from powershell_executor import execute_powershell

# Set Microsoft Bot Credentials from Environment Variables
MICROSOFT_APP_ID = os.getenv("MICROSOFT_APP_ID", "your-app-id")
MICROSOFT_APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "your-client-secret")

SETTINGS = BotFrameworkAdapterSettings(app_id=MICROSOFT_APP_ID, app_password=MICROSOFT_APP_PASSWORD)
bot_adapter = BotFrameworkAdapter(SETTINGS)

app = FastAPI()

class TeamsBot:
    async def on_message_activity(self, turn_context: TurnContext):
        """Handles incoming Teams messages, converts NL to PowerShell, executes, and responds."""
        user_input = turn_context.activity.text.strip()
        
        # Convert NL to PowerShell command
        ps_command = convert_nl_to_powershell(user_input)

        # Execute PowerShell command
        execution_output = execute_powershell(ps_command)

        # Send response back to Teams
        await turn_context.send_activity(f"💻 PowerShell Command: `{ps_command}`\n\n📜 Output:\n```\n{execution_output}\n```")

@app.post("/api/messages")
async def messages(request: Request):
    """Handles incoming messages from Microsoft Teams"""
    body = await request.json()
    activity = Activity().deserialize(body)
    
    async def turn(turn_context: TurnContext):
        bot = TeamsBot()
        await bot.on_message_activity(turn_context)

    await bot_adapter.process_activity(activity, turn)
    return {"status": "success"}
