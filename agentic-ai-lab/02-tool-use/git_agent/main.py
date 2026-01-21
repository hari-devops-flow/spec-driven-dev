import argparse
import sys
import os

from .config import load_config
from .agent import GitAutoCommitterAgent

def main():
    parser = argparse.ArgumentParser(description="Git Auto-Committer Agent (SDD Implementation)")
    parser.add_argument("--config", default="git-agent.config.yaml", help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without changes (overrides config)")
    parser.add_argument("--execute", action="store_true", help="Execute changes (overrides dry-run)")
    parser.add_argument("--force", action="store_true", help="Force run (ignores 'once daily' rule)")
    
    args = parser.parse_args()
    
    # Resolve Config Path
    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        print(f"[FATAL] Config file not found: {config_path}")
        sys.exit(1)
        
    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"[FATAL] Invalid config: {e}")
        sys.exit(1)
        
    # Determine Execution Mode
    # Strict safety: Default to dry_run unless --execute is passed
    # OR if config defaults to dry_run=False.
    # BUT design spec says: "Dry-Run Default: Unless --execute is passed."
    
    is_dry_run = True
    
    if args.dry_run:
        is_dry_run = True
    elif args.execute:
        is_dry_run = False
    else:
        # Fallback to config default
        is_dry_run = config.settings.dry_run_default
        
    # Safety Net: If user meant to run but didn't pass --execute, and config says dry_run=True,
    # we warn them.
    if is_dry_run:
        print("[INFO] Running in DRY-RUN mode. Use --execute to apply changes.")

    agent = GitAutoCommitterAgent(config, is_dry_run, args.force)
    agent.run()

if __name__ == "__main__":
    main()
