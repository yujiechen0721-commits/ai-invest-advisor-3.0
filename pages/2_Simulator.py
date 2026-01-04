import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="複利實驗室", layout="wide")

st.title("🧪 複利模擬實驗室")

# 假設從前一頁獲取或設定預設
monthly_save = 10000
allocation = {"0050.TW": 0.6, "VT": 0.4}

@st.cache_data(ttl=3600)
def get_historical_data(tickers):
    # 抓取過去 10 年數據
    data = yf.download(list(tickers.keys()), period="10y", progress=False)['Adj Close']
    return data

data = get_historical_data(allocation)

# 模擬複利 (10年)
st.write("### 歷史績效回測模擬 (假設每月投入)")
returns = data.pct_change().mean()
portfolio_return = sum(returns[t] * w for t, w in allocation.items())

# 計算 120 個月的成長
values = []
current_val = 0
for i in range(120):
    current_val = (current_val + monthly_save) * (1 + portfolio_return)
    values.append(current_val)

fig = go.Figure()
fig.add_trace(go.Scatter(y=values, mode='lines', name='AI 投資組合', line=dict(color='#00ff88', width=3)))
fig.update_layout(title="十年複利成長曲線 (預估)", template="plotly_dark", xaxis_title="月份", yaxis_title="資產總值")
st.plotly_chart(fig, use_container_width=True)

st.metric("十年後預估總資產", f"${values[-1]:,.0f}")
