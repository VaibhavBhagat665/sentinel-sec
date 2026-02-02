import argparse
import sys
import subprocess
import os

try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = RESET = ""

def print_banner():
    print(f"""
{CYAN}╔═══════════════════════════════════════╗
║  🛡️  SENTINEL - Security Agent         ║
║     Autonomous Vulnerability Fixer    ║
╚═══════════════════════════════════════╝{RESET}
""")

def run_setup():
    print_banner()
    print(f"{YELLOW}Let's get you set up!{RESET}\n")
    
    print("Step 1: LLM Provider")
    print("─" * 40)
    print(f"""
{GREEN}Option A: Ollama (FREE, runs locally){RESET}
  1. Download: https://ollama.ai/download
  2. Install and run Ollama
  3. Pull a model:
     {CYAN}ollama pull llama3{RESET}
  4. Done! Sentinel will auto-detect it.

{GREEN}Option B: Groq Cloud (fast, free tier){RESET}
  1. Sign up: https://console.groq.com/keys
  2. Create API key (starts with "gsk_")
  3. Set it:
     Windows:  {CYAN}$env:GROQ_API_KEY="gsk_..."{RESET}
     Mac/Linux: {CYAN}export GROQ_API_KEY="gsk_..."{RESET}
""")
    
    print("Step 2: Test It")
    print("─" * 40)
    print(f"""
  {CYAN}sentinel fix your_file.py{RESET}
  
  This will analyze the file and show you a security patch.
  
  To auto-apply the fix:
  {CYAN}sentinel apply your_file.py{RESET}
""")
    
    print("Step 3: Try Examples")
    print("─" * 40)
    print(f"""
  We included example vulnerable files:
  {CYAN}sentinel fix examples/vulnerable_sql.py{RESET}
  {CYAN}sentinel fix examples/vulnerable_cmd.py{RESET}
""")
    print(f"{GREEN}✓ Setup complete! Run 'sentinel fix <file>' to start.{RESET}")

def run_fix_headless(file_path, issue_desc):
    from langchain_core.messages import HumanMessage
    from autosec.agent.graph import build_graph
    
    print_banner()
    print(f"{CYAN}Analyzing:{RESET} {file_path}\n")
    
    if not os.path.exists(file_path):
        print(f"{RED}Error: File not found: {file_path}{RESET}")
        return None

    with open(file_path, "r") as f:
        content = f.read()

    issue = issue_desc or "Fix security vulnerabilities in this file."
    rag_context = f"Target: {file_path}\n\n```python\n{content}\n```\n\n{issue}"

    print(f"{YELLOW}[1/4]{RESET} Building agent graph...")
    app = build_graph()
    
    initial_state = {
        "messages": [HumanMessage(content=f"Fix: {file_path}. {issue}")],
        "cve_id": "SENTINEL-FIX",
        "repo_path": os.path.abspath(file_path),
        "rag_context": rag_context,
        "iterations": 0,
        "sast_issues": []
    }

    try:
        print(f"{YELLOW}[2/4]{RESET} Planning remediation...")
        print(f"{YELLOW}[3/4]{RESET} Generating patch...")
        print(f"{YELLOW}[4/4]{RESET} Verifying with SAST...")
        
        final_state = app.invoke(initial_state)
        patch = final_state.get("current_patch")
        
        if patch:
            print(f"\n{GREEN}✓ Patch generated successfully!{RESET}\n")
            print("─" * 50)
            print(patch)
            print("─" * 50)
            print(f"\n{CYAN}To apply: sentinel apply {file_path}{RESET}")
        else:
            print(f"{RED}No patch generated.{RESET}")
            
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return None
    
    return patch

def run_apply_headless(file_path, issue_desc):
    print_banner()
    print(f"{CYAN}APPLY MODE:{RESET} {file_path}\n")
    
    patch = run_fix_headless(file_path, issue_desc)
    
    if not patch:
        print(f"{RED}No patch generated. File unchanged.{RESET}")
        return
    
    backup_path = file_path + ".bak"
    try:
        with open(file_path, "r") as f:
            original = f.read()
        with open(backup_path, "w") as f:
            f.write(original)
        print(f"{YELLOW}Backup saved: {backup_path}{RESET}")
    except Exception as e:
        print(f"{RED}Backup failed: {e}{RESET}")
    
    try:
        with open(file_path, "w") as f:
            f.write(patch)
        print(f"{GREEN}✓ File patched: {file_path}{RESET}")
    except Exception as e:
        print(f"{RED}Write failed: {e}{RESET}")

def run_ui():
    print_banner()
    print(f"{CYAN}Starting Web Dashboard...{RESET}")
    base_path = os.path.dirname(__file__)
    app_path = os.path.join(base_path, "ui", "app.py")
    subprocess.run([sys.executable, "-m", "chainlit", "run", app_path, "-w"])

def main():
    parser = argparse.ArgumentParser(description="Sentinel: Autonomous Security Agent")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("setup", help="First-time setup guide")
    subparsers.add_parser("ui", help="Launch web dashboard")
    subparsers.add_parser("version", help="Show version")

    fix_parser = subparsers.add_parser("fix", help="Analyze and show fix")
    fix_parser.add_argument("file")
    fix_parser.add_argument("-m", "--message", default=None)

    apply_parser = subparsers.add_parser("apply", help="Apply fix to file")
    apply_parser.add_argument("file")
    apply_parser.add_argument("-m", "--message", default=None)

    args = parser.parse_args()

    if args.command == "setup":
        run_setup()
    elif args.command == "ui":
        run_ui()
    elif args.command == "fix":
        run_fix_headless(args.file, args.message)
    elif args.command == "apply":
        run_apply_headless(args.file, args.message)
    elif args.command == "version":
        print("Sentinel v0.2.0 - Autonomous Security Agent")
    else:
        print_banner()
        parser.print_help()
        print(f"\n{YELLOW}First time? Run: sentinel setup{RESET}")

if __name__ == "__main__":
    main()
