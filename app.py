import streamlit as st
import pandas as pd
from google.cloud import storage
from io import StringIO
import os

st.set_page_config(page_title="Bullas Spank Monitor", layout="wide")

BUCKET_NAME = "bullas-spank-logs"
BLOB_NAME = "2025-04-30_spank_log.csv"

@st.cache_data
def load_data(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return pd.read_csv(StringIO(blob.download_as_text()), parse_dates=["timestamp"])

try:
    df = load_data(BUCKET_NAME, BLOB_NAME)
    latest = df.iloc[-1]
    st.title("🐻 Bullas Spank Monitor")
    st.metric("1h Spank", latest["last_1h_spank_count"])
    st.line_chart(df.set_index("timestamp")[["last_1h_spank_count"]])
except Exception as e:
    st.error(f"読み込み失敗: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    os.system(f"streamlit run app.py --server.port {port} --server.headless true")