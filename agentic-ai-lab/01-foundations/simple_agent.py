import time
import random

# ==========================================
# 1. The "Environment"
# Code that simulates the external system the agent interacts with.
# ==========================================
class MockServerEnv:
    def __init__(self):
        self.state = "CRITICAL_FAILURE"
        self.logs = [
            "ERROR: Connection refused on port 80",
            "ERROR: Service 'nginx' is not running"
        ]
        
    def observe(self):
        """Returns the current state of the world."""
        return {
            "status": self.state,
            "recent_logs": self.logs[-1] if self.logs else "No logs"
        }

    def execute(self, action: str):
        """Executes a tool/action effectively changing the world."""
        print(f"\n[SYSTEM] Executing: {action}...")
        time.sleep(1) # Simulate latency
        
        if action == "restart_nginx":
            if self.state == "CRITICAL_FAILURE":
                self.state = "RUNNING"
                self.logs.append("INFO: nginx started successfully")
                return "Command executed: Service restarted."
            else:
                return "Service is already running."
        
        elif action == "check_logs":
            return f"Logs: {self.logs}"
            
        elif action == "ask_human":
             return "Human says: 'Did you try turning it off and on again?'"
             
        else:
            return f"Unknown command: {action}"

# ==========================================
# 2. The "Brain" (Mock LLM)
# Simulates intelligence by mapping observations to actions via heuristics.
# In a real agent, this is `client.chat.completions.create(...)`
# ==========================================
def mock_llm_decision(observation, goal):
    """
    Simulates the LLM's 'Thought' process.
    Input: Current Context
    Output: Next Action
    """
    status = observation.get("status")
    
    print(f"\n[BRAIN] Thinking... (Observed: {status})")
    
    # ---------------------------------------------------------
    # This logic block represents what the LLM *learns* to do
    # via the prompt instructions.
    # ---------------------------------------------------------
    if status == "CRITICAL_FAILURE":
        return "THOUGHT: The server is down. I should check logs or restart it. Let's restart it.", "restart_nginx"
    elif status == "RUNNING":
        return "THOUGHT: The server is running. Goal achieved.", "FINISH"
    else:
        return "THOUGHT: I am confused.", "ask_human"

# ==========================================
# 3. The "Agent" (Control Loop)
# The system architecture that binds Brain and Environment.
# ==========================================
class SimpleAgent:
    def __init__(self, env):
        self.env = env
        self.max_steps = 5
        
    def run(self, goal):
        print(f"--- Agent Started. Goal: {goal} ---")
        step = 0
        
        while step < self.max_steps:
            step += 1
            print(f"\n--- Step {step} ---")
            
            # 1. OBSERVE
            # Get data from environment + memory (not implemented yet)
            observation = self.env.observe()
            print(f"[AGENT] Observed: {observation}")
            
            # 2. THINK
            # Send context to LLM to get a decision
            thought, action = mock_llm_decision(observation, goal)
            print(f"[AGENT] Thought: {thought}")
            print(f"[AGENT] Decided Action: {action}")
            
            # 3. CHECK TERMINATION
            if action == "FINISH":
                print("\n[SUCCESS] Goal achieved!")
                return
            
            # 4. ACT
            # Execute the tool
            result = self.env.execute(action)
            print(f"[AGENT] Navigation Result: {result}")
            
            # Loop continues with new observation...
            
        print("\n[FAILURE] Max steps reached without achieving goal.")

# ==========================================
# Main Entrypoint
# ==========================================
if __name__ == "__main__":
    # Initialize the world
    server_env = MockServerEnv()
    
    # Initialize the agent
    agent = SimpleAgent(server_env)
    
    # Run the mission
    agent.run("Fix the HTTP 500 Error")
