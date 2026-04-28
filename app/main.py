"""
main.py — COP32 African Climate Dashboard
10 Academy KAIM9 | Week 0 Bonus

Run with:
    streamlit run app/main.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    load_all, monthly_avg, yearly_extreme_heat, yearly_dry_spells,
    filter_year_range, summary_stats,
    COUNTRIES, COUNTRY_COLORS, VARIABLE_LABELS
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COP32 African Climate Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
    .main-header p  { opacity: 0.75; margin: 0.3rem 0 0; font-size: 0.95rem; }
    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1a1a2e;
        border-left: 4px solid #E63946;
        padding-left: 0.75rem;
        margin: 1.5rem 0 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌍 African Climate Intelligence Dashboard</h1>
    <p>Supporting Ethiopia's data-driven position for COP32 · Addis Ababa 2027</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Controls")

    selected_countries = st.multiselect(
        "🌐 Select Countries",
        options=COUNTRIES,
        default=COUNTRIES,
        help="Choose one or more countries to display"
    )

    year_range = st.slider(
        "📅 Year Range",
        min_value=2015,
        max_value=2026,
        value=(2015, 2026),
        step=1
    )

    selected_variable = st.selectbox(
        "📊 Climate Variable",
        options=list(VARIABLE_LABELS.keys()),
        format_func=lambda x: VARIABLE_LABELS[x],
        index=0
    )

    heat_threshold = st.slider(
        "🌡️ Extreme Heat Threshold (°C)",
        min_value=30,
        max_value=45,
        value=35,
        step=1
    )

    st.markdown("---")
    st.caption("Data: NASA POWER · 2015–2026\nChallenge: 10 Academy KAIM9")

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data(countries):
    return load_all(countries)

if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar.")
    st.stop()

with st.spinner("Loading climate data..."):
    df = get_data(tuple(selected_countries))

if df.empty:
    st.error("❌ No data files found. Make sure cleaned CSVs are in the data/ folder.")
    st.stop()

df = filter_year_range(df, year_range[0], year_range[1])

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Avg Temperature", f"{df['T2M'].mean():.1f}°C")
col2.metric("🌧️ Avg Daily Precip", f"{df['PRECTOTCORR'].mean():.2f} mm")
col3.metric(f"☀️ Days > {heat_threshold}°C", f"{(df['T2M_MAX'] > heat_threshold).mean()*100:.1f}%")
col4.metric("💧 Avg Humidity", f"{df['RH2M'].mean():.1f}%")

# ── Temperature Trend ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Temperature Trend Over Time</div>', unsafe_allow_html=True)

monthly = monthly_avg(df, selected_variable)
fig_temp = go.Figure()
for country in selected_countries:
    cdf = monthly[monthly['Country'] == country].sort_values('Date')
    fig_temp.add_trace(go.Scatter(
        x=cdf['Date'], y=cdf[selected_variable],
        name=country,
        line=dict(color=COUNTRY_COLORS.get(country, '#888'), width=2),
        mode='lines'
    ))

fig_temp.update_layout(
    title=f"Monthly Average {VARIABLE_LABELS[selected_variable]} ({year_range[0]}–{year_range[1]})",
    xaxis_title="Date",
    yaxis_title=VARIABLE_LABELS[selected_variable],
    legend_title="Country",
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)
fig_temp.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
fig_temp.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
st.plotly_chart(fig_temp, use_container_width=True)

# ── Precipitation Boxplot ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">Precipitation Distribution by Country</div>', unsafe_allow_html=True)

fig_box = go.Figure()
for country in selected_countries:
    cdf = df[df['Country'] == country]['PRECTOTCORR'].dropna()
    fig_box.add_trace(go.Box(
        y=cdf,
        name=country,
        marker_color=COUNTRY_COLORS.get(country, '#888'),
        boxmean=True
    ))

fig_box.update_layout(
    title="Daily Precipitation Distribution (mm/day)",
    yaxis_title="PRECTOTCORR (mm/day)",
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white'
)
st.plotly_chart(fig_box, use_container_width=True)

# ── Extreme Events ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Extreme Event Analysis</div>', unsafe_allow_html=True)

col_heat, col_dry = st.columns(2)

with col_heat:
    heat = yearly_extreme_heat(df, threshold=heat_threshold)
    if not heat.empty:
        fig_heat = px.bar(
            heat, x='Year', y='ExtremeHeatDays', color='Country',
            barmode='group',
            color_discrete_map=COUNTRY_COLORS,
            title=f"Extreme Heat Days / Year (T2M_MAX > {heat_threshold}°C)",
            labels={'ExtremeHeatDays': 'Days'}
        )
        fig_heat.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_heat, use_container_width=True)

with col_dry:
    dry = yearly_dry_spells(df)
    if not dry.empty:
        fig_dry = px.bar(
            dry, x='Year', y='MaxDryDays', color='Country',
            barmode='group',
            color_discrete_map=COUNTRY_COLORS,
            title="Max Consecutive Dry Days / Year (< 1mm/day)",
            labels={'MaxDryDays': 'Days'}
        )
        fig_dry.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_dry, use_container_width=True)

# ── Summary Stats Table ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Summary Statistics</div>', unsafe_allow_html=True)

col_t, col_p = st.columns(2)
with col_t:
    st.caption("**Temperature (T2M) — °C**")
    t_stats = summary_stats(df, 'T2M')
    st.dataframe(t_stats, use_container_width=True)

with col_p:
    st.caption("**Precipitation (PRECTOTCORR) — mm/day**")
    p_stats = summary_stats(df, 'PRECTOTCORR')
    st.dataframe(p_stats, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🌍 10 Academy KAIM9 · Week 0 · Data: NASA POWER (2015–2026) · COP32 Addis Ababa 2027")