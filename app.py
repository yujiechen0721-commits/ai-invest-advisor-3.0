import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# --- 頁面基本配置 ---
st.set_page_config(page_title="AI 投資小秘書 Pro", layout="wide", initial_sidebar_state="collapsed")

# --- 進階 CSS 樣式 ---
st.markdown("""
    <style>
    /* 隱藏側邊欄 */
    [data-testid="stSidebar"] {display: none;}
    
    /* 整體背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 主容器 */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* 頂部導航列 */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* 卡片樣式升級 */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        text-align: center;
        border: 2px solid rgba(255,255,255,0.8);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    }
    
    .stat-card h3 {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .stat-card h2 {
        font-size: 2rem;
        margin: 10px 0;
        font-weight: 800;
    }
    
    /* 漸層標題 */
    .main-title {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    /* 內容容器 */
    .content-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* 按鈕優化 */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Metric 優化 */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* 警示框優化 */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State 初始化 ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 首頁概覽"
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["2330.TW", "0050.TW", "AAPL", "TSLA"]
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

# --- 工具函數 ---
def get_stock_data(ticker, period="1y"):
    """獲取股票數據"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        info = stock.info
        return data, info
    except:
        return None, None

def calculate_returns(data):
    """計算報酬率"""
    if data is None or len(data) == 0:
        return 0
    return ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100)

def get_risk_allocation(risk_level, age):
    """根據風險等級和年齡計算資產配置"""
    risk_map = {
        "保守": {"股票": 20, "債券": 60, "現金": 20},
        "穩健": {"股票": 40, "債券": 45, "現金": 15},
        "成長": {"股票": 60, "債券": 30, "現金": 10},
        "積極": {"股票": 80, "債券": 15, "現金": 5}
    }
    
    base_allocation = risk_map[risk_level]
    
    # 年齡調整：年紀越大,股票比例略降
    age_adjustment = max(0, (age - 30) * 0.5)
    base_allocation["股票"] = max(10, base_allocation["股票"] - age_adjustment)
    base_allocation["債券"] = min(80, base_allocation["債券"] + age_adjustment)
    
    return base_allocation

# --- 頂部導航 ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col_nav = st.columns(5)

nav_items = ["🏠 首頁概覽", "🤖 AI 智能配資", "📊 即時盤勢", "💼 我的投資組合", "💡 投資策略庫"]
for idx, item in enumerate(nav_items):
    with col_nav[idx]:
        if st.button(item, use_container_width=True, key=f"nav_{idx}"):
            st.session_state.current_page = item

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 1. 🏠 首頁概覽
# ==========================================
if st.session_state.current_page == "🏠 首頁概覽":
    st.markdown('<p class="main-title">AI 投資小秘書 Pro</p>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; margin-bottom: 2rem;'>您專屬的智能資產管理顧問</h4>", unsafe_allow_html=True)
    
    # 獲取即時市場數據
    indices = {
        "^TWII": "台股加權",
        "^GSPC": "S&P 500",
        "^DJI": "道瓊指數",
        "^IXIC": "那斯達克"
    }
    
    cols = st.columns(4)
    for idx, (ticker, name) in enumerate(indices.items()):
        with cols[idx]:
            try:
                data, _ = get_stock_data(ticker, period="5d")
                if data is not None and len(data) > 1:
                    current = data['Close'].iloc[-1]
                    prev = data['Close'].iloc[-2]
                    change = ((current - prev) / prev) * 100
                    color = "#00C853" if change >= 0 else "#ff5252"
                    arrow = "▲" if change >= 0 else "▼"
                    
                    st.markdown(f'''
                        <div class="stat-card">
                            <h3>{name}</h3>
                            <h2 style="color: {color};">{current:,.0f}</h2>
                            <p style="color: {color}; font-weight: 600;">{arrow} {abs(change):.2f}%</p>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="stat-card"><h3>{name}</h3><p>數據載入中...</p></div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="stat-card"><h3>{name}</h3><p>無法載入</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 我的自選股
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📌 我的自選股動態")
    
    cols = st.columns(len(st.session_state.watchlist))
    for idx, ticker in enumerate(st.session_state.watchlist):
        with cols[idx]:
            data, info = get_stock_data(ticker, period="1mo")
            if data is not None and len(data) > 0:
                returns = calculate_returns(data)
                current_price = data['Close'].iloc[-1]
                color = "green" if returns >= 0 else "red"
                
                st.metric(
                    label=ticker,
                    value=f"${current_price:.2f}",
                    delta=f"{returns:.2f}%"
                )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI 智能分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🧠 今日 AI 盤勢分析")
        st.info("📊 **市場情緒**: 偏多 (65/100)\n\n"
                "💡 **關鍵觀察**: 科技股持續強勢,半導體資金流入明顯\n\n"
                "⚠️ **風險提示**: 留意美國 Fed 利率決議\n\n"
                "✅ **操作建議**: 建議維持 60-70% 持股水位")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("📰 重要財經新聞")
        st.success("🔥 **AI 晶片需求暴增**: 輝達 Q4 營收超預期 30%")
        st.warning("⚡ **Fed 會議**: 市場預期維持利率不變")
        st.info("💰 **台積電**: 3nm 製程訂單滿載至明年 Q2")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. 🤖 AI 智能配資
# ==========================================
elif st.session_state.current_page == "🤖 AI 智能配資":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("🤖 AI 智能資產配置優化")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age = st.number_input("您的年齡", 20, 80, 35, help="年齡會影響資產配置比例")
    with col2:
        monthly_save = st.number_input("每月投入金額 (元)", 5000, 500000, 30000, step=5000)
    with col3:
        risk = st.select_slider("風險承擔等級", options=["保守", "穩健", "成長", "積極"])
    with col4:
        years = st.number_input("投資年限", 1, 40, 20, help="預計投資多少年")

    if st.button("🚀 生成 AI 投資診斷報告", use_container_width=True):
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        
        # 計算資產配置
        allocation = get_risk_allocation(risk, age)
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            # 餅圖
            labels = list(allocation.keys())
            values = list(allocation.values())
            colors = ['#667eea', '#764ba2', '#f093fb']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values,
                hole=.5,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont_size=14
            )])
            fig.update_layout(
                title="🎯 建議資產配置比例",
                height=400,
                showlegend=True,
                margin=dict(t=50, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_res2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("📊 投資試算結果")
            
            # 計算預期報酬
            expected_return = {
                "保守": 4.5,
                "穩健": 6.5,
                "成長": 8.5,
                "積極": 10.5
            }
            
            annual_return = expected_return[risk]
            total_invest = monthly_save * 12 * years
            
            # 複利計算
            future_value = monthly_save * ((1 + annual_return/100/12)**(years*12) - 1) / (annual_return/100/12)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("總投入金額", f"NT$ {total_invest:,.0f}")
                st.metric("預估年化報酬", f"{annual_return}%")
            with col_m2:
                st.metric("預估最終資產", f"NT$ {future_value:,.0f}")
                st.metric("預估獲利", f"NT$ {future_value - total_invest:,.0f}")
            
            st.divider()
            
            st.markdown("### 💡 AI 診斷建議")
            st.write(f"✅ **風險等級**: {risk} - 適合您的年齡與目標")
            st.write(f"📈 **核心策略**: 股票 {allocation['股票']}% / 債券 {allocation['債券']}% / 現金 {allocation['現金']}%")
            st.write(f"🎯 **目標達成**: {years} 年後預計累積 **{future_value/10000:.0f} 萬元**")
            st.write(f"⚡ **再平衡**: 建議每季檢視一次資產配置")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 建議投資標的
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("📋 建議投資標的組合")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.markdown("#### 🎯 股票部位")
            st.write("- **0050.TW** (40%): 台灣 50 ETF")
            st.write("- **VTI** (30%): 美國全市場 ETF")
            st.write("- **VWO** (30%): 新興市場 ETF")
        
        with col_t2:
            st.markdown("#### 🛡️ 債券部位")
            st.write("- **AGG** (50%): 美國綜合債券")
            st.write("- **BND** (30%): 美債 ETF")
            st.write("- **元大AAA至A公司債** (20%)")
        
        with col_t3:
            st.markdown("#### 💰 現金部位")
            st.write("- **高利活存** (60%)")
            st.write("- **貨幣市場基金** (40%)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. 📊 即時盤勢
# ==========================================
elif st.session_state.current_page == "📊 即時盤勢":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("📊 全球市場動態監測")
    
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        ticker = st.text_input("輸入股票代碼", "2330.TW", 
                               help="台股加 .TW (如: 2330.TW)、美股直接輸入代碼 (如: AAPL)")
    with col_input2:
        period = st.selectbox("時間區間", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if ticker:
        data, info = get_stock_data(ticker, period=period)
        
        if data is not None and len(data) > 0:
            # 股票資訊卡片
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            col_info = st.columns(5)
            with col_info[0]:
                st.metric("當前價格", f"${data['Close'].iloc[-1]:.2f}")
            with col_info[1]:
                day_change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100)
                st.metric("日漲跌", f"{day_change:.2f}%")
            with col_info[2]:
                period_return = calculate_returns(data)
                st.metric("區間報酬", f"{period_return:.2f}%")
            with col_info[3]:
                st.metric("最高價", f"${data['High'].max():.2f}")
            with col_info[4]:
                st.metric("最低價", f"${data['Low'].min():.2f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # K線圖與成交量
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(f'{ticker} 價格走勢', '成交量')
            )
            
            # K線圖
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='K線',
                    increasing_line_color='#00C853',
                    decreasing_line_color='#ff5252'
                ),
                row=1, col=1
            )
            
            # 移動平均線
            ma20 = data['Close'].rolling(window=20).mean()
            ma60 = data['Close'].rolling(window=60).mean()
            
            fig.add_trace(
                go.Scatter(x=data.index, y=ma20, name='MA20', 
                          line=dict(color='#667eea', width=1.5)),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=data.index, y=ma60, name='MA60',
                          line=dict(color='#764ba2', width=1.5)),
                row=1, col=1
            )
            
            # 成交量
            colors = ['#00C853' if data['Close'].iloc[i] >= data['Open'].iloc[i] 
                     else '#ff5252' for i in range(len(data))]
            
            fig.add_trace(
                go.Bar(x=data.index, y=data['Volume'], name='成交量',
                      marker_color=colors, opacity=0.5),
                row=2, col=1
            )
            
            fig.update_layout(
                height=700,
                xaxis_rangeslider_visible=False,
                hovermode='x unified',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            fig.update_xaxes(title_text="日期", row=2, col=1)
            fig.update_yaxes(title_text="價格", row=1, col=1)
            fig.update_yaxes(title_text="成交量", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 技術指標
            col_tech1, col_tech2 = st.columns(2)
            
            with col_tech1:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.subheader("📈 技術指標分析")
                
                current_price = data['Close'].iloc[-1]
                ma20_current = ma20.iloc[-1]
                ma60_current = ma60.iloc[-1]
                
                if current_price > ma20_current > ma60_current:
                    trend = "🟢 強勢多頭"
                elif current_price > ma20_current:
                    trend = "🟡 偏多格局"
                elif current_price < ma20_current < ma60_current:
                    trend = "🔴 弱勢空頭"
                else:
                    trend = "🟡 盤整格局"
                
                st.write(f"**趨勢判斷**: {trend}")
                st.write(f"**MA20**: ${ma20_current:.2f}")
                st.write(f"**MA60**: ${ma60_current:.2f}")
                st.write(f"**支撐位**: ${data['Low'].tail(20).min():.2f}")
                st.write(f"**壓力位**: ${data['High'].tail(20).max():.2f}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_tech2:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.subheader("📊 統計數據")
                
                volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
                
                st.write(f"**年化波動率**: {volatility:.2f}%")
                st.write(f"**平均成交量**: {data['Volume'].mean():,.0f}")
                st.write(f"**最大回撤**: {((data['Close'].max() - data['Close'].min()) / data['Close'].max() * 100):.2f}%")
                st.write(f"**資料筆數**: {len(data)} 天")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 歷史數據
            with st.expander("📋 查看詳細歷史數據"):
                st.dataframe(data.tail(30).sort_index(ascending=False), use_container_width=True)
        else:
            st.error("❌ 無法獲取股票資料,請確認代碼是否正確")

# ==========================================
# 4. 💼 我的投資組合
# ==========================================
elif st.session_state.current_page == "💼 我的投資組合":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("💼 投資組合管理")
    
    # 新增持股
    st.subheader("➕ 新增持股")
    col_add = st.columns([2, 1, 1, 1, 1])
    with col_add[0]:
        new_ticker = st.text_input("股票代碼", key="new_ticker")
    with col_add[1]:
        new_shares = st.number_input("持有股數", min_value=0, value=100, key="new_shares")
    with col_add[2]:
        new_cost = st.number_input("成本價", min_value=0.0, value=100.0, key="new_cost")
    with col_add[3]:
        st.write("")
        st.write("")
        if st.button("新增", use_container_width=True):
            if new_ticker:
                st.session_state.portfolio[new_ticker] = {
                    "shares": new_shares,
                    "cost": new_cost
                }
                st.success(f"✅ 已新增 {new_ticker}")
                st.rerun()
    with col_add[4]:
        st.write("")
        st.write("")
        if st.button("清空", use_container_width=True):
            st.session_state.portfolio = {}
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 顯示投資組合
    if st.session_state.portfolio:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("📊 持股明細")
        
        portfolio_data = []
        total_cost = 0
        total_value = 0
        
        for ticker, holding in st.session_state.portfolio.items():
            data, _ = get_stock_data(ticker, period="1d")
            if data is not None and len(data) > 0:
                current_price = data['Close'].iloc[-1]
                cost = holding["cost"]
                shares = holding["shares"]
                
                position_cost = cost * shares
                position_value = current_price * shares
                profit = position_value - position_cost
                profit_pct = (profit / position_cost) * 100
                
                total_cost += position_cost
                total_value += position_value
                
                portfolio_data.append({
                    "股票代碼": ticker,
                    "持有股數": shares,
                    "成本價": f"${cost:.2f}",
                    "現價": f"${current_price:.2f}",
                    "成本金額": f"${position_cost:,.2f}",
                    "市值": f"${position_value:,.2f}",
                    "損益": f"${profit:,.2f}",
                    "報酬率": f"{profit_pct:.2f}%"
                })
        
        df = pd.DataFrame(portfolio_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 總覽
        st.divider()
        col_sum = st.columns(4)
        with col_sum[0]:
            st.metric("總成本", f"NT$ {total_cost:,.0f}")
        with col_sum[1]:
            st.metric("總市值", f"NT$ {total_value:,.0f}")
        with col_sum[2]:
            total_profit = total_value - total_cost
            st.metric("總損益", f"NT$ {total_profit:,.0f}")
        with col_sum[3]:
            total_return = (total_profit / total_cost * 100) if total_cost > 0 else 0
            st.metric("總報酬率", f"{total_return:.2f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 目前沒有持股記錄,請先新增持股")

# ==========================================
# 5. 💡 投資策略庫
# ==========================================
elif st.session_state.current_page == "💡 投資策略庫":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("💡 專業投資知識庫")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 熱門主題", "📖 投資基礎", "🧩 進階技術", "🎓 經典策略"])
    
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🔥 2024-2025 投資熱門話題")
        
        col_hot1, col_hot2 = st.columns(2)
        
        with col_hot1:
            st.markdown("### 🤖 AI 產業深度解讀")
            st.write("""
            **為何輝達(NVIDIA)是核心?**
            - GPU 運算能力是 AI 訓練的基礎設施
            - 市佔率超過 80%,護城河極深
            - 從雲端到邊緣運算全方位布局
            
            **AI 產業鏈投資機會:**
            - 上游: 輝達、AMD、台積電
            - 中游: 微軟、Google、亞馬遜 (雲端服務)
            - 下游: 各類 AI 應用公司
            """)
            
            st.markdown("### 💰 高股息投資陷阱")
            st.write("""
            **如何避開只配息沒價差的標的?**
            - ⚠️ 殖利率 > 8% 要特別小心
            - 📊 檢查股價是否長期下跌
            - 💡 關注配息穩定性(至少看 5 年)
            - ✅ 優先選擇「股利成長股」而非高殖利率股
            
            **推薦篩選條件:**
            - 連續 5 年配息
            - 股利成長率 > 3%
            - 本益比 < 20
            - 負債比 < 50%
            """)
        
        with col_hot2:
            st.markdown("### 🌐 台美股連動分析")
            st.write("""
            **費城半導體指數對台股的影響**
            - 台股權值前 10 名有 5 家是半導體
            - 費半漲 → 台積電漲 → 台股漲 (高度連動)
            - 美股開盤前可觀察費半期貨走向
            
            **操作建議:**
            1. 美股收盤後 1 小時內做功課
            2. 費半大漲 > 2% → 台股開高機率大
            3. 注意時差: 美股收盤 = 台灣早上 6 點
            """)
            
            st.markdown("### 🏦 2025 央行政策展望")
            st.write("""
            **升息或降息如何影響投資?**
            - 📈 **升息環境**: 現金為王,債券、高股息股受惠
            - 📉 **降息環境**: 成長股、科技股表現較佳
            - 🎯 **當前環境(2025 Q1)**: 利率高檔持平,等待降息訊號
            
            **投資策略:**
            - 維持股 6 債 3 現 1 的配置
            - 科技股保持 50-60% 比重
            - 等待明確降息訊號再加碼成長股
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("📖 投資基礎知識")
        
        with st.expander("💡 什麼是定期定額?為什麼有效?"):
            st.write("""
            **定期定額 (Dollar Cost Averaging, DCA)**
            
            **核心概念:**
            - 固定時間(如每月 1 號)
            - 固定金額(如 10,000 元)
            - 買入同一標的
            
            **為什麼有效?**
            1. **降低成本風險**: 高點少買、低點多買
            2. **避免情緒干擾**: 不需判斷進場時機
            3. **強迫儲蓄**: 養成投資習慣
            
            **實際案例:**
            ```
            1月: 股價 100 元,買 100 股 = 10,000 元
            2月: 股價 50 元,買 200 股 = 10,000 元
            3月: 股價 80 元,買 125 股 = 10,000 元
            
            平均成本 = 30,000 / 425 = 70.6 元
            (比簡單平均 76.7 元更低!)
            ```
            
            **適合標的:**
            - ✅ 0050、0056 等大盤 ETF
            - ✅ VTI、VOO 等美股 ETF
            - ❌ 個股波動太大,風險高
            """)
        
        with st.expander("📊 ETF vs 個股: 該選哪一個?"):
            st.write("""
            | 比較項目 | ETF | 個股 |
            |---------|-----|------|
            | **風險** | 低(分散) | 高(集中) |
            | **報酬** | 市場平均 | 可能很高或很低 |
            | **研究成本** | 低 | 高(需研究財報) |
            | **適合對象** | 新手、忙碌族 | 進階投資人 |
            | **持有數量** | 3-5 檔即可 | 需 8-10 檔分散 |
            
            **新手建議:**
            1. 先從 ETF 開始 (0050 或 VTI)
            2. 投入至少 1 年,感受市場波動
            3. 學習看財報後再考慮個股
            4. 個股佔比不超過總資產 30%
            """)
        
        with st.expander("💰 資產配置黃金比例"):
            st.write("""
            **經典配置法則:**
            
            **1. 100 法則 (保守型)**
            - 股票比例 = 100 - 年齡
            - 30 歲 → 70% 股票 + 30% 債券
            - 50 歲 → 50% 股票 + 50% 債券
            
            **2. 110/120 法則 (積極型)**
            - 股票比例 = 110 - 年齡 (或 120 - 年齡)
            - 30 歲 → 80-90% 股票
            
            **3. 風險平價策略**
            - 股票 60%、債券 30%、現金 10%
            - 適合大多數人的均衡配置
            
            **4. 核心-衛星策略**
            - 核心 70%: 大盤 ETF (穩定)
            - 衛星 30%: 主題型 ETF 或個股 (追求超額報酬)
            """)
        
        with st.expander("🎯 如何設定投資目標?"):
            st.write("""
            **SMART 原則:**
            - **S**pecific (具體): "5 年存 100 萬" 而非 "想要有錢"
            - **M**easurable (可衡量): 設定明確數字
            - **A**chievable (可達成): 符合收入與能力
            - **R**elevant (相關): 與人生規劃連結
            - **T**ime-bound (有期限): 設定明確時間
            
            **範例目標:**
            - 💍 短期(1-3年): 結婚基金 50 萬
            - 🏠 中期(5-10年): 買房頭期款 200 萬
            - 🌴 長期(20-30年): 退休金 2000 萬
            
            **反推每月投入:**
            ```
            目標: 10 年存 300 萬
            假設年化報酬 7%
            → 每月需投入約 18,000 元
            ```
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🧩 進階投資技術")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("### 📈 技術分析入門")
            st.write("""
            **移動平均線 (MA)**
            - MA20: 月線,短期趨勢
            - MA60: 季線,中期趨勢
            - **黃金交叉**: 短均線上穿長均線 → 買入訊號
            - **死亡交叉**: 短均線下穿長均線 → 賣出訊號
            
            **相對強弱指標 (RSI)**
            - RSI > 70: 超買,注意回檔
            - RSI < 30: 超賣,可能反彈
            - 最佳買點: RSI 從 30 以下回升
            
            **布林通道 (Bollinger Bands)**
            - 價格觸及上軌 → 可能回落
            - 價格觸及下軌 → 可能反彈
            - 通道收窄 → 即將大波動
            """)
            
            st.markdown("### 💼 價值投資指標")
            st.write("""
            **本益比 (PE Ratio)**
            - PE = 股價 / 每股盈餘
            - PE < 15: 相對便宜
            - PE > 25: 相對昂貴
            - ⚠️ 不同產業標準不同
            
            **股價淨值比 (PB Ratio)**
            - PB = 股價 / 每股淨值
            - PB < 1: 股價低於帳面價值
            - 適合用於金融、傳產股
            
            **股東權益報酬率 (ROE)**
            - ROE = 淨利 / 股東權益
            - ROE > 15%: 優質公司
            - ROE > 20%: 超級績優股
            - 巴菲特最愛的指標!
            """)
        
        with col_adv2:
            st.markdown("### 🔄 再平衡策略")
            st.write("""
            **為什麼需要再平衡?**
            - 市場漲跌會改變原定配置比例
            - 股票大漲後風險提高
            - 定期調整維持風險控制
            
            **操作方法:**
            
            **情境 1: 股票大漲**
            ```
            原定配置: 股 60% / 債 40%
            漲後變成: 股 75% / 債 25%
            
            → 賣出 15% 股票
            → 買入 15% 債券
            → 回到 60% / 40%
            ```
            
            **情境 2: 股票大跌**
            ```
            原定配置: 股 60% / 債 40%
            跌後變成: 股 45% / 債 55%
            
            → 賣出 15% 債券
            → 買入 15% 股票
            → 回到 60% / 40%
            ```
            
            **再平衡頻率:**
            - ✅ 每季檢視一次
            - ✅ 偏離超過 5% 就調整
            - ❌ 不要每天調整(交易成本高)
            """)
            
            st.markdown("### 🛡️ 風險管理")
            st.write("""
            **停損策略**
            - 個股: -7% 至 -10% 停損
            - ETF: -15% 至 -20% 停損
            - ⚠️ 停損不是認賠,是風險控制
            
            **資金控管**
            - 單一個股不超過 10%
            - 同產業不超過 30%
            - 保留 10% 現金應急
            
            **心理建設**
            - 虧損 20% 需漲 25% 才能回本
            - 虧損 50% 需漲 100% 才能回本
            - 保護資本 > 追求報酬
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🎓 經典投資策略")
        
        with st.expander("🏆 巴菲特價值投資法"):
            st.write("""
            **核心理念:**
            「以合理的價格買入優秀的公司,長期持有」
            
            **選股標準:**
            1. ✅ 護城河夠深 (競爭優勢)
            2. ✅ ROE > 15% 且穩定
            3. ✅ 自由現金流充沛
            4. ✅ 負債比 < 50%
            5. ✅ 經營團隊誠信可靠
            
            **估值方法:**
            - 本益比低於產業平均
            - 股價淨值比 < 3
            - 殖利率 > 3%
            
            **持有原則:**
            - 長期持有(5 年以上)
            - 不因短期波動賣出
            - 除非基本面惡化
            
            **巴菲特愛股:**
            - 可口可樂 (持有超過 30 年)
            - 蘋果 (目前最大持股)
            - 美國銀行
            """)
        
        with st.expander("📊 指數化投資 (被動投資)"):
            st.write("""
            **理論基礎:**
            - 95% 的主動基金跑不贏大盤
            - 長期持有指數即可獲得市場平均報酬
            - 低成本、免選股、省時間
            
            **核心標的:**
            
            **台股:**
            - 0050 (元大台灣 50)
            - 006208 (富邦台 50)
            
            **美股:**
            - VTI (美國全市場)
            - VOO (S&P 500)
            - VT (全球股市)
            
            **債券:**
            - AGG (美國綜合債券)
            - BND (美國債券總體市場)
            
            **標準配置:**
            ```
            積極型 (30 歲以下):
            - 80% VTI + 20% AGG
            
            穩健型 (30-50 歲):
            - 60% VTI + 30% AGG + 10% 現金
            
            保守型 (50 歲以上):
            - 40% VTI + 50% AGG + 10% 現金
            ```
            """)
        
        with st.expander("🔄 動態再平衡策略"):
            st.write("""
            **策略說明:**
            設定股債比例,定期調整以維持風險水平
            
            **基本配置: 60/40 法則**
            - 60% 股票 ETF
            - 40% 債券 ETF
            
            **操作規則:**
            
            **每季檢視一次:**
            1. 計算當前比例
            2. 如偏離 ±5% → 進行調整
            3. 賣出漲多的、買入跌多的
            
            **範例:**
            ```
            Q1: 股 60% 債 40% (初始)
            Q2: 股票大漲 → 股 70% 債 30%
            動作: 賣 10% 股票,買入債券
            結果: 回到 60% / 40%
            
            Q3: 股票大跌 → 股 50% 債 50%
            動作: 賣 10% 債券,買入股票
            結果: 回到 60% / 40%
            ```
            
            **優點:**
            - 自動「逢高賣、逢低買」
            - 風險控制穩定
            - 不需預測市場
            
            **缺點:**
            - 牛市可能少賺
            - 需要紀律執行
            - 有交易成本
            """)
        
        with st.expander("💰 股利成長投資法"):
            st.write("""
            **策略核心:**
            買入「連續配息且股利成長」的公司,創造穩定現金流
            
            **篩選條件:**
            1. ✅ 連續 10 年以上配息
            2. ✅ 股利年成長率 > 5%
            3. ✅ 配息率 40-60% (太高或太低都不好)
            4. ✅ ROE > 15%
            5. ✅ 負債比 < 60%
            
            **美股經典標的:**
            - 可口可樂 (連續配息 60+ 年)
            - 寶僑 P&G (連續配息 65+ 年)
            - 3M (股利貴族成員)
            
            **台股潛力標的:**
            - 中華電 (穩定高息)
            - 台積電 (股利持續成長)
            - 統一超 (連續配息)
            
            **適合族群:**
            - 退休族需要現金流
            - 保守投資人
            - 想建立被動收入
            
            **風險提醒:**
            - 不要只看殖利率高低
            - 注意公司成長性
            - 避免「價差虧損」
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 15px; margin-top: 2rem;'>
        <p style='color: #666; margin: 0;'>
            <strong>AI 投資小秘書 Pro</strong> | 
            僅供學術研究使用,不代表任何投資建議 | 
            投資有風險,請謹慎評估
        </p>
        <p style='color: #999; font-size: 0.9rem; margin-top: 10px;'>
            © 2025 All Rights Reserved | 
            數據來源: Yahoo Finance
        </p>
    </div>
""", unsafe_allow_html=True)
