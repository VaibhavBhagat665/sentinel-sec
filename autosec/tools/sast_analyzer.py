import subprocess
import json
import tempfile
import os

def run_bandit(code: str) -> dict:
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
        return {"results": [], "error": "bandit not installed"}
    finally:
        os.unlink(tmp_path)

def analyze_security(code: str) -> tuple[bool, list[str]]:
    report = run_bandit(code)
    issues = []
    
    for finding in report.get("results", []):
        severity = finding.get("issue_severity", "LOW")
        msg = finding.get("issue_text", "Unknown issue")
        line = finding.get("line_number", 0)
        issues.append(f"[{severity}] Line {line}: {msg}")
    
    is_safe = len(issues) == 0
    return is_safe, issues
