from openai import OpenAI
from context import DIGITAL_TWIN_SYSTEM_PROMPT
from tools import tools, record_email_tool
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr
import os
import subprocess
import json

subprocess.run(["ollama", "pull", "llama3.2"])

load_dotenv(override=True)
groq_api_key = os.getenv('GROQ_API_KEY')
openrouter_api = os.getenv('OPENROUTER_API_KEY')

groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key:
    print(f"Groq API Key exists and begins with {groq_api_key[:6]}\n")
else:
    print(f"Groq API Key not set.\n")


openrouter_api = os.getenv('OPENROUTER_API_KEY')
if openrouter_api:
    print(f"OpenRouter API key exists and begins with {openrouter_api[:6]}\n")
else:
    print(f"OpenRouter API key not set.\n")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"

groq = OpenAI(
    api_key= groq_api_key,
    base_url= GROQ_BASE_URL
)

openrouter = OpenAI(
    api_key= openrouter_api,
    base_url= OPENROUTER_BASE_URL
)

ollama = OpenAI(
    api_key= "anything",
    base_url= OLLAMA_BASE_URL
)

groq_model_name = "openai/gpt-oss-20b"
openrouter_nvidia_model_name = "nvidia/nemotron-3-ultra-550b-a55b:free"
openrouter_laguna_model_name = "poolside/laguna-s-2.1:free"
ollama_model_name = "llama3.2"

def get_client_and_model(model_choice):
    if model_choice == groq_model_name:
        return groq, model_choice
    elif model_choice in (openrouter_nvidia_model_name, openrouter_laguna_model_name):
        return openrouter, model_choice
    elif model_choice == ollama_model_name:
        return ollama, model_choice
    return groq, groq_model_name  # fallback


def chat(message, history, model_choice):
    client, model_name = get_client_and_model(model_choice)

    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": DIGITAL_TWIN_SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]

    response = client.chat.completions.create(model=model_name, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message_obj = response.choices[0].message
        tool_call = message_obj.tool_calls[0]
        email = json.loads(tool_call.function.arguments).get("email")
        record_email_tool(email)
        messages.append(message_obj)
        messages.append({"role": "tool", "content": "Email recorded", "tool_call_id": tool_call.id})
        response = client.chat.completions.create(model=model_name, messages=messages, tools=tools)

    return response.choices[0].message.content


if __name__ == "__main__":
    model_dropdown = gr.Dropdown(
        choices=[
            ("GPT-OSS 20B", groq_model_name),
            ("NVIDIA Nemotron 3 Ultra", openrouter_nvidia_model_name),
            ("Laguna S 2.1", openrouter_laguna_model_name),
            ("Llama 3.2", ollama_model_name),
        ],
        value=groq_model_name,
        label="Choose model",
    )

    gr.ChatInterface(
        chat,
        additional_inputs=[model_dropdown],
        additional_inputs_accordion=None,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base(), inbrowser=True)