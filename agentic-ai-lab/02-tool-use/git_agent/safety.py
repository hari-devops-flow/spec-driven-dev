import os
from typing import List
from .config import Config

class SafetyGuard:
    def __init__(self, config: Config):
        # Store allowed paths as absolute paths
        self.allowed_paths = [os.path.abspath(r.path) for r in config.repositories]

    def validate_repo(self, path: str) -> bool:
        """
        Ensures the target repository is in the allowlist and is a valid git repo.
        """
        abs_path = os.path.abspath(path)
        
        # 1. Check Allowlist
        is_allowed = False
        for allowed in self.allowed_paths:
            if abs_path == allowed or abs_path.startswith(allowed + os.sep):
                is_allowed = True
                break
        
        if not is_allowed:
            print(f"[SECURITY] REJECTED: {abs_path} is NOT in allowed_paths.")
            return False
            
        # 2. Check Git validity
        if not os.path.isdir(os.path.join(abs_path, ".git")):
            print(f"[SECURITY] REJECTED: {abs_path} is not a valid git repository.")
            return False
            
        return True
