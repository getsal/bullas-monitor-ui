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
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💥 Spank/lasthour", latest["last_1h_spank_count"])
col2.metric("🐮 Unique Bullas/hour ", latest["unique_spanker_count_last_1h"])
col3.metric("🐋 Whale Bulla", latest["whale_spank_count_last_1h"])
col4.metric("⚡ Spank/min", latest["spank_per_minute"])
col5.metric("⏳ Breadline expected", f"{average_breadline_hour:.2f} Hour!!")
st.line_chart(df.set_index("timestamp")[["last_1h_spank_count", "regular_hit_count"]])
st.dataframe(df.tail(20), use_container_width=True)
if latest["last_1h_spank_count"] > 0:
    average_breadline_hour = 300.0 / latest["last_1h_spank_count"]
else:
    average_breadline_hour = float("inf")  # または 0.0except Exception as e:
st.error(f"⚠️ Failed load data. Mooooo!: {e}")

if **name** == "**main**":
port = int(os.environ.get("PORT", 8080))
print(f"🚀 Launching Streamlit on port {port}")
os.system(f"streamlit run [app.py](http://app.py) --server.port {port} --server.headless true")
