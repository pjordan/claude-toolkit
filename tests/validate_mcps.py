#!/usr/bin/env python3
"""
Validate MCP servers in the claude-toolkit repository.

This script checks:
- Directory structure
- Required files exist
- server.py is valid Python
- requirements.txt is properly formatted
- .env.example exists
- README.md is present and formatted
- No sensitive data in files
"""

import os
import sys
from pathlib import Path
import ast
import re

class MCPValidator:
    def __init__(self, mcps_dir="mcps/servers"):
        self.mcps_dir = Path(mcps_dir)
        self.errors = []
        self.warnings = []
    
    def validate_all(self):
        """Validate all MCP servers."""
        print("🔍 Validating MCP servers...\n")
        
        if not self.mcps_dir.exists():
            self.errors.append(f"MCPs directory not found: {self.mcps_dir}")
            return False
        
        server_dirs = [d for d in self.mcps_dir.iterdir() if d.is_dir()]
        
        if not server_dirs:
            self.warnings.append("No MCP servers found to validate")
            return True
        
        for server_dir in server_dirs:
            print(f"Validating: {server_dir.name}")
            self.validate_server(server_dir)
        
        self.print_results()
        return len(self.errors) == 0
    
    def validate_server(self, server_dir: Path):
        """Validate a single MCP server directory."""
        # Check required files
        server_py = server_dir / "server.py"
        requirements = server_dir / "requirements.txt"
        env_example = server_dir / ".env.example"
        readme = server_dir / "README.md"
        
        if not server_py.exists():
            self.errors.append(f"  ❌ Missing server.py in {server_dir.name}")
            return
        
        if not requirements.exists():
            self.warnings.append(
                f"  ⚠️  Missing requirements.txt in {server_dir.name}"
            )
        
        if not env_example.exists():
            self.warnings.append(
                f"  ⚠️  Missing .env.example in {server_dir.name}"
            )
        
        if not readme.exists():
            self.warnings.append(
                f"  ⚠️  Missing README.md in {server_dir.name}"
            )
        
        # Validate server.py
        self.validate_server_py(server_py, server_dir.name)
        
        # Validate requirements.txt
        if requirements.exists():
            self.validate_requirements(requirements, server_dir.name)
        
        # Validate .env.example
        if env_example.exists():
            self.validate_env_example(env_example, server_dir.name)
        
        # Check for .env file (should not be committed)
        if (server_dir / ".env").exists():
            self.errors.append(
                f"  ❌ {server_dir.name}: .env file should not be committed"
            )
    
    def validate_server_py(self, server_file: Path, server_name: str):
        """Validate server.py is valid Python."""
        try:
            content = server_file.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(
                f"  ❌ Cannot read {server_name}/server.py: {e}"
            )
            return
        
        # Check Python syntax
        try:
            ast.parse(content)
        except SyntaxError as e:
            self.errors.append(
                f"  ❌ {server_name}/server.py: Syntax error on line {e.lineno}"
            )
            return
        
        # Check for MCP imports
        required_imports = ["mcp.server", "asyncio"]
        for imp in required_imports:
            if imp not in content:
                self.warnings.append(
                    f"  ⚠️  {server_name}/server.py: Missing '{imp}' import"
                )
        
        # Check for basic MCP structure
        if "Server(" not in content:
            self.errors.append(
                f"  ❌ {server_name}/server.py: No Server instance found"
            )
        
        if "@app.list_tools()" not in content and "@server.list_tools()" not in content:
            self.warnings.append(
                f"  ⚠️  {server_name}/server.py: No list_tools() handler found"
            )
        
        if "@app.call_tool()" not in content and "@server.call_tool()" not in content:
            self.warnings.append(
                f"  ⚠️  {server_name}/server.py: No call_tool() handler found"
            )
        
        # Check for sensitive data
        self.check_sensitive_data(content, server_name, "server.py")
        
        # Check for hardcoded credentials
        if re.search(r'(api[_-]?key|password|token|secret)\s*=\s*["\'][^"\']+["\']', 
                    content, re.IGNORECASE):
            self.errors.append(
                f"  ❌ {server_name}/server.py: Possible hardcoded credentials"
            )
    
    def validate_requirements(self, req_file: Path, server_name: str):
        """Validate requirements.txt format."""
        try:
            content = req_file.read_text(encoding='utf-8')
        except Exception as e:
            self.warnings.append(
                f"  ⚠️  Cannot read {server_name}/requirements.txt: {e}"
            )
            return
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Check for mcp package
        has_mcp = any('mcp' in line.lower() for line in lines)
        if not has_mcp:
            self.warnings.append(
                f"  ⚠️  {server_name}: requirements.txt should include 'mcp'"
            )
        
        # Check format (basic validation)
        for line in lines:
            if line.startswith('#'):
                continue
            # Basic package name validation
            if not re.match(r'^[a-zA-Z0-9_-]+([<>=!]=?[0-9.]+)?$', line):
                self.warnings.append(
                    f"  ⚠️  {server_name}: Unusual format in requirements.txt: {line}"
                )
    
    def validate_env_example(self, env_file: Path, server_name: str):
        """Validate .env.example format."""
        try:
            content = env_file.read_text(encoding='utf-8')
        except Exception as e:
            self.warnings.append(
                f"  ⚠️  Cannot read {server_name}/.env.example: {e}"
            )
            return
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Check format
        for line in lines:
            if line.startswith('#'):
                continue
            if '=' not in line:
                self.warnings.append(
                    f"  ⚠️  {server_name}/.env.example: Line missing '=': {line}"
                )
        
        # Check for actual values (should be placeholders)
        sensitive_patterns = [
            (r'[a-f0-9]{32,}', "API key-like value"),
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI key-like value"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub token-like value"),
        ]
        
        for pattern, name in sensitive_patterns:
            if re.search(pattern, content):
                self.errors.append(
                    f"  ❌ {server_name}/.env.example: Contains {name}"
                )
    
    def check_sensitive_data(self, content: str, server_name: str, filename: str):
        """Check for potentially sensitive data."""
        # More specific patterns than in skills validator
        if re.search(r'["\'][a-zA-Z0-9]{32,}["\']', content):
            # Could be an API key
            self.warnings.append(
                f"  ⚠️  {server_name}/{filename}: Long alphanumeric string found (potential credential)"
            )
    
    def print_results(self):
        """Print validation results."""
        print("\n" + "="*60)
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(error)
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(warning)
        
        if not self.errors and not self.warnings:
            print("\n✅ All MCP servers validated successfully!")
        elif not self.errors:
            print("\n✅ No errors found (warnings present)")
        else:
            print("\n❌ Validation failed")
        
        print("="*60 + "\n")

def main():
    """Main entry point."""
    # Find repository root
    current_dir = Path.cwd()
    
    # Try to find mcps directory
    mcps_paths = [
        current_dir / "mcps" / "servers",
        current_dir.parent / "mcps" / "servers",
        Path(__file__).parent.parent / "mcps" / "servers",
    ]
    
    mcps_dir = None
    for path in mcps_paths:
        if path.exists():
            mcps_dir = path
            break
    
    if not mcps_dir:
        print("❌ Could not find mcps/servers directory")
        print("   Run this script from the repository root or tests/ directory")
        return 1
    
    validator = MCPValidator(mcps_dir)
    success = validator.validate_all()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
