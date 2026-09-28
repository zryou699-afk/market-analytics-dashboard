# 📈 Market Technical & Risk Analytics Dashboard

PythonとStreamlitを活用した、金融市場データ（株式・為替）のテクニカル分析およびリスク指標の動的可視化ダッシュボードです。

## 🌐 Live Demo
👉 **[Webアプリを開く](あなたのStreamlitのURLをここに貼る)**

## 🛠 主な機能
- **動的な銘柄・期間変更**: 米国株、日本株（^N225）、為替（USDJPY=X）など任意のティッカーに対応
- **インタラクティブ・ローソク足チャート**: Plotlyを用いた拡大・縮小・ホバー機能付きチャート
- **テクニカル指標の動的算出**:
  - 短期・長期の単純移動平均線（SMA）
  - ボリンジャーバンド（±2σ）
- **リスク・リターン分析**:
  - 年率ボラティリティの自動算出（年換算 $\sqrt{252}$）
  - 日次リターンの分布ヒストグラム表示

## 💻 使用技術（Tech Stack）
- **Language**: Python 3
- **Framework**: Streamlit
- **Data Source**: yfinance (Yahoo! Finance API)
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly
- **Deployment**: Streamlit Community Cloud
