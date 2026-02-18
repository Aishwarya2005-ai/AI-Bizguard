import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="BizGuard AI", layout="wide")

# ---------------- CUSTOM LIGHT SaaS STYLE ----------------
st.markdown("""
<style>

/* App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #f8fafc, #eef2f7);
}

/* Top Navbar */
.navbar {
    background-color: white;
    padding: 20px 40px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

/* Card */
.card {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
    margin-bottom: 30px;
}

/* Section Title */
.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #1e293b;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    height: 3em;
    width: 250px;
    display: block;
    margin: 0 auto;
}

.stButton>button:hover {
    transform: scale(1.05);
    transition: 0.3s ease;
}

/* Metric Styling */
[data-testid="metric-container"] {
    background-color: #f1f5f9;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
    <h2 style="color:#2563eb;">🛡️ BizGuard AI</h2>
    <p style="color:#64748b;">AI-Powered Business Risk Intelligence System</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📥 Enter Business Data</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    revenue = st.number_input("Monthly Revenue (₹)", min_value=0.0)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0)

with col2:
    loan = st.number_input("Outstanding Loan (₹)", min_value=0.0)
    growth = st.slider("Customer Growth Rate (%)", -50, 50, 0)

competition = st.selectbox("Competition Level", ["Low", "Medium", "High"])

st.markdown("<br>", unsafe_allow_html=True)
analyze = st.button("🚀 Analyze Risk")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze:

    if revenue == 0:
        st.error("Revenue cannot be zero.")
        st.stop()

    risk_score = 0
    breakdown = {}

    if expenses > 0.8 * revenue:
        risk_score += 2
        breakdown["Expense Burden"] = 25
    if loan > revenue:
        risk_score += 2
        breakdown["Debt Stress"] = 30
    if growth < 0:
        risk_score += 2
        breakdown["Negative Growth"] = 20
    if competition == "High":
        risk_score += 2
        breakdown["High Market Competition"] = 25
    elif competition == "Medium":
        risk_score += 1
        breakdown["Moderate Competition"] = 15

    risk_percentage = (risk_score / 8) * 100
    expense_ratio = (expenses / revenue) * 100

    if risk_score <= 2:
        risk_level = "🟢 Low Risk"
        message = "Business appears financially stable."
    elif risk_score <= 5:
        risk_level = "🟡 Moderate Risk"
        message = "Strategic improvements recommended."
    else:
        risk_level = "🔴 High Risk"
        message = "Immediate action required."

    # ---------------- RESULT CARD ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Risk Dashboard</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Risk Score", risk_score)
        st.metric("Risk Probability", f"{risk_percentage:.2f}%")

    with col4:
        st.metric("Risk Level", risk_level)
        st.metric("Expense Ratio", f"{expense_ratio:.2f}%")

    st.progress(int(risk_percentage))
    st.markdown(f"### {message}")

    st.markdown("---")

    # -------- Risk Breakdown (NEW) --------
    st.subheader("🔍 AI Risk Factor Contribution")
    if breakdown:
        breakdown_df = pd.DataFrame({
            "Risk Factor": breakdown.keys(),
            "Impact (%)": breakdown.values()
        })
        st.bar_chart(breakdown_df.set_index("Risk Factor"))
    else:
        st.write("No major risk contributors detected.")

    st.markdown("---")

    # -------- 3 Month Forecast (NEW) --------
    st.subheader("📈 3-Month Financial Projection")

    projected_revenue = []
    current_revenue = revenue

    for i in range(3):
        current_revenue = current_revenue * (1 + growth / 100)
        projected_revenue.append(current_revenue)

    forecast_df = pd.DataFrame({
        "Month": ["Month 1", "Month 2", "Month 3"],
        "Projected Revenue": projected_revenue
    })

    st.line_chart(forecast_df.set_index("Month"))

    st.markdown("---")

    # -------- What-If Simulation (NEW) --------
    st.subheader("🧠 What-If Simulation Mode")

    improved_expense = expenses * 0.9
    improved_risk_score = risk_score

    if improved_expense <= 0.8 * revenue:
        improved_risk_score = max(risk_score - 2, 0)

    improved_percentage = (improved_risk_score / 8) * 100

    st.write("If expenses reduce by 10%:")
    st.metric("New Risk Probability", f"{improved_percentage:.2f}%")

    st.markdown("---")

    # -------- Original Chart --------
    chart_data = pd.DataFrame({
        "Category": ["Risk", "Safe Zone"],
        "Percentage": [risk_percentage, 100 - risk_percentage]
    })

    st.bar_chart(chart_data.set_index("Category"))

    st.markdown('</div>', unsafe_allow_html=True)

    st.success("✔ AI Analysis Complete")

    st.markdown("---")

st.markdown(
    "<center><small>© 2026 BizGuard AI | Designed & Developed by <b>Aishwarya S (ENGINEERING STUDENT@ TOCE)</b></small></center>",
    unsafe_allow_html=True
)