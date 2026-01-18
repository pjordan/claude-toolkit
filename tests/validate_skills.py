#!/usr/bin/env python3
"""
Validate skills in the claude-toolkit repository.

This script checks:
- Directory structure
- Required files exist
- SKILL.md follows template structure
- README.md is present and formatted
- No sensitive data in files
"""

import os
import sys
from pathlib import Path
import re

class SkillValidator:
    def __init__(self, skills_dir="skills/examples"):
        self.skills_dir = Path(skills_dir)
        self.errors = []
        self.warnings = []
        
    def validate_all(self):
        """Validate all skills in the examples directory."""
        print("🔍 Validating skills...\n")
        
        if not self.skills_dir.exists():
            self.errors.append(f"Skills directory not found: {self.skills_dir}")
            return False
        
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir()]
        
        if not skill_dirs:
            self.warnings.append("No skills found to validate")
            return True
        
        for skill_dir in skill_dirs:
            print(f"Validating: {skill_dir.name}")
            self.validate_skill(skill_dir)
        
        self.print_results()
        return len(self.errors) == 0
    
    def validate_skill(self, skill_dir: Path):
        """Validate a single skill directory."""
        # Check required files
        skill_md = skill_dir / "SKILL.md"
        readme_md = skill_dir / "README.md"
        
        if not skill_md.exists():
            self.errors.append(f"  ❌ Missing SKILL.md in {skill_dir.name}")
            return
        
        if not readme_md.exists():
            self.warnings.append(f"  ⚠️  Missing README.md in {skill_dir.name}")
        
        # Validate SKILL.md content
        self.validate_skill_content(skill_md, skill_dir.name)
        
        # Validate README.md if present
        if readme_md.exists():
            self.validate_readme(readme_md, skill_dir.name)
    
    def validate_skill_content(self, skill_file: Path, skill_name: str):
        """Validate SKILL.md structure and content."""
        try:
            content = skill_file.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"  ❌ Cannot read {skill_name}/SKILL.md: {e}")
            return
        
        # Check for required sections
        required_sections = [
            "overview",
            "when to use",
            "instructions",
            "examples",
        ]
        
        content_lower = content.lower()
        
        for section in required_sections:
            if section not in content_lower:
                self.warnings.append(
                    f"  ⚠️  {skill_name}: Missing '{section}' section"
                )
        
        # Check for at least one example
        example_pattern = r'###?\s+example'
        if not re.search(example_pattern, content, re.IGNORECASE):
            self.warnings.append(
                f"  ⚠️  {skill_name}: No examples found"
            )
        
        # Check for sensitive data patterns
        self.check_sensitive_data(content, skill_name, "SKILL.md")
        
        # Validate length (should be substantial)
        if len(content) < 500:
            self.warnings.append(
                f"  ⚠️  {skill_name}: SKILL.md seems too short ({len(content)} chars)"
            )
    
    def validate_readme(self, readme_file: Path, skill_name: str):
        """Validate README.md content."""
        try:
            content = readme_file.read_text(encoding='utf-8')
        except Exception as e:
            self.warnings.append(f"  ⚠️  Cannot read {skill_name}/README.md: {e}")
            return
        
        # Check for basic content
        if len(content) < 100:
            self.warnings.append(
                f"  ⚠️  {skill_name}: README.md seems too short"
            )
        
        # Check for link to SKILL.md
        if "SKILL.md" not in content:
            self.warnings.append(
                f"  ⚠️  {skill_name}: README should link to SKILL.md"
            )
    
    def check_sensitive_data(self, content: str, skill_name: str, filename: str):
        """Check for potentially sensitive data."""
        sensitive_patterns = {
            "API Key": r'api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
            "Password": r'password["\']?\s*[:=]\s*["\']?[^"\'\s]{8,}',
            "Token": r'token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
            "Secret": r'secret["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
        }
        
        for name, pattern in sensitive_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                self.errors.append(
                    f"  ❌ {skill_name}/{filename}: Potential {name} found"
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
            print("\n✅ All skills validated successfully!")
        elif not self.errors:
            print("\n✅ No errors found (warnings present)")
        else:
            print("\n❌ Validation failed")
        
        print("="*60 + "\n")

def main():
    """Main entry point."""
    # Find repository root
    current_dir = Path.cwd()
    
    # Try to find skills directory
    skills_paths = [
        current_dir / "skills" / "examples",
        current_dir.parent / "skills" / "examples",
        Path(__file__).parent.parent / "skills" / "examples",
    ]
    
    skills_dir = None
    for path in skills_paths:
        if path.exists():
            skills_dir = path
            break
    
    if not skills_dir:
        print("❌ Could not find skills/examples directory")
        print("   Run this script from the repository root or tests/ directory")
        return 1
    
    validator = SkillValidator(skills_dir)
    success = validator.validate_all()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
