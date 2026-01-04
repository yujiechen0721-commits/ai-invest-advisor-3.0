import streamlit as st

st.set_page_config(
    page_title="ZenVest AI | 智慧投資導航",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    h1, h2 { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ZenVest AI 智慧投資平台")
st.subheader("為比賽而生的高階資產配置系統")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### 核心價值
    - **數據驅動**：串接 Yahoo Finance 即時 API。
    - **AI 導引**：根據風險偏好提供專業權重。
    - **視覺化分析**：動態複利曲線與風險對比。
    """)
with col2:
    st.info("💡 **操作指南**：請利用左側導覽列進入「AI 配置」或「模擬實驗室」開始您的投資旅程。")

st.image("https://images.unsplash.com/photo-1611974717482-9825d2f6274a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="專業投資模擬系統")
