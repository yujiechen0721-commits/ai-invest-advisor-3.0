import streamlit as st

st.set_page_config(
    page_title="AI 投資小秘書",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI 投資小秘書")
st.subheader("你的個人化智能投資助理")

st.markdown("----")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("你的年齡", 20, 65, 30)
with col2:
    monthly = st.number_input("每月可投資金額（元）", 1000, 100000, 10000, step=1000)
with col3:
    risk = st.selectbox("風險偏好", ["保守", "中性", "積極"])

st.markdown("### 📌 AI 分析結果")

profile = {
    "保守": "穩定現金流 + 抗波動資產",
    "中性": "成長與穩定並重",
    "積極": "追求長期資本增值"
}

st.info(f"""
**投資者輪廓**
- 年齡：{age} 歲  
- 風險屬性：{risk}  
- 投資風格：{profile[risk]}
""")

st.success("👉 請使用左側選單，查看完整投資模擬與分析")
