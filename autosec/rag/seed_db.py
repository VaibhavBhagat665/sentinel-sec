from autosec.rag.retriever import CVERetriever

def seed_cve_db():
    r = CVERetriever()
    
    cves = [
        ("CWE-89", "SQL Injection via string concatenation in query", "Use parameterized queries with placeholders"),
        ("CWE-78", "OS Command Injection via os.system or shell=True", "Use subprocess with shell=False and list args"),
        ("CWE-22", "Path Traversal via unsanitized file paths", "Validate path with os.path.realpath and check prefix"),
        ("CWE-79", "Cross-Site Scripting via unescaped HTML output", "Use html.escape() or template auto-escaping"),
        ("CWE-502", "Insecure Deserialization with pickle", "Avoid pickle for untrusted data, use JSON"),
        ("CWE-798", "Hardcoded credentials in source code", "Use environment variables or secrets manager"),
        ("CWE-327", "Use of weak cryptographic algorithm MD5/SHA1", "Use SHA-256 or bcrypt for passwords"),
        ("CWE-918", "Server-Side Request Forgery via URL parameter", "Validate URL scheme and host whitelist"),
    ]
    
    for cve_id, desc, fix in cves:
        r.add_cve(cve_id, desc, fix)
        print(f"Added {cve_id}")
    
    print("CVE database seeded.")

if __name__ == "__main__":
    seed_cve_db()
