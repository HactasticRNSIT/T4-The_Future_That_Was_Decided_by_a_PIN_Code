import streamlit as st
import matplotlib.pyplot as plt
from data.districts import district_data

st.set_page_config(layout="wide")

st.title("🌍 Climate Risk Intelligence Dashboard")

# =========================
# RISK ENGINE (UPGRADED)
# =========================
def compute_risk(data):
    risk = 0
    breakdown = {}

    # AQI (Air pollution)
    breakdown["Air Quality"] = min(data["aqi"] / 5, 30)
    risk += breakdown["Air Quality"]

    # Temperature (climate stress)
    temp_score = 0
    if data["temp"] > 38:
        temp_score = 25
    elif data["temp"] > 33:
        temp_score = 15
    breakdown["Temperature"] = temp_score
    risk += temp_score

    # Rainfall (water stress)
    rainfall_score = {
        "Very Low": 20,
        "Low": 15,
        "Moderate": 10,
        "High": 5
    }.get(data["rainfall"], 10)

    breakdown["Water Stress"] = rainfall_score
    risk += rainfall_score

    # Transport impact
    transport_score = 20 if "traffic pollution" in data["risk_factors"] else 5
    breakdown["Transport"] = transport_score
    risk += transport_score

    # Industrial impact
    industrial_score = 20 if "industrial pollution" in data["risk_factors"] else 5
    breakdown["Industry"] = industrial_score
    risk += industrial_score

    # Social/urban pressure (estimated factor)
    social_score = 10
    breakdown["Urban Pressure"] = social_score
    risk += social_score

    return min(risk, 100), breakdown

# =========================
# EDUCATION IMPACT
# =========================
def education_impact(risk):
    if risk >= 75:
        return "🔴 Severe disruption to learning (health + attendance affected)"
    elif risk >= 50:
        return "🟠 Moderate learning disruption"
    return "🟢 Low educational impact"

# =========================
# ACTION SYSTEM (NEW)
# =========================
def action_plan(risk, data):
    actions = []

    if risk >= 75:
        actions.append("Immediate government intervention required")
        actions.append("Install air quality control systems in schools")
        actions.append("Heat safety protocols for students")

    if data["aqi"] > 120:
        actions.append("Reduce traffic emissions near schools")

    if data["temp"] > 38:
        actions.append("Shift school timings to early morning")

    if "industrial pollution" in data["risk_factors"]:
        actions.append("Relocate schools away from industrial zones")

    if not actions:
        actions.append("Maintain monitoring — risk currently manageable")

    return actions

# =========================
# RANK ALL DISTRICTS
# =========================
def rank_districts():
    ranking = []
    for d in district_data:
        r, _ = compute_risk(district_data[d])
        ranking.append((d, r))
    return sorted(ranking, key=lambda x: x[1], reverse=True)

# =========================
# UI INPUT
# =========================
district = st.selectbox("Select District", list(district_data.keys()))
data = district_data[district]

risk, breakdown = compute_risk(data)

# =========================
# TOP KPIs
# =========================
st.markdown("## 📊 Key Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AQI", data["aqi"])

with col2:
    st.metric("Temperature", f'{data["temp"]}°C')

with col3:
    st.metric("Risk Score", risk)

st.markdown("---")

# =========================
# RISK BREAKDOWN
# =========================
st.markdown("## 🧠 Risk Breakdown (What contributes?)")

for k, v in breakdown.items():
    st.write(f"• **{k}** → {round(v,1)} score")

st.markdown("---")

# =========================
# EDUCATION IMPACT
# =========================
st.markdown("## 📚 Education Impact")

st.success(education_impact(risk))

st.markdown("---")

# =========================
# ACTION PLAN
# =========================
st.markdown("## 🚨 Recommended Actions")

for a in action_plan(risk, data):
    st.write("✔", a)

st.markdown("---")

# =========================
# HIGHEST RISK DISTRICT
# =========================
st.markdown("## 🔥 Highest Risk District in Karnataka")

ranking = rank_districts()
top_district, top_risk = ranking[0]

st.error(f"🔴 {top_district} → Risk Score: {top_risk}")

st.markdown("---")

# =========================
# FULL RANKING
# =========================
st.markdown("## 📊 District Risk Ranking")

for d, r in ranking:
    if r >= 75:
        st.error(f"{d} → {r}")
    elif r >= 50:
        st.warning(f"{d} → {r}")
    else:
        st.success(f"{d} → {r}")

st.markdown("---")

# =========================
# CHART
# =========================
st.markdown("## 📈 Visualization")

fig, ax = plt.subplots()
ax.bar([x[0] for x in ranking], [x[1] for x in ranking])
plt.xticks(rotation=90)
ax.set_ylabel("Risk Score")
ax.set_title("District Risk Comparison")

st.pyplot(fig)