import streamlit as st
import pandas as pd
from google.cloud import storage
from io import StringIO
import os

st.set_page_config(page_title="Bullas Spank Monitor", layout="wide")

BUCKET_NAME = "bullas-spank-logs"
BLOB_NAME = "2025-04-30_spank_log.csv"  # ← GCS上の最新ファイル名に合わせて

@st.cache_data
def load_data(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    csv_content = blob.download_as_text()
    return pd.read_csv(StringIO(csv_content), parse_dates=["timestamp"])

try:
    df = load_data(BUCKET_NAME, BLOB_NAME)
    latest = df.iloc[-1]

    st.title("🐻 Bullas Spank Monitoring (from GCS)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💥 1h Spank数", latest["last_1h_spank_count"])
    col2.metric("🧍 ユニーク数", latest["unique_spanker_count_last_1h"])
    col3.metric("🐋 ホエール数", latest["whale_spank_count_last_1h"])
    col4.metric("⚡ Spank/分", latest["spank_per_minute"])

    st.line_chart(df.set_index("timestamp")[["last_1h_spank_count", "regular_hit_count"]])
    st.dataframe(df.tail(20), use_container_width=True)
except Exception as e:
    st.error(f"⚠️ データ読み込み失敗: {e}")

# ✅ Cloud RunでPORT=8080を受けて起動する
if __name__ == "__main__":
    import streamlit.web.bootstrap
    import sys
    sys.argv = ["streamlit", "run", "app.py", "--server.port=8080", "--server.headless=true"]
    streamlit.web.bootstrap.run()
