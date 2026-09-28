import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ページ設定
st.set_page_config(page_title="Financial Market Dashboard", layout="wide")
st.title("📈 Market Technical & Risk Analytics Dashboard")

# サイドバー設定
st.sidebar.header("Parameters")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
sma_short = st.sidebar.slider("Short SMA Window", 5, 50, 20)
sma_long = st.sidebar.slider("Long SMA Window", 20, 200, 50)

# データ取得
@st.cache_data
def load_data(symbol, p):
    df = yf.download(symbol, period=p)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

try:
    df = load_data(ticker, period)
    
    if df.empty:
        st.error("No data found for the ticker.")
    else:
        # 指標計算
        df['SMA_Short'] = df['Close'].rolling(window=sma_short).mean()
        df['SMA_Long'] = df['Close'].rolling(window=sma_long).mean()
        df['Daily_Return'] = df['Close'].pct_change()
        
        # ボリンジャーバンド
        rolling_std = df['Close'].rolling(window=sma_short).std()
        df['BB_Upper'] = df['SMA_Short'] + (rolling_std * 2)
        df['BB_Lower'] = df['SMA_Short'] - (rolling_std * 2)

        # 主要メトリクスの表示
        col1, col2, col3 = st.columns(3)
        latest_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        price_diff = latest_price - prev_price
        pct_change = (price_diff / prev_price) * 100
        volatility = df['Daily_Return'].std() * (252 ** 0.5) * 100  # 年率ボラティリティ

        col1.metric("Latest Close", f"${latest_price:.2f}", f"{price_diff:.2f} ({pct_change:.2f}%)")
        col2.metric("Annualized Volatility", f"{volatility:.2f}%")
        col3.metric("Data Points", len(df))

        # ローソク足 + 指標チャート
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name='Market Price'))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_Short'], line=dict(color='orange', width=1.5), name=f'SMA {sma_short}'))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_Long'], line=dict(color='blue', width=1.5), name=f'SMA {sma_long}'))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='gray', width=1, dash='dash'), name='Upper Band'))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='gray', width=1, dash='dash'), name='Lower Band'))

        fig.update_layout(title=f"{ticker} Price & Technical Indicators", xaxis_rangeslider_visible=False, height=550)
        st.plotly_chart(fig, use_container_width=True)

        # リターン分布の可視化
        st.subheader("Daily Returns Distribution")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=df['Daily_Return'].dropna(), nbinsx=50, marker_color='teal'))
        fig_hist.update_layout(title="Daily Return Histogram", xaxis_title="Daily Return", yaxis_title="Count", height=350)
        st.plotly_chart(fig_hist, use_container_width=True)

except Exception as e:
    st.error(f"Error fetching data: {e}")