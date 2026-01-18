import os
import time

class TokenBudgetManager:
    def __init__(self, limit=0.05):
        self.limit = limit
        self.current_spend = 0.0
        self.is_active = True

    def check_and_charge(self, estimated_cost):
        # Implementation of the "Token Budget Circuit Breaker" logic [cite: 72]
        if not self.is_active:
             raise Exception("CIRCUIT BREAKER: System halted due to previous violation.")

        if self.current_spend + estimated_cost > self.limit:
            self.is_active = False
            # Stops execution to prevent "Rabbit Hole" infinite loops 
            raise Exception(f"CIRCUIT BREAKER TRIPPED: Budget Exceeded. Limit: ${self.limit}, Current: ${self.current_spend}")
        
        self.current_spend += estimated_cost
        return True

    def get_status(self):
        return f"${self.current_spend:.4f} / ${self.limit:.4f}"

class CascadeRouter:
    def __init__(self, budget_manager):
        self.budget = budget_manager
        # Pricing based on the Cascade Model arbitrage strategy 
        self.prices = {
            "FAST_TIER": 0.002, 
            "REASONING_TIER": 0.02 
        }

    def route_request(self, user_query):
        print(f"\n--- Processing Query: '{user_query}' ---")
        
        # Simple heuristic to determine complexity
        complexity = "HIGH" if len(user_query) > 20 else "LOW"
        
        try:
            if complexity == "LOW":
                cost = self.prices["FAST_TIER"]
                self.budget.check_and_charge(cost)
                print(f"✅ Routing to FAST TIER (Gemini Flash). Est Cost: ${cost}")
                return "Fast response generated."
            
            else:
                cost = self.prices["REASONING_TIER"]
                self.budget.check_and_charge(cost)
                print(f"🧠 Routing to REASONING TIER (Claude/Pro). Est Cost: ${cost}")
                return "Deep reasoning response generated."

        except Exception as e:
            print(f"🛑 STOP: {str(e)}")
            return None

if __name__ == "__main__":
    manager = TokenBudgetManager(limit=0.05)
    router = CascadeRouter(manager)

    tasks = [
        "Hi there",                      
        "What is 2+2?",                  
        "Explain quantum gravity theory",
        "Write a poem about rust",       
        "Analyze this financial report", 
    ]

    for task in tasks:
        router.route_request(task)
        print(f"Budget Status: {manager.get_status()}")
        time.sleep(0.5)