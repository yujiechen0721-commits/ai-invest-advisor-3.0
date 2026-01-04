import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.title("📊 投資組合 20 年複利模擬")

age = st.slider("年齡", 20, 60, 30)
monthly = st.number_input("每月投入", 1000, 50000, 5000, 1000)
risk = st.selectbox("風險偏好", ["保守", "中性", "積極"])

def allocation(risk):
    base = {"0050.TW":0.4, "0056.TW":0.3, "VT":0.2, "BND":0.1}
    if risk == "保守":
        base["BND"] += 0.2
    elif risk == "積極":
        base["VT"] += 0.2
    return base

if st.button("🚀 開始模擬"):
    alloc = allocation(risk)
    returns = []

    for t, w in alloc.items():
        data = yf.download(t, period="10y", progress=False)
        if not data.empty:
            r = data["Adj Close"].pct_change().mean()
            returns.append(r * w)

    monthly_r = sum(returns)
    value = 0
    values = []

    for i in range(240):
        value = value * (1 + monthly_r) + monthly
        if i % 12 == 0:
            values.append(value)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(21)),
        y=values,
        mode="lines+markers",
        name="AI 投資組合"
    ))

    fig.update_layout(
        title="20 年資產成長模擬",
        xaxis_title="年",
        yaxis_title="資產總額",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"💰 預估最終資產：{values[-1]:,.0f} 元")
