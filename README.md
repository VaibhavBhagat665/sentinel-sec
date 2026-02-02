# 🛡️ Project Sentinel
### The Autonomous Security Engineer for Your Codebase

[![PyPI version](https://badge.fury.io/py/sentinel-sec.svg)](https://pypi.org/project/sentinel-sec/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentinel** is an AI-powered security agent that doesn't just *find* vulnerabilities in your code — it **fixes them automatically**.

Powered by **Llama 3** (via Groq) for instant inference and **LibCST** for surgical code editing.

---

## 🚀 Quick Start

### Install
```bash
pip install sentinel-sec
```

### Setup (Choose One)

#### Option A: Ollama (FREE, OFFLINE) ⭐ Recommended
Run AI completely **on your machine** — no API keys, no internet needed.

1. **Install Ollama**: [ollama.ai/download](https://ollama.ai/download)
2. **Pull the model**:
   ```bash
   ollama pull llama3
   ```
3. **Start Ollama** (keep running in background):
   ```bash
   ollama serve
   ```
4. **Run Sentinel** — it auto-detects Ollama!

---

#### Option B: Groq (FAST, ONLINE)
Use Groq's cloud for blazing-fast inference.

1. Get free API key: [console.groq.com](https://console.groq.com/)
2. Set it:
   ```powershell
   # Windows
   $env:GROQ_API_KEY="gsk_your_key_here"
   ```
   ```bash
   # Linux/Mac
   export GROQ_API_KEY="gsk_your_key_here"
   ```

### Fix a File (Preview)
```bash
sentinel fix app.py
```
This analyzes your file and shows you the proposed fix.

### Fix a File (Auto-Apply)
```bash
sentinel apply app.py
```
This fixes the file **and writes the changes directly** (creates a `.bak` backup).

### Launch the Web Dashboard
```bash
sentinel ui
```
Opens an interactive chat interface at `http://localhost:8000`.

---

## 📖 How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PLANNER   │────▶│    CODER    │────▶│    TEST     │────▶│  REFLECTOR  │
│  Analyze    │     │  Generate   │     │  Verify     │     │  Critique   │
│  the CVE    │     │  the patch  │     │  the fix    │     │  if failed  │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                   │
                          ◀───────────────────────────────────────-┘
                                    (Loop until fixed)
```

1. **Planner**: Reads your code and the vulnerability description. Creates a remediation plan.
2. **Coder**: Writes a Python patch based on the plan.
3. **Test**: Runs the patch in a sandboxed environment (Docker).
4. **Reflector**: If tests fail, it critiques the code and sends feedback to the Coder.
5. **Repeat** until the tests pass (max 10 iterations).

---

## 💻 Usage Examples

### Example 1: SQL Injection Fix
**Your vulnerable code (`auth.py`):**
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"  # BAD!
    cursor.execute(query)
    return cursor.fetchone()
```

**Run Sentinel:**
```bash
sentinel apply auth.py -m "SQL Injection vulnerability"
```

**Result (automatically written to `auth.py`):**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE name = ?"  # FIXED!
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

---

### Example 2: Command Injection Fix
**Your vulnerable code (`ping.py`):**
```python
import os

def ping(ip):
    os.system("ping -c 1 " + ip)  # BAD!
```

**Run Sentinel:**
```bash
sentinel fix ping.py
```

**Proposed Fix:**
```python
import subprocess

def ping(ip):
    subprocess.run(["ping", "-c", "1", ip], check=True)  # FIXED!
```

---

## 🖥️ Web Dashboard (UI)

For a visual experience, run:
```bash
sentinel ui
```

Then open `http://localhost:8000` in your browser.

**Features:**
- 💬 Chat-based interface
- 🔄 See the agent's thought process in real-time
- ✅ Review and approve patches before applying

---

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `sentinel fix <file>` | Analyze and show the fix (preview only) |
| `sentinel apply <file>` | Analyze, fix, and write to the file |
| `sentinel ui` | Launch the web dashboard |
| `sentinel version` | Show version info |

**Options:**
- `-m, --message "description"` — Provide context about the vulnerability

---

## 📦 Installation Options

### From PyPI (Recommended)
```bash
pip install sentinel-sec
```

### From GitHub (Development)
```bash
git clone https://github.com/YOUR_USERNAME/project-sentinel.git
cd project-sentinel
pip install -e .
```

---

## ⚙️ Requirements

- Python 3.12+
- Docker (optional, for sandboxed testing)

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq (Llama 3.1 8B) |
| Agent Framework | LangGraph |
| Code Editing | LibCST |
| Web UI | Chainlit |
| Packaging | setuptools, twine |

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for blazing-fast inference
- [LangChain](https://langchain.com/) & [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- [LibCST](https://github.com/Instagram/LibCST) for surgical code modification

---

**Made with ❤️ by the Project Sentinel Team**
