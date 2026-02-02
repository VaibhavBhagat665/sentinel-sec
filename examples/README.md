# Examples

This folder contains intentionally vulnerable Python files for testing Sentinel.

## How to Use

### 1. SQL Injection Example
```bash
sentinel fix examples/vulnerable_sql.py
# or to auto-apply:
sentinel apply examples/vulnerable_sql.py
```

### 2. Command Injection Example
```bash
sentinel fix examples/vulnerable_cmd.py
```

### 3. Path Traversal Example
```bash
sentinel fix examples/vulnerable_path.py
```

## What to Expect

Sentinel will:
1. Analyze the code
2. Identify the vulnerability
3. Generate a secure fix
4. (If using `apply`) Write the fix directly to the file

A backup file (`.bak`) is created when using `apply`.
