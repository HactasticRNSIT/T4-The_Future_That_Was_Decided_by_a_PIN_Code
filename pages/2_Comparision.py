import streamlit as st
import matplotlib.pyplot as plt
from data.districts import district_data

st.title("⚖️ District Comparison")

d1 = st.selectbox("District 1", list(district_data.keys()))
d2 = st.selectbox("District 2", list(district_data.keys()))

def risk(data):
    r = 0
    if data["aqi"] > 150:
        r += 30
    if data["temp"] > 38:
        r += 30
    if "traffic pollution" in data["risk_factors"]:
        r += 20
    return min(r, 100)

c1 = district_data[d1]
c2 = district_data[d2]

r1 = risk(c1)
r2 = risk(c2)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {d1}")
    st.metric("Risk Score", r1)

with col2:
    st.markdown(f"### {d2}")
    st.metric("Risk Score", r2)

st.markdown("---")

st.markdown("## 📊 Comparison Chart")

fig, ax = plt.subplots()
ax.bar([d1, d2], [r1, r2])
st.pyplot(fig)