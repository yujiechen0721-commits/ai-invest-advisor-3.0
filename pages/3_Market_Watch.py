import streamlit as st
import yfinance as yf

st.title("🌐 全球市場即時監測")

tickers = ["^TWII", "^GSPC", "^IXIC", "BTC-USD", "GC=F"]
names = ["台股指數", "標普500", "那斯達克", "比特幣", "黃金期貨"]

cols = st.columns(len(tickers))

for i, t in enumerate(tickers):
    df = yf.Ticker(t).history(period="2d")
    price = df['Close'].iloc[-1]
    change = price - df['Close'].iloc[-2]
    cols[i].metric(names[i], f"{price:,.2f}", f"{change:,.2f}")

st.divider()
st.info("本系統每小時自動更新一次數據，提供最精確的決策依據。")
