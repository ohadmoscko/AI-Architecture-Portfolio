# AI Architecture Portfolio: Cognitive Systems & Governance

##  Overview
This repository demonstrates advanced **Agentic Design Patterns** tailored for enterprise reliability and economic efficiency. Unlike standard chatbot wrappers, these modules implement **deterministic guardrails**, **self-healing loops**, and **financial circuit breakers**.

##  Modules

### 1. The Reflection Engine ('reflection_agent.py')
A self-correcting agentic loop based on the **Generator-Critic** architecture.
* **Problem:** LLMs often hallucinate or ignore strict formatting compliance instructions.
* **Solution:** A 'Sandwich Architecture' where a Critic Agent evaluates outputs against a strict rubric before showing them to the user.
* **Key Feature:** Implements **Compliance Override Logic**the agent prioritizes enterprise standards (e.g., mandatory Headers) over user preferences ('no text').

### 2. The Cascade Router ('cascade_router.py')
A FinOps-oriented orchestration layer for managing inference costs.
* **Problem:** Routing simple queries to expensive models destroys unit economics.
* **Solution:** A logic gate that classifies query complexity and routes traffic to the most cost-effective tier (Gemini Flash vs. Pro).
* **Key Feature:** **Token Budget Circuit Breaker**a hard-stop mechanism that halts execution if session costs exceed defined limits, preventing 'runaway' API bills.

##  How to Run the Live Dashboard
This project includes a Streamlit control plane to visualize the agentic reasoning.

1. Install dependencies:
   pip install google-genai python-dotenv streamlit

2. Set up your '.env' file with 'GOOGLE_API_KEY'.
3. Launch the dashboard:
   streamlit run dashboard.py

##  Tech Stack
* **Orchestration:** Python (Deterministic State Machines)
* **Models:** Google Gemini 2.5 Flash (via 'google-genai' SDK)
* **Interface:** Streamlit
