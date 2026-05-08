import streamlit as st
import matplotlib.pyplot as plt
from data.districts import district_data

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
h1, h2 {
    color: #0f172a;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

st.title("📊 District Intelligence Dashboard")

district = st.selectbox("Select District", list(district_data.keys()))
data = district_data[district]

# ---------------- RISK ENGINE ----------------
def risk(data):
    r = 0

    if data["aqi"] > 150:
        r += 30
    elif data["aqi"] > 100:
        r += 20

    if data["temp"] > 38:
        r += 30
    elif data["temp"] > 33:
        r += 15

    if "traffic pollution" in data["risk_factors"]:
        r += 20

    if "industrial pollution" in data["risk_factors"]:
        r += 20

    return min(r, 100)

def education(r):
    if r > 70:
        return "Severe disruption in learning environment"
    elif r > 40:
        return "Moderate education impact"
    return "Low impact"

def explain(data, r):
    reasons = []

    if data["aqi"] > 120:
        reasons.append("Air pollution affecting children health")

    if data["temp"] > 38:
        reasons.append("Extreme heat reduces school attendance")

    if "traffic pollution" in data["risk_factors"]:
        reasons.append("Transport emissions increase exposure")

    if r > 70:
        reasons.append("Combined environmental stress is critical")

    return reasons

# ---------------- CALC ----------------
score = risk(data)

# ---------------- CARDS ----------------
st.markdown("## 📌 Key Metrics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("AQI", data["aqi"])

with c2:
    st.metric("Temperature", f'{data["temp"]}°C')

with c3:
    st.metric("Risk Score", score)

st.markdown("---")

# ---------------- RISK FACTORS ----------------
st.markdown("## ⚠ Risk Factors")

for r in data["risk_factors"]:
    st.write("✔", r)

st.markdown("---")

# ---------------- EXPLANATION ----------------
st.markdown("## 🧠 Why this risk?")

for r in explain(data, score):
    st.write("•", r)

st.success(education(score))

st.markdown("---")

# ---------------- CHART ----------------
st.markdown("## 📊 Risk Overview")

districts = list(district_data.keys())
values = []

for d in districts:
    values.append(risk(district_data[d]))

fig, ax = plt.subplots()
ax.bar(districts, values)
plt.xticks(rotation=90)

st.pyplot(fig)