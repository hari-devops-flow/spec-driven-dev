import json
import os
from datetime import datetime
from typing import Dict, List, Optional

STATE_FILE = "state.json"

class StateManager:
    def __init__(self, state_file: str = STATE_FILE):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if not os.path.exists(self.state_file):
            return {"history": []}
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"history": []}

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def should_run(self, repo_path: str) -> bool:
        """
        Returns True if the agent has NOT run for this repo today.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        repo_abs = os.path.abspath(repo_path)
        
        for entry in self.state.get("history", []):
            if entry.get("repo") == repo_abs and entry.get("date") == today:
                 # Already ran today
                 return False
        return True

    def record_run(self, repo_path: str, action: str, status: str, details: str = ""):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "repo": os.path.abspath(repo_path),
            "action": action,
            "status": status,
            "details": details
        }
        self.state.setdefault("history", []).append(entry)
        self._save_state()
