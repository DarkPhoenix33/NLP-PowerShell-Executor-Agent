import os
import openai
from groq_prompt import get_powershell_prompt  
# Initialize Groq API Client
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="#Your_API_KEY"
)


def convert_nl_to_powershell(nl_instruction):
    """
    Converts a natural language instruction into a PowerShell command using Groq API.
    Ensures the response contains only the PowerShell command without explanation.
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": get_powershell_prompt()},  # Use Modular Prompt
                {"role": "user", "content": f"Convert this instruction into a valid PowerShell command:\n{nl_instruction}"},
            ],
            temperature=0.0,
            max_tokens=50
        )

        # Extract generated PowerShell command
        ps_command = response.choices[0].message.content.strip()

        # Ensure no markdown formatting
        ps_command = ps_command.replace("```powershell", "").replace("```", "").strip()

        return ps_command

    except Exception as e:
        return f"Error calling Groq API: {str(e)}"