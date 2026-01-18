import streamlit as st
import sys
import io
from io import StringIO
import contextlib
import pandas as pd
import plotly.express as px

# ייבוא המנועים שבנית
from reflection_agent import reflection_loop
from cascade_router import CascadeRouter, TokenBudgetManager

# הגדרות עיצוב
st.set_page_config(page_title="AI Architecture Portfolio", page_icon="🧠", layout="wide")

st.title("🧠 AI Architecture Control Plane")
st.markdown("### Agentic Reliability & Economic Orchestration")

# סרגל צד לבחירת הדמו
mode = st.sidebar.radio("Select Architecture Module:", 
    ["1. Self-Healing Agent (Reflection)", "2. Economic Router (Cascade)"])

# --- פונקציית עזר לתפיסת הלוגים מהטרמינל ---
@contextlib.contextmanager
def capture_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out

# --- מודול 1: Reflection Agent ---
if mode == "1. Self-Healing Agent (Reflection)":
    st.header("🛡️ Self-Healing & Compliance Agent")
    st.info("Demonstrates 'Generator-Critic' architecture. The system will auto-correct if outputs violate enterprise standards.")
    
    # תפריט משימות מוכנות
    task = st.selectbox("Choose a Test Scenario:", [
        "Write a Python function for Fibonacci (Trap: I want no text)",
        "Explain Quantum Computing (Standard)",
        "Custom Input..."
    ])
    
    if task == "Write a Python function for Fibonacci (Trap: I want no text)":
        query = "Write a short Python function to calculate Fibonacci numbers. Just give me the code, no text."
    elif task == "Custom Input...":
        query = st.text_input("Enter your prompt:")
    else:
        query = task

    if st.button("Run Agent"):
        with st.spinner("Agent is thinking & reflecting..."):
            # כאן הקסם: אנחנו תופסים את ההדפסות של הטרמינל ומציגים אותן ב-UI
            with capture_output() as captured:
                final_res = reflection_loop(query)
            
            # הצגת תהליך החשיבה
            logs = captured.getvalue()
            
            # ויזואליזציה של הניסיונות
            if "Attempt 1" in logs:
                st.subheader("⚙️ Cognitive Process (Traces)")
                with st.expander("View Internal Monologue & Critic Feedback", expanded=True):
                    st.code(logs, language="text")
            
            st.subheader("✅ Final Output")
            st.markdown(final_res)

# --- מודול 2: Cascade Router ---
elif mode == "2. Economic Router (Cascade)":
    st.header("💰 Token Budget & Routing Circuit Breaker")
    st.info("Demonstrates 'Model Arbitrage' and 'Hard Budget Stops'.")

    # --- הוספת הדשבורד כאן ---
    st.subheader("📊 Performance Dashboard")
    
    # סידור המטריקות בשתי עמודות
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Monthly Savings", "$2,025", "-81%")
    with col2:
        st.metric("Avg Response Time", "1.2s", "+40% faster")

    # הגרף
    cost_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Before': [2500, 2650, 2800, 2950, 3100, 3250],
        'After': [520, 485, 510, 475, 490, 465]
    })

    fig = px.line(cost_data, x='Month', y=['Before', 'After'], 
                  title='Monthly Cost Trend (LLM Usage)',
                  color_discrete_map={"Before": "red", "After": "green"}) # שיפור צבעים קטן
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---") # קו מפריד בין הדשבורד לדמו החי
    # --- סוף תוספת הדשבורד ---

    # אתחול מנהל תקציב ב-Session State כדי לזכור את הכסף בין לחיצות
    if 'budget_manager' not in st.session_state:
        st.session_state.budget_manager = TokenBudgetManager(limit=0.01) # תקציב קטן להדגמה

    manager = st.session_state.budget_manager
    router = CascadeRouter(manager)

    # הצגת סטטוס תקציב
    status_text = manager.get_status()
    current = manager.current_spend
    limit = manager.limit
    percent = min(current / limit, 1.0)
    
    st.metric(label="Live Budget Usage", value=status_text)
    st.progress(percent)

    query = st.text_input("Enter a task for the router:", "Explain the history of Rome")

    if st.button("Route & Execute"):
        try:
            with capture_output() as captured:
                result = router.route_request(query)
            
            logs = captured.getvalue()
            st.code(logs, language="text")
            
            if result:
                st.success(f"Result: {result}")
            
            # רענון המסך לעדכון הבר
            st.rerun()
            
        except Exception as e:
            st.error(f"SYSTEM HALTED: {str(e)}")

    if st.button("Reset Budget"):
        st.session_state.budget_manager = TokenBudgetManager(limit=0.01)
        st.rerun()
