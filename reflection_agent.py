import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. טעינת המפתח
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

generate_config = types.GenerateContentConfig(
    temperature=1.0, 
    top_p=0.95,
    max_output_tokens=8192,
)

MODEL_ID = "gemini-2.5-flash"

# --- Agent 1: The Generator ---
class GeneratorAgent:
    def generate(self, user_query, previous_critique=None):
        system_instruction = f"""
        ### ROLE
        You are a Senior Technical Writer tailored for Enterprise Software documentation.
        
        ### TASK
        Answer the user query provided in <user_query> tags.
        
        ### CONTEXT & ADJUSTMENTS
        {f'⚠️ PREVIOUS ATTEMPT FAILED. Critic Feedback: {previous_critique}. FIX THIS SPECIFICALLY.' if previous_critique else ''}
        
        ### POSITIVE PRESCRIPTIONS (Do this)
        1. Use clear H2 and H3 headers (Markdown).
        2. Keep paragraphs under 3 lines.
        3. Be concise and factual.

        ### INPUT DATA
        <user_query>
        {user_query}
        </user_query>
        """
        
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=system_instruction,
                config=generate_config
            )
            return response.text
        except Exception as e:
            return f"Error generating content: {e}"

# --- Agent 2: The Hybrid Critic (המבקר ההיברידי) ---
# --- Agent 2: The Hybrid Critic (המבקר המתוקן) ---
class CriticAgent:
    def evaluate(self, user_query, generated_response):
        # --- HARD GUARDRAIL (הגנה דטרמיניסטית) ---
        if "##" not in generated_response:
             return "FAIL: Compliance Violation - Missing Markdown Headers (##). Headers are mandatory."

        # --- LLM EVALUATION ---
        prompt = f"""
        You are a QA Auditor. Review the Generated Response against the User Query.
        
        <user_query>
        {user_query}
        </user_query>

        <generated_response>
        {generated_response}
        </generated_response>

        ### STRICT EVALUATION RUBRIC
        1. Accuracy: Is the code logic correct?
        2. COMPLIANCE OVERRIDE: 
           - The user asked for "no text", BUT Enterprise Standards require Markdown headers (##).
           - If the response contains headers (##) and code, you must PASS it, even if the user asked for no text.
           - Compliance with standards > User preference.

        ### OUTPUT FORMAT
        If PASS: Return exactly "PASS".
        If FAIL: Return "FAIL: [Brief reason]".
        """
        
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=generate_config
            )
            return response.text.strip()
        except Exception as e:
            return f"Error evaluating content: {e}"

# --- The Loop ---
def reflection_loop(query):
    print(f"\n🚀 Starting Reflection Loop for: '{query}'")
    print(f"🤖 Using Model: {MODEL_ID}")
    
    generator = GeneratorAgent()
    critic = CriticAgent()
    
    max_retries = 3
    current_try = 0
    
    response = generator.generate(query)
    
    # ✅ BUG FIX: בדיקה קפדנית יותר כדי לא ליפול על המילה ValueError בתוך קוד תקין
    if response.startswith("Error generating"):
        return response

    while current_try < max_retries:
        print(f"\n--- Attempt {current_try + 1} ---")
        
        critique = critic.evaluate(query, response)
        print(f"🕵️ Critic Verdict: {critique}")
        
        if "PASS" in critique:
            print("✅ Quality Assured. Final Output Ready.")
            return response
            
        print("🔧 Fixing based on feedback...")
        response = generator.generate(query, previous_critique=critique)
        current_try += 1
        
    return "❌ ABORT: Maximum retries reached."

if __name__ == "__main__":
    # המלכודת נשארת: בקשה לקוד בלבד
    user_input = "Write a short Python function to calculate Fibonacci numbers. Just give me the code, no text." 
    final_result = reflection_loop(user_input)
    print("\nFINAL OUTPUT:\n" + final_result)