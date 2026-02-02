# Example: Path Traversal Vulnerability
# Run: sentinel apply examples/vulnerable_path.py

import os

def read_file(filename):
    """
    VULNERABLE: This function is susceptible to Path Traversal.
    An attacker can input: ../../../etc/passwd
    """
    # BAD: No validation of user-supplied path
    filepath = os.path.join("/var/www/uploads", filename)
    
    with open(filepath, "r") as f:
        return f.read()

def serve_image(image_name):
    """
    VULNERABLE: Another path traversal example.
    """
    # BAD: Direct concatenation
    path = "/images/" + image_name
    return open(path, "rb").read()

if __name__ == "__main__":
    print(read_file("report.pdf"))
