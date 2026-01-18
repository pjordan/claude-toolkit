#!/usr/bin/env python3
"""
Script to scaffold a new A2A agent project.

Usage:
    python create_agent.py <agent-name> [--type basic|advanced] [--path <output-path>]
"""
import argparse
import os
import shutil
from pathlib import Path


def create_agent(agent_name: str, agent_type: str, output_path: str):
    """Create a new agent from template."""

    # Determine template path
    skill_dir = Path(__file__).parent.parent
    template_path = skill_dir / "assets" / f"{agent_type}-agent"

    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return False

    # Create output directory
    agent_path = Path(output_path) / agent_name
    if agent_path.exists():
        print(f"❌ Error: Directory already exists at {agent_path}")
        return False

    # Copy template
    try:
        shutil.copytree(template_path, agent_path)
        print(f"✅ Created agent: {agent_name}")
        print(f"   Location: {agent_path}")
        print(f"   Type: {agent_type}")
        print()
        print("Next steps:")
        print(f"1. cd {agent_path}")
        print("2. pip install -r requirements.txt")
        print("3. python main.py")
        print()
        print(f"📄 Edit main.py to customize your agent")

        return True

    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Create a new A2A agent from template"
    )
    parser.add_argument(
        "agent_name",
        help="Name of the agent to create"
    )
    parser.add_argument(
        "--type",
        choices=["basic", "advanced"],
        default="basic",
        help="Type of agent template (default: basic)"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Output path (default: current directory)"
    )

    args = parser.parse_args()

    success = create_agent(args.agent_name, args.type, args.path)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
