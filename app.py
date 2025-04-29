import streamlit as st
import pandas as pd
from google.cloud import storage
from io import StringIO
from datetime import datetime
import os

st.set_page_config(page_title="🐮 Bull ish Monitor", layout="wide")

BUCKET_NAME = "bullas-spank-logs"
date_str = datetime.utcnow().strftime("%Y-%m-%d")
BLOB_NAME = f"{date_str}_spank_log.csv"

@st.cache_data
def load_data(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return pd.read_csv(StringIO(blob.download_as_text()), parse_dates=["timestamp"])

try:
    df = load_data(BUCKET_NAME, BLOB_NAME)
    latest = df.iloc[-1]
    st.title(f"🐻 Bullas Spank Monitor ({date_str})")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💥 1h Spank数", latest["last_1h_spank_count"])
    col2.metric("🧍 ユニーク数", latest["unique_spanker_count_last_1h"])
    col3.metric("🐋 ホエール数", latest["whale_spank_count_last_1h"])
    col4.metric("⚡ Spank/分", latest["spank_per_minute"])
    st.line_chart(df.set_index("timestamp")[["last_1h_spank_count", "regular_hit_count"]])
    st.dataframe(df.tail(20), use_container_width=True)
except Exception as e:
    st.error(f"⚠️ データ読み込み失敗: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Launching Streamlit on port {port}")
    os.system(f"streamlit run app.py --server.port {port} --server.headless true")
