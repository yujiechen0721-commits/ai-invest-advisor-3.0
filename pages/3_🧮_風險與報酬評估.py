import streamlit as st
import yfinance as yf
import numpy as np

st.title("🧮 投資風險與報酬評估")

ticker = st.selectbox("選擇資產", ["0050.TW", "VT", "BND"])

data = yf.download(ticker, period="10y", progress=False)
ret = data["Adj Close"].pct_change().dropna()

annual_return = ret.mean() * 252
risk = ret.std() * (252 ** 0.5)

st.metric("年化報酬率", f"{annual_return:.2%}")
st.metric("年化風險（波動）", f"{risk:.2%}")

st.info("📌 本頁為簡化版風險報酬分析（Sharpe Ratio 概念）")
