import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Set page title dan icon
st.set_page_config(
    page_title='GDP Dashboard',
    page_icon='🌎',
    layout='wide'
)

# -----------------------
# Ambil data GDP (CSV)
@st.cache_data(ttl=86400)
def load_gdp_data():
    DATA_PATH = Path(__file__).parent / 'data' / 'gdp_data.csv'

    if not DATA_PATH.exists():
        st.error("File gdp_data.csv tidak ditemukan di folder /data.")
        return pd.DataFrame()  # return kosong

    raw_df = pd.read_csv(DATA_PATH)

    # Range tahun
    MIN_YEAR, MAX_YEAR = 1960, 2022

    # Transform pivot ke format long
    df = raw_df.melt(
        id_vars=['Country Name', 'Country Code'],
        value_vars=[str(year) for year in range(MIN_YEAR, MAX_YEAR + 1)],
        var_name='Year',
        value_name='GDP'
    )
    df['Year'] = pd.to_numeric(df['Year'])
    df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')  # safe convert
    return df

gdp_df = load_gdp_data()

# -----------------------
# UI dan logika
st.title("🌍 GDP Dashboard")
st.markdown("Data dari [World Bank](https://data.worldbank.org/).")

if gdp_df.empty:
    st.stop()

# Slider tahun
min_year, max_year = int(gdp_df['Year'].min()), int(gdp_df['Year'].max())
from_year, to_year = st.slider("Pilih rentang tahun", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Multiselect negara
countries = sorted(gdp_df['Country Code'].unique())
selected = st.multiselect("Pilih negara", countries, default=['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# Filter data
filtered_df = gdp_df[
    (gdp_df['Country Code'].isin(selected)) &
    (gdp_df['Year'] >= from_year) &
    (gdp_df['Year'] <= to_year)
]

# -----------------------
# Grafik
st.header("📈 GDP dari tahun ke tahun")
if filtered_df.empty:
    st.warning("Data kosong untuk filter yang dipilih.")
else:
    st.line_chart(
        filtered_df,
        x='Year',
        y='GDP',
        color='Country Code'
    )

# -----------------------
# Perbandingan GDP awal vs akhir
st.header(f"📊 Perbandingan GDP {from_year} vs {to_year}")
col_grid = st.columns(4)

for i, country in enumerate(selected):
    col = col_grid[i % 4]
    with col:
        first = gdp_df[(gdp_df['Country Code'] == country) & (gdp_df['Year'] == from_year)]
        last = gdp_df[(gdp_df['Country Code'] == country) & (gdp_df['Year'] == to_year)]

        if not first.empty and not last.empty:
            gdp_first = first['GDP'].values[0] / 1e9
            gdp_last = last['GDP'].values[0] / 1e9

            if np.isnan(gdp_first) or gdp_first == 0:
                growth = 'n/a'
                delta_color = 'off'
            else:
                growth = f"{gdp_last / gdp_first:.2f}x"
                delta_color = 'normal'

            st.metric(
                label=f"{country} GDP",
                value=f"{gdp_last:,.0f} B",
                delta=growth,
                delta_color=delta_color
            )
        else:
            st.metric(
                label=f"{country} GDP",
                value="n/a",
                delta="no data",
                delta_color="off"
            )
