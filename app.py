import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Bullas Spank Monitor", layout="wide")

# 📁 ログフォルダとCSVファイル一覧
LOG_DIR = "logs"
log_files = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".csv")])

# 📅 日付セレクトボックス（ファイル名から）
selected_file = st.selectbox("📅 日付を選択", log_files, index=len(log_files)-1)

# 📊 CSV読み込み
df = pd.read_csv(os.path.join(LOG_DIR, selected_file), parse_dates=["timestamp"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 🔢 最新データ表示
latest = df.iloc[-1]

st.title("🐻 Bullas Spank Monitoring")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💥 1h Spank数", latest["last_1h_spank_count"])
col2.metric("🧍 ユニーク数", latest["unique_spanker_count_last_1h"])
col3.metric("🐋 ホエール数", latest["whale_spank_count_last_1h"])
col4.metric("⚡ Spank/分", latest["spank_per_minute"])

# 📈 グラフ表示
st.subheader("📈 スパンク推移（15分ごと）")
st.line_chart(df.set_index("timestamp")[["last_1h_spank_count", "regular_hit_count"]])

# 📋 テーブル表示
st.subheader("📋 ログ一覧")
st.dataframe(df.tail(20), use_container_width=True)
