# Digital Twin

**An AI agent that acts as your digital twin, using your LinkedIn profile PDF export and a personal summary as context to answer questions about your background, experience, projects, and skills. It can also collect visitors’ email addresses and record them in a text file for follow-up.**

## Features

- 💬 Conversational AI digital twin
- 🤖 Support for multiple LLMs:
  - GPT-OSS 20B through Groq
  - NVIDIA Nemotron 3 Ultra through OpenRouter
  - Laguna S 2.1 through OpenRouter
  - Llama 3.2 through Ollama
- 🔄 Switch models directly from the chat interface
- 🛠️ Tool calling for collecting visitor email addresses
- 💾 Stores submitted emails locally in `emails.txt`
- 🎨 Custom Gradio UI and styling
- 🏠 Runs locally with Ollama or remotely through Groq/OpenRouter

---

## Project Structure

```text
Digital Twin/
│
├── app.py              # Main Gradio application
├── context.py          # Digital twin system prompt
├── tools.py            # Tool definitions and email recording
├── styles.py           # UI styling and JavaScript
├── linkedin.pdf        # NOT included in the repository
├── summary.txt         # NOT included in the repository
├── emails.txt          # Stores collected emails
└── Digital Twin.ipynb  # Original development notebook
```

> **Note:** `linkedin.pdf` and `summary.txt` contain personal information and are intentionally excluded from the repository.

---

# Setup Guide

## 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd "Digital Twin"
```

If the repository is being cloned as part of a larger project, make sure you are working inside the `Digital Twin` directory.

---

## 2. Create a virtual environment

The repository does **not** include `.venv`.

Create a new virtual environment using Python:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

You should then see something similar to:

```text
(.venv) PS D:\...\Digital Twin>
```

---

## 3. Install dependencies

Install the required packages:

```bash
pip install openai gradio python-dotenv
```

You also need **Ollama** installed if you want to use the local Llama 3.2 model.

Verify it with:

```bash
ollama --version
```

---

# 4. Set up API keys

The application uses environment variables for the remote model providers.

Create a `.env` file in the `Digital Twin` directory:

```text
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Do **not** commit `.env` to GitHub.

The application loads these variables using `python-dotenv`.

---

# 5. Set up Ollama

If you want to use **Llama 3.2**, install Ollama and make sure it is running.

Then pull the model:

```bash
ollama pull llama3.2
```

The application also attempts to pull the model automatically when it starts:

```python
subprocess.run(["ollama", "pull", "llama3.2"])
```

You can therefore simply make sure Ollama is installed and running.

---

# 6. Add the personal data

Two files are intentionally missing from the repository:

```text
linkedin.pdf
summary.txt
```

These files contain the information used to construct the digital twin.

Before running the application, place the required files in the project directory:

```text
Digital Twin/
├── app.py
├── context.py
├── tools.py
├── styles.py
├── linkedin.pdf
├── summary.txt
└── ...
```

If you are setting up the project for a different person, replace these files with that person's professional information and update `context.py` accordingly.

> **Important:** Do not commit personal documents such as `linkedin.pdf` or other private profile information to the public repository.

---

# 7. Run the application

From the `Digital Twin` directory:

```bash
python app.py
```

Gradio will start a local web server.

Open the URL shown in the terminal, typically:

```text
http://127.0.0.1:7860
```

---

# Model Selection

The interface supports four models:

| Model | Provider | Type |
|---|---|---|
| GPT-OSS 20B | Groq | Cloud |
| NVIDIA Nemotron 3 Ultra | OpenRouter | Cloud |
| Laguna S 2.1 | OpenRouter | Cloud |
| Llama 3.2 | Ollama | Local |

The selected model is passed to the chat function, which chooses the appropriate OpenAI-compatible client:

```text
GPT-OSS 20B
       ↓
     Groq

Nemotron / Laguna
       ↓
   OpenRouter

Llama 3.2
       ↓
     Ollama
```

All providers use the OpenAI-compatible API interface.

---

# Tool Calling

The digital twin has access to a tool that records visitor email addresses.

When the model determines that an email should be recorded, the tool is called and the email is saved locally.

The recorded emails are stored in:

```text
emails.txt
```

The tool is implemented in:

```text
tools.py
```

---

# Troubleshooting

### `ModuleNotFoundError`

If you see something like:

```text
ModuleNotFoundError: No module named 'gradio'
```

make sure the virtual environment is activated and install the dependencies:

```bash
.venv\Scripts\activate
pip install openai gradio python-dotenv
```

---

### Missing API key

If you see:

```text
OpenAIError: Missing credentials
```

check that your `.env` file exists in the project directory and contains:

```text
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

Also make sure there are no unnecessary quotation marks or spaces around the values.

---

### Llama 3.2 doesn't work

Make sure Ollama is installed and running:

```bash
ollama --version
```

Then:

```bash
ollama pull llama3.2
```

You can verify that the model exists with:

```bash
ollama list
```

---

### Personal data files are missing

The repository intentionally does not contain:

```text
linkedin.pdf
summary.txt
```

These must be supplied separately before running the version of the project that depends on them.

---

## Security Notes

Do **not** commit any of the following to the repository:

```text
.env
.venv/
linkedin.pdf
summary.txt
```

API keys and personal professional documents should remain private.

A suitable `.gitignore` should include:

```gitignore
.venv/
.env
__pycache__/
linkedin.pdf
summary.txt
.gradio/
```

---

## Technologies

- **Python**
- **Gradio** — web interface
- **OpenAI Python SDK** — unified interface for the LLM providers
- **Groq** — cloud inference
- **OpenRouter** — access to additional models
- **Ollama** — local LLM inference
- **python-dotenv** — environment variable management

---

## Author

**Marwa Omar**

AI/ML Engineer

This project was developed as part of an exploration of **LLM applications, tool calling, and agentic AI workflows**.
