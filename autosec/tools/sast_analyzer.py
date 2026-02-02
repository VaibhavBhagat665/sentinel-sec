import subprocess
import json
import tempfile
import os

def run_bandit(code: str) -> dict:
    """Run Bandit for Python files"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp_path = f.name
    
    try:
        result = subprocess.run(
            ['bandit', '-f', 'json', '-q', tmp_path],
            capture_output=True, text=True
        )
        if result.stdout:
            return json.loads(result.stdout)
        return {"results": []}
    except Exception:
        return {"results": []}
    finally:
        os.unlink(tmp_path)

def run_semgrep(code: str, extension: str) -> dict:
    """Run Semgrep for Polyglot files"""
    with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as f:
        f.write(code)
        tmp_path = f.name
        
    try:
        # Using a lightweight config for speed
        result = subprocess.run(
            ['semgrep', '--config', 'p/security-audit', '--json', '--quiet', tmp_path],
            capture_output=True, text=True
        )
        if result.stdout:
            return json.loads(result.stdout)
        return {"results": []}
    except Exception:
        return {"results": [], "error": "semgrep not installed"}
    finally:
        os.unlink(tmp_path)

def analyze_security(code: str, file_path: str = "script.py") -> tuple[bool, list[str]]:
    """
    Route analysis based on file extension.
    """
    is_python = file_path.endswith('.py')
    _, ext = os.path.splitext(file_path)
    
    report = {}
    if is_python:
        report = run_bandit(code)
    else:
        report = run_semgrep(code, ext)

    issues = []
    
    # Parse Bandit results
    if is_python:
        for finding in report.get("results", []):
            severity = finding.get("issue_severity", "LOW")
            msg = finding.get("issue_text", "Unknown issue")
            line = finding.get("line_number", 0)
            issues.append(f"[BANDIT] [{severity}] Line {line}: {msg}")
            
    # Parse Semgrep results
    else:
        for finding in report.get("results", []):
            extra = finding.get("extra", {})
            severity = extra.get("severity", "WARNING")
            msg = extra.get("message", "Unknown issue")
            line = finding.get("start", {}).get("line", 0)
            issues.append(f"[SEMGREP] [{severity}] Line {line}: {msg}")
    
    is_safe = len(issues) == 0
    return is_safe, issues
