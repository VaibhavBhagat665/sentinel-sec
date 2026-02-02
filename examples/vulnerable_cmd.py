# Example: Command Injection Vulnerability
# Run: sentinel apply examples/vulnerable_cmd.py

import os

def ping_host(hostname):
    """
    VULNERABLE: This function is susceptible to Command Injection.
    An attacker can input: 127.0.0.1; rm -rf /
    """
    # BAD: Using os.system with user input
    os.system(f"ping -c 1 {hostname}")

def lookup_dns(domain):
    """
    VULNERABLE: Another command injection example.
    """
    # BAD: Shell=True with user input
    import subprocess
    subprocess.call(f"nslookup {domain}", shell=True)

if __name__ == "__main__":
    ping_host("google.com")
