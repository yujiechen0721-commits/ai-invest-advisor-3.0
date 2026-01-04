import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("🔍 ETF 與指數分析中心")

ticker = st.selectbox("選擇標的", ["0050.TW", "0056.TW", "VT", "BND", "^TWII"])

data = yf.download(ticker, period="5y", progress=False)

st.subheader("📈 價格走勢")
fig = px.line(data, y="Adj Close", title=f"{ticker} 價格變化")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 年化波動率")
vol = data["Adj Close"].pct_change().std() * (252**0.5)
st.metric("波動率", f"{vol:.2%}")
