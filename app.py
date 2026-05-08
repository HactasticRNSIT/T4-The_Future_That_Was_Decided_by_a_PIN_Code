import streamlit as st

st.set_page_config(
    page_title="Climate Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* App background */
.main {
    background-color: #f5f7fb;
}

/* Sidebar like website menu */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
    font-size: 16px;
}

/* Header */
h1 {
    color: #0f172a;
    font-size: 38px;
}

/* Card look */
.block-container {
    padding-top: 2rem;
}

/* Metrics */
div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🌍 Climate Intelligence Dashboard")
st.markdown("### Real-time District Risk & Education Impact System")

st.markdown("---")

# ---------------- LAYOUT STYLE DASHBOARD ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 Dashboard → View district analysis")

with col2:
    st.info("⚖️ Compare → Compare districts")

with col3:
    st.info("🚨 Risk Engine → AI-based scoring")

st.markdown("---")

st.success("Use the left sidebar to navigate like a real web application")