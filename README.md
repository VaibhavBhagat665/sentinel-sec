# 🛡️ Project Sentinel
### The Autonomous Security Engineer for Your Codebase

[![PyPI version](https://badge.fury.io/py/sentinel-sec.svg)](https://pypi.org/project/sentinel-sec/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentinel** is an AI-powered security agent that doesn't just *find* vulnerabilities in your code — it **fixes them automatically**.

Powered by **Llama 3** (via Groq/Ollama) and **Neuro-Symbolic** verification (Bandit/Semgrep).

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

#### Option B: Groq (FAST, ONLINE)
Use Groq's cloud for blazing-fast inference.

1. Get free API key: [console.groq.com/keys](https://console.groq.com/keys)
2. Set it (key starts with `gsk_`):
   ```powershell
   # Windows
   $env:GROQ_API_KEY="gsk_your_key_here"
   ```
   ```bash
   # Linux/Mac
   export GROQ_API_KEY="gsk_your_key_here"
   ```

---

## ⚡ Multi-Language Support (v0.2.1)

Sentinel now supports auto-fixing vulnerabilities in:

| Language | Supported Files | Verification Tool |
|----------|-----------------|-------------------|
| **Python** | `.py` | Bandit (SAST) |
| **JavaScript** | `.js` | Semgrep |
| **TypeScript** | `.ts` | Semgrep |
| **Java** | `.java` | Semgrep |
| **C++** | `.cpp`, `.c` | Semgrep |
| **Go** | `.go` | Semgrep |
| **SQL** | `.sql` | Semgrep |

**Usage is identical:**
```bash
sentinel fix src/main.cpp
sentinel apply services/auth.js
```

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

1. **Planner**: Analyzes code & vulnerability. Uses RAG to find fix patterns.
2. **Coder**: Writes the patch in the target language (Python, C++, JS, etc.).
3. **Verifier**: Runs SAST (Bandit or Semgrep) to verify safety.
4. **Reflector**: If SAST fails, providing feedback for self-correction.

---

## 💻 Usage Examples

### Python (SQL Injection)
```bash
sentinel apply auth.py
```

### JavaScript (XSS)
```bash
sentinel apply frontend/input.js
```

### C++ (Buffer Overflow)
```bash
sentinel fix src/buffer_test.cpp
```

---

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `sentinel setup` | Interactive setup guide |
| `sentinel fix <file>` | Analyze and show fix (preview only) |
| `sentinel apply <file>` | Analyze, fix, and write to the file |
| `sentinel ui` | Launch the web dashboard |
| `sentinel version` | Show version info |

---

## 📦 Installation Options

### From PyPI (Recommended)
```bash
pip install sentinel-sec
```

### From GitHub (Development)
```bash
git clone https://github.com/VaibhavBhagat665/sentinel-sec.git
cd sentinel-sec
pip install -e .
```

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

**Made with ❤️ by a mad man**
