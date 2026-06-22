"""
dashboard.py — Smart Grid Monitor Dashboard (Sprint 6)
Streamlit app that reads smart_grid_report.csv and visualizes
device status, trends, alert history, summary stats, and pattern analysis.
"""

import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import time

CSV_PATH = "smart_grid_report.csv"
REFRESH_INTERVAL = 10  # seconds

SEVERITY_ORDER = ["CRITICAL", "WARNING", "PRE-WARNING", "INFO"]

SEVERITY_COLOR = {
    "CRITICAL":    "#e74c3c",
    "WARNING":     "#f39c12",
    "PRE-WARNING": "#3498db",
    "INFO":        "#2ecc71",
}

SEVERITY_BADGE = {
    "CRITICAL":    "🔴 CRITICAL",
    "WARNING":     "🟡 WARNING",
    "PRE-WARNING": "🔵 PRE-WARNING",
    "INFO":        "🟢 INFO",
}

st.set_page_config(
    page_title="Smart Grid Monitor",
    page_icon="⚡",
    layout="wide",
)

@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data(path: str) -> pd.DataFrame:
    """Load and parse CSV report. Returns empty DataFrame if file not found."""
    if not Path(path).exists():
        return pd.DataFrame()
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["voltage"] = pd.to_numeric(df["voltage"], errors="coerce")
    df["severity"] = pd.Categorical(df["severity"], categories=SEVERITY_ORDER, ordered=True)
    return df


df = load_data(CSV_PATH)

st.title("⚡ Smart Grid Monitor — Dashboard")
st.caption(f"Data source: `{CSV_PATH}` · Auto-refresh every {REFRESH_INTERVAL}s")

if df.empty:
    st.error(
        f"ไม่พบไฟล์ `{CSV_PATH}` — รัน `python scheduler.py` เพื่อสร้างข้อมูลก่อน"
    )
    st.stop()

@st.fragment(run_every=REFRESH_INTERVAL)
def auto_refresh():
    """Re-fetch data silently without resetting scroll position."""
    load_data.clear()

auto_refresh()

st.divider()

# Section 1 — Summary Stats

st.subheader("📊 Section 1 — Summary Stats")
st.caption("ภาพรวมการทำงานของระบบทั้งหมด ตั้งแต่จำนวนรอบที่รัน ไปจนถึงการแจ้งเตือนแยกตามระดับความรุนแรง")

total_rows     = len(df)
total_runs     = df["timestamp"].nunique()
total_critical = len(df[df["severity"] == "CRITICAL"])
total_warning  = len(df[df["severity"] == "WARNING"])
total_pre      = len(df[df["severity"] == "PRE-WARNING"])
total_info     = len(df[df["severity"] == "INFO"])

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Runs",      total_runs)
c2.metric("Total Records",   total_rows)
c3.metric("🔴 CRITICAL",    total_critical)
c4.metric("🟡 WARNING",     total_warning)
c5.metric("🔵 PRE-WARNING", total_pre)
c6.metric("🟢 INFO",        total_info)

# Severity breakdown donut
sev_counts = (
    df["severity"]
    .value_counts()
    .reset_index()
    .rename(columns={"count": "count", "severity": "Severity"})
)
sev_counts.columns = ["Severity", "Count"]

donut = (
    alt.Chart(sev_counts)
    .mark_arc(innerRadius=55)
    .encode(
        theta=alt.Theta("Count:Q"),
        color=alt.Color(
            "Severity:N",
            scale=alt.Scale(
                domain=list(SEVERITY_COLOR.keys()),
                range=list(SEVERITY_COLOR.values()),
            ),
        ),
        tooltip=["Severity:N", "Count:Q"],
    )
    .properties(height=350, title="Severity Breakdown")
)
st.altair_chart(donut, use_container_width=True)

st.divider()

# Section 2 — Live Device Status

st.subheader("📡 Section 2 — Live Device Status")
st.caption("สถานะและค่าเซนเซอร์ของอุปกรณ์แต่ละตัวในรอบล่าสุด")

latest_ts = df["timestamp"].max()
latest_df = df[df["timestamp"] == latest_ts].copy()
latest_df = latest_df.sort_values("severity")

def render_status_card(row):
    """Render a compact status card for one device."""
    color = SEVERITY_COLOR.get(str(row["severity"]), "#95a5a6")
    badge = SEVERITY_BADGE.get(str(row["severity"]), row["severity"])
    temp_str  = f"{row['temperature']:.1f} °C"  if pd.notna(row["temperature"]) else "—"
    volt_str  = f"{row['voltage']:.1f} V"        if pd.notna(row["voltage"])     else "—"
    st.markdown(
        f"""
        <div style="
            border-left: 5px solid {color};
            background: #1e1e2e;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 8px;
        ">
            <div style="font-size:1.05em; font-weight:700; color:#cdd6f4;">
                {row['id']} &nbsp;<span style="font-size:0.8em; color:#a6adc8;">({row['type']})</span>
            </div>
            <div style="font-size:0.82em; color:#a6adc8; margin-bottom:6px;">{row['location']}</div>
            <div style="display:flex; gap:16px; font-size:0.88em; color:#cdd6f4;">
                <span>🌡️ {temp_str}</span>
                <span>⚡ {volt_str}</span>
                <span>🔌 {row['status']}</span>
            </div>
            <div style="margin-top:8px;">
                <span style="
                    background:{color}22;
                    color:{color};
                    border:1px solid {color};
                    border-radius:4px;
                    padding:2px 8px;
                    font-size:0.78em;
                    font-weight:600;
                ">{badge}</span>
                &nbsp;<span style="font-size:0.8em; color:#a6adc8;">{row['reason']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

cols = st.columns(2)
for i, (_, row) in enumerate(latest_df.iterrows()):
    with cols[i % 2]:
        render_status_card(row)

st.caption(f"Timestamp: `{latest_ts}`")

st.divider()

# Section 3 — Temperature Trend

st.subheader("📈 Section 3 — Temperature Trend")
st.caption("ติดตามอุณหภูมิแต่ละอุปกรณ์แบบย้อนหลัง เพื่อสังเกตแนวโน้มการเพิ่มขึ้นก่อนเกิดเหตุ")

all_devices = sorted(df["id"].unique().tolist())
selected_devices = st.multiselect(
    "Select Devices",
    options=all_devices,
    default=all_devices,
    key="trend_devices",
)

trend_df = df[df["id"].isin(selected_devices) & df["temperature"].notna()].copy()

if trend_df.empty:
    st.info("ไม่มีข้อมูลอุณหภูมิสำหรับ device ที่เลือก")
else:
    chart = (
        alt.Chart(trend_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("timestamp:T", title="Time", axis=alt.Axis(format="%H:%M:%S")),
            y=alt.Y(
                "temperature:Q",
                title="Temperature (°C)",
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color("id:N", title="Device"),
            tooltip=[
                alt.Tooltip("timestamp:T", title="Time", format="%Y-%m-%d %H:%M:%S"),
                alt.Tooltip("id:N", title="Device"),
                alt.Tooltip("temperature:Q", title="Temp (°C)", format=".1f"),
                alt.Tooltip("severity:N", title="Severity"),
            ],
        )
        .properties(height=320)
        .interactive()
    )

    threshold_line = (
        alt.Chart(pd.DataFrame({"threshold": [75.0]}))
        .mark_rule(color="#e74c3c", strokeDash=[6, 3], opacity=0.6)
        .encode(y="threshold:Q")
    )

    st.altair_chart(chart + threshold_line, use_container_width=True)
    st.caption("เส้นประแดง = Transformer threshold (75°C)")

st.divider()

# Section 4 — Alert History

st.subheader("🚨 Section 4 — Alert History")
st.caption("รายการแจ้งเตือนทั้งหมดที่เกิดขึ้นในระบบ")

col_sev, col_dev = st.columns(2)

with col_sev:
    severity_options = [s for s in SEVERITY_ORDER if s in df["severity"].unique().tolist()]
    selected_severity = st.selectbox(
        "Severity",
        options=["ALL"] + severity_options,
        index=0,
        key="alert_severity",
    )

with col_dev:
    selected_alert_devices = st.multiselect(
        "Select Device",
        options=all_devices,
        default=all_devices,
        key="alert_devices",
    )

if selected_severity == "ALL":
    alert_df = df.copy()
else:
    alert_df = df[df["severity"] == selected_severity].copy()

alert_df = alert_df[alert_df["id"].isin(selected_alert_devices)]
alert_df = alert_df.sort_values("timestamp", ascending=False)

display_alert = alert_df[["timestamp", "id", "type", "location", "temperature", "voltage", "status", "severity", "reason"]].copy()
display_alert["temperature"] = display_alert["temperature"].map(lambda x: f"{x:.1f}" if pd.notna(x) else "—")
display_alert["voltage"]     = display_alert["voltage"].map(lambda x: f"{x:.1f}" if pd.notna(x) else "—")
display_alert.columns = ["Timestamp", "ID", "Type", "Location", "Temp (°C)", "Voltage (V)", "Status", "Severity", "Reason"]

st.dataframe(
    display_alert,
    use_container_width=True,
    height=300,
    hide_index=True,
)
st.caption(f"แสดง {len(display_alert):,} รายการ")

st.divider()

# Section 5 — Pattern Analysis

st.subheader("🔍 Section 5 — Pattern Analysis")
st.caption("อุปกรณ์ที่เกิดการแจ้งเตือนบ่อยที่สุด จำแนกตามระดับความรุนแรง")

pattern_df = (
    df[df["severity"].isin(["WARNING", "CRITICAL", "PRE-WARNING"])]
    .groupby(["id", "severity"], observed=True)
    .size()
    .reset_index(name="count")
)

if pattern_df.empty:
    st.info("ยังไม่มีข้อมูล alert")
else:
    bar = (
        alt.Chart(pattern_df)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Alert Count"),
            y=alt.Y("id:N", sort="-x", title="Device"),
            color=alt.Color(
                "severity:N",
                scale=alt.Scale(
                    domain=list(SEVERITY_COLOR.keys()),
                    range=list(SEVERITY_COLOR.values()),
                ),
                title="Severity",
            ),
            tooltip=["id:N", "severity:N", "count:Q"],
        )
        .properties(height=280, title="Alert Frequency by Device")
    )
    st.altair_chart(bar, use_container_width=True)

    # Top 5 devices by alert count
    top5 = (
        pattern_df.groupby("id")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    lines = "\n".join(
        f"{rank + 1}. **{dev_id}** — {cnt} ครั้ง"
        for rank, (dev_id, cnt) in enumerate(top5.items())
    )
    st.warning(f"⚠️ Device ที่มี alert บ่อยที่สุด\n\n{lines}")

st.divider()
st.caption("Smart Grid Monitor · Designed, Developed and Maintained by Phuriphat Rattanatham")