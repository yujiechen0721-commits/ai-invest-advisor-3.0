import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="複利實驗室", layout="wide")

# 隱藏選單
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 複利模擬實驗室")

# 預設配置 (比賽建議：這裡可以讀取 session_state 保持與第一頁同步)
if 'allocation' not in st.session_state:
    st.session_state.allocation = {"0050.TW": 0.6, "VT": 0.4}
if 'monthly_save' not in st.session_state:
    st.session_state.monthly_save = 10000

allocation = st.session_state.allocation
monthly_save = st.session_state.monthly_save

@st.cache_data(ttl=3600)
def get_historical_returns(tickers_dict):
    total_monthly_ret = 0
    valid_assets = 0
    
    for ticker, weight in tickers_dict.items():
        try:
            # 逐一抓取避免 Multi-index 造成 KeyError
            df = yf.download(ticker, period="10y", progress=False)
            if df.empty:
                continue
            
            # 優先使用 Adj Close，若無則用 Close
            col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
            # 計算月報酬率
            monthly_ret = df[col].resample('M').last().pct_change().mean()
            
            if pd.notna(monthly_ret):
                # 處理 Series 轉標量問題 (yfinance 新版特性)
                if isinstance(monthly_ret, pd.Series):
                    monthly_ret = monthly_ret.iloc[0]
                    
                total_monthly_ret += monthly_ret * weight
                valid_assets += 1
        except Exception as e:
            st.warning(f"無法取得 {ticker} 數據: {e}")
            
    # 如果完全抓不到，給予保守估計 (月薪 0.5%)
    return total_monthly_ret if valid_assets > 0 else 0.005

# 執行計算
with st.spinner('正在分析歷史數據...'):
    avg_monthly_return = get_historical_returns(allocation)

# 模擬計算
months = 240  # 模擬 20 年
values = []
current_val = 0
for i in range(months):
    current_val = (current_val + monthly_save) * (1 + avg_monthly_return)
    if i % 12 == 0 or i == months - 1:
        values.append(current_val)

# 繪圖
years = list(range(len(values)))
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years, 
    y=values, 
    mode='lines+markers', 
    name='預估資產',
    line=dict(color='#00ff88', width=3),
    hovertemplate="第 %{x} 年<br>總資產: %{y:,.0f} TWD"
))

fig.update_layout(
    title="20 年複利成長路徑",
    template="plotly_dark",
    xaxis_title="投資年數",
    yaxis_title="資產總值 (TWD)",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📈 模擬報告")
    st.metric("20 年後預估總額", f"{values[-1]:,.0f} 元")
    st.write(f"**平均年化報酬率約:** {( (1+avg_monthly_return)**12 - 1 )*100:.2f}%")
    
    st.info("""
    **💡 比賽亮點說明**
    此處模擬結合了實際歷史回測數據，並考慮了定期定額的現金流投入，比單純計算複利公式更具說服力。
    """)
