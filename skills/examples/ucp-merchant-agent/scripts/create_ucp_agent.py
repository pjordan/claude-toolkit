#!/usr/bin/env python3
"""
UCP Agent Scaffolding Script

Creates a new UCP shopping agent from the basic template.

Usage:
    python create_ucp_agent.py <agent-name> [--path <output-path>]

Example:
    python create_ucp_agent.py my-shopping-agent --path ./agents
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_template_path() -> Path:
    """Get the path to the basic-shopping-agent template."""
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "templates" / "basic-shopping-agent"

    if not template_path.exists():
        print(f"Error: Template not found at {template_path}")
        sys.exit(1)

    return template_path


def validate_agent_name(name: str) -> bool:
    """Validate agent name follows conventions."""
    if not name:
        return False

    # Must start with letter, contain only letters, numbers, hyphens
    if not name[0].isalpha():
        return False

    for char in name:
        if not (char.isalnum() or char == "-"):
            return False

    return True


def create_agent(agent_name: str, output_path: Path) -> Path:
    """
    Create a new agent from template.

    Args:
        agent_name: Name for the new agent
        output_path: Directory to create agent in

    Returns:
        Path to created agent directory
    """
    template_path = get_template_path()
    agent_path = output_path / agent_name

    # Check if already exists
    if agent_path.exists():
        print(f"Error: Directory already exists: {agent_path}")
        sys.exit(1)

    # Create output directory if needed
    output_path.mkdir(parents=True, exist_ok=True)

    # Copy template
    shutil.copytree(template_path, agent_path)

    # Customize files
    customize_agent(agent_path, agent_name)

    return agent_path


def customize_agent(agent_path: Path, agent_name: str):
    """Customize template files for the new agent."""

    # Update main.py title
    main_py = agent_path / "main.py"
    if main_py.exists():
        content = main_py.read_text()
        content = content.replace(
            'title="UCP Shopping Agent"',
            f'title="{agent_name.replace("-", " ").title()}"',
        )
        content = content.replace(
            '"service": "ucp-shopping-agent"',
            f'"service": "{agent_name}"',
        )
        main_py.write_text(content)

    # Create agent profile template
    profile_json = agent_path / "agent-profile.json"
    profile_content = f'''{{
  "ucp": {{
    "version": "2026-01-11",
    "capabilities": [
      {{
        "name": "dev.ucp.shopping.checkout",
        "version": "2026-01-11"
      }}
    ],
    "payment_handlers": [
      "com.google.pay",
      "dev.ucp.ap2"
    ]
  }},
  "agent": {{
    "name": "{agent_name.replace("-", " ").title()}",
    "description": "UCP shopping agent for agentic commerce",
    "contact": "support@example.com"
  }}
}}
'''
    profile_json.write_text(profile_content)

    # Create README for the agent
    readme = agent_path / "README.md"
    readme_content = f"""# {agent_name.replace("-", " ").title()}

A UCP shopping agent for integrating with UCP-compliant merchants.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Host your agent profile:
   - Upload `agent-profile.json` to a public URL
   - Update `AGENT_PROFILE_URL` in `.env`

4. Run the agent:
   ```bash
   python main.py
   ```

5. Test:
   ```bash
   curl http://localhost:8000/health
   ```

## API Endpoints

- `GET /health` - Health check
- `POST /discover` - Discover merchant capabilities
- `POST /checkout/create` - Create checkout session
- `POST /checkout/complete` - Complete checkout with payment

## Configuration

See `.env.example` for configuration options.

## License

MIT
"""
    readme.write_text(readme_content)


def main():
    parser = argparse.ArgumentParser(
        description="Create a new UCP shopping agent from template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s my-shopping-agent
    %(prog)s my-shopping-agent --path ./agents
    %(prog)s grocery-agent --path /opt/agents
        """,
    )

    parser.add_argument(
        "name",
        help="Name for the new agent (e.g., my-shopping-agent)",
    )

    parser.add_argument(
        "--path",
        "-p",
        default=".",
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()

    # Validate name
    if not validate_agent_name(args.name):
        print("Error: Invalid agent name. Use lowercase letters, numbers, and hyphens.")
        print("       Name must start with a letter.")
        sys.exit(1)

    output_path = Path(args.path).resolve()

    print(f"Creating UCP agent: {args.name}")
    print(f"Output path: {output_path}")

    agent_path = create_agent(args.name, output_path)

    print()
    print(f"✅ Agent created successfully at: {agent_path}")
    print()
    print("Next steps:")
    print(f"  1. cd {agent_path}")
    print("  2. pip install -r requirements.txt")
    print("  3. cp .env.example .env")
    print("  4. Edit .env with your configuration")
    print("  5. python main.py")
    print()
    print("For more information, see the README.md in your agent directory.")


if __name__ == "__main__":
    main()
