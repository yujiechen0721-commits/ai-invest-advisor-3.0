import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 頁面基本配置 ---
st.set_page_config(page_title="AI 投資小秘書 Pro", layout="wide")

# --- 進階 CSS 樣式：打造頂部導航與專業卡片 ---
st.markdown("""
    <style>
    /* 隱藏側邊欄與預設元件 */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    
    /* 頂部導航列容器 */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 1rem;
        background-color: #0E1117;
        position: sticky;
        top: 0;
        z-index: 999;
        border-bottom: 2px solid #30363D;
        margin-bottom: 2rem;
    }
    
    /* 自定義卡片樣式 */
    .stat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    /* 專業漸層標題 */
    .main-title {
        background: linear-gradient(90deg, #00C853, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部導航邏輯 ---
# 使用 st.session_state 來追蹤當前頁面
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 首頁概覽"

# 建立頂部按鈕列
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1,1,1,1])

with col_nav1:
    if st.button("🏠 首頁概覽", use_container_width=True):
        st.session_state.current_page = "🏠 首頁概覽"
with col_nav2:
    if st.button("🤖 AI 智能配資", use_container_width=True):
        st.session_state.current_page = "🤖 AI 智能配資"
with col_nav3:
    if st.button("📊 即時盤勢", use_container_width=True):
        st.session_state.current_page = "📊 即時盤勢"
with col_nav4:
    if st.button("💡 投資策略庫", use_container_width=True):
        st.session_state.current_page = "💡 投資策略庫"
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 1. 🏠 首頁概覽
# ==========================================
if st.session_state.current_page == "🏠 首頁概覽":
    st.markdown('<p class="main-title">AI 投資小秘書 Pro</p>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #666;'>您專屬的智能資產管理顧問</h4><br>", unsafe_allow_html=True)
    
    # 關鍵指標卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><h3>台股加權</h3><h2 style="color: #00C853;">18,234</h2><p>▲ 1.2%</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>美股 S&P500</h3><h2 style="color: #ff5252;">5,123</h2><p>▼ 0.3%</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>美元/台幣</h3><h2 style="color: #007bff;">31.52</h2><p>-0.01</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><h3>恐懼貪婪</h3><h2 style="color: #ff9800;">65</h2><p>貪婪</p></div>', unsafe_allow_html=True)

    st.write("### 📢 智能盤後快訊")
    st.success("今日 AI 分析：市場情緒維持偏多，半導體產業資金流入明顯。建議維持 60% 持股水位。")

# ==========================================
# 2. 🤖 AI 智能配資
# ==========================================
elif st.session_state.current_page == "🤖 AI 智能配資":
    st.header("🤖 AI 智能資產配置優化")
    
    with st.container():
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            age = st.number_input("您的年齡", 20, 80, 30)
        with c2:
            monthly_save = st.number_input("每月預計投入", 5000, 100000, 10000)
        with c3:
            risk = st.select_slider("風險承擔等級", options=["保守", "穩健", "成長", "積極"])

    if st.button("🚀 生成深度診斷報告"):
        # 模擬分配邏輯
        st.divider()
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            labels = ['0050.TW', 'VT', 'BND', '現金']
            values = [45, 30, 20, 5]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(title="建議資產比例", margin=dict(t=50, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_res2:
            st.markdown("### 📝 AI 診斷分析")
            st.write(f"1. **目標設定**：30 年後退休目標資產可達 **3,500 萬**。")
            st.write("2. **核心策略**：以 0.618 黃金比例分配風險資產。")
            st.write("3. **防禦機制**：配置 20% 高品質債券以應對波動。")
            st.metric("預估年化報酬率", "8.5%", "+1.2%")

# ==========================================
# 3. 📊 即時盤勢
# ==========================================
elif st.session_state.current_page == "📊 即時盤勢":
    st.header("📊 全球市場動態監測")
    ticker = st.text_input("輸入股票代碼 (例: 2330.TW, TSLA, NVDA)", "2330.TW")
    
    try:
        data = yf.download(ticker, period="1y", progress=False)
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'],
                        increasing_line_color= '#FF3333', decreasing_line_color= '#33FF33')])
        fig.update_layout(title=f"{ticker} 走勢分析 (K線圖)", xaxis_rangeslider_visible=False, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # 顯示詳細數據
        with st.expander("查看原始歷史數據"):
            st.dataframe(data.tail(10), use_container_width=True)
    except:
        st.error("代碼錯誤或無法抓取資料")

# ==========================================
# 4. 💡 投資策略庫
# ==========================================
elif st.session_state.current_page == "💡 投資策略庫":
    st.header("💡 專業投資知識庫")
    
    tab1, tab2, tab3 = st.tabs(["🔥 熱門主題", "📖 投資基礎", "🧩 進階技術"])
    
    with tab1:
        st.markdown("""
        - **2024 AI 產業深度解讀**：為何輝達是核心？
        - **高股息陷阱**：如何避開只有配息沒有價差的標的。
        - **台美股連動分析**：費城半導體對台股的影響。
        """)
        
    with tab2:
        st.info("💡 基礎小提醒：定期定額是降低成本風險的最佳方式。")

# --- Footer ---
st.markdown("---")
st.caption("AI 投資小秘書 | 僅供學術研究使用，不代表任何投資建議。")
