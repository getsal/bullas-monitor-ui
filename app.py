import os
import streamlit as st
import pandas as pd
from google.cloud import storage
from io import StringIO
from datetime import datetime

# GCS settings
BUCKET_NAME = "bullas-spank-logs"
today_str = datetime.utcnow().strftime("%Y-%m-%d")
SPANK_BLOB = f"{today_str}_spank_log.csv"
CLICK_BLOB = f"click_log_{today_str}.csv"

# Load CSV function
@st.cache_data
def load_csv(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    return pd.read_csv(StringIO(content), parse_dates=["timestamp"])

# Main app
st.set_page_config(page_title="Bullas Click Monitor", layout="wide")

try:
    # --- Load Click Log ---
    df_click = load_csv(BUCKET_NAME, CLICK_BLOB)
    st.title("🖱️ Click Log Monitor")

    st.subheader("📌 Latest Click Records")
    st.dataframe(df_click.tail(10), use_container_width=True)

    st.subheader("🏆 Top Spankers")
    ranking = df_click.groupby("spanker")["click_count"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(ranking)

    st.subheader("⏱️ Timeline (Click Count per 15min)")
    df_click_agg = df_click.resample("15min", on="timestamp")["click_count"].sum().reset_index()
    st.line_chart(df_click_agg.set_index("timestamp"))

except Exception as e:
    st.error(f"⚠️ Failed to load click log: {e}")

st.divider()

try:
    # --- Load Spank Log ---
    df_spank = load_csv(BUCKET_NAME, SPANK_BLOB)
    latest = df_spank.iloc[-1]

    st.title(f"🐮 Bullas Monitor ({today_str})")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💥 Spank (last hour)", latest["last_1h_spank_count"])
    col2.metric("🐮 Unique Spankers (hour)", latest["unique_spanker_count_last_1h"])
    col3.metric("🐋 Whale Spankers", latest["whale_spank_count_last_1h"])
    col4.metric("⚡ Spank per Minute", latest["spank_per_minute"])

    # Breadline expected time
    if latest["last_1h_spank_count"] > 0:
        average_breadline_hour = 300.0 / latest["last_1h_spank_count"]
    else:
        average_breadline_hour = float("inf")
    col5.metric("⏳ Breadline Expected", f"{average_breadline_hour:.2f} hours")

    st.line_chart(df_spank.set_index("timestamp")[["last_1h_spank_count", "regular_hit_count"]])
    st.dataframe(df_spank.tail(20), use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Failed to load spank log: {e}")

# ✅ Launch in Cloud Run properly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Launching Streamlit on port {port}")
    os.system(f"streamlit run app.py --server.port {port} --server.headless true")