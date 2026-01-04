import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="AI 資產配置", layout="wide")

st.title("📊 AI 智能權重建議")

with st.sidebar:
    st.header("參數設定")
    age = st.slider("您的年齡", 18, 80, 30)
    risk = st.select_slider("風險承受度", options=["保守", "穩健", "平衡", "積極", "極進取"])
    monthly_save = st.number_input("每月預計投入 (TWD)", 1000, 100000, 10000)

# 邏輯計算
def calculate_logic(risk):
    mapping = {
        "保守": {"0050.TW": 0.2, "0056.TW": 0.4, "BND": 0.4},
        "穩健": {"0050.TW": 0.4, "0056.TW": 0.3, "BND": 0.3},
        "平衡": {"0050.TW": 0.5, "0056.TW": 0.2, "VT": 0.2, "BND": 0.1},
        "積極": {"0050.TW": 0.6, "VT": 0.3, "BND": 0.1},
        "極進取": {"0050.TW": 0.4, "VT": 0.4, "TSLA": 0.2} # 增加波動標的
    }
    return mapping.get(risk, mapping["平衡"])

allocation = calculate_logic(risk)

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"### 基於 {age} 歲的建議配置")
    for t, w in allocation.items():
        st.write(f"- **{t}**: `{w*100:.0f}%`")
    st.success(f"建議每月定期定額：{monthly_save:,.0f} 元")

with col2:
    fig = go.Figure(data=[go.Pie(labels=list(allocation.keys()), values=list(allocation.values()), hole=.3)])
    fig.update_layout(title_text="資產分布比例", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
