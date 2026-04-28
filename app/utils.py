"""
utils.py — Data loading and processing utilities for the COP32 Climate Dashboard.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

COUNTRIES = ['Ethiopia', 'Kenya', 'Sudan', 'Tanzania', 'Nigeria']

COUNTRY_COLORS = {
    'Ethiopia':  '#E63946',
    'Kenya':     '#2A9D8F',
    'Sudan':     '#E9C46A',
    'Tanzania':  '#457B9D',
    'Nigeria':   '#6A4C93'
}

VARIABLE_LABELS = {
    'T2M':          'Mean Temperature (°C)',
    'T2M_MAX':      'Max Temperature (°C)',
    'T2M_MIN':      'Min Temperature (°C)',
    'T2M_RANGE':    'Temperature Range (°C)',
    'PRECTOTCORR':  'Precipitation (mm/day)',
    'RH2M':         'Relative Humidity (%)',
    'WS2M':         'Wind Speed (m/s)',
    'WS2M_MAX':     'Max Wind Speed (m/s)',
    'QV2M':         'Specific Humidity (g/kg)',
    'PS':           'Surface Pressure (kPa)',
}

DATA_DIR = Path(__file__).parent.parent / 'data'


def load_country(country: str):
    path = DATA_DIR / f'{country.lower()}_clean.csv'
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=['Date'])
    df['Country'] = country
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df


def load_all(countries=None):
    if countries is None:
        countries = COUNTRIES
    frames = []
    for c in countries:
        df = load_country(c)
        if df is not None:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def monthly_avg(df, variable):
    grouped = (
        df.groupby(['Country', df['Date'].dt.to_period('M')])[variable]
        .mean()
        .reset_index()
    )
    grouped.columns = ['Country', 'Period', variable]
    grouped['Date'] = grouped['Period'].dt.to_timestamp()
    return grouped


def yearly_extreme_heat(df, threshold=35.0):
    hot = df[df['T2M_MAX'] > threshold]
    result = hot.groupby(['Country', 'Year']).size().reset_index(name='ExtremeHeatDays')
    return result


def max_consecutive_dry(series, threshold=1.0):
    dry = (series < threshold).astype(int)
    max_streak = streak = 0
    for v in dry:
        if v:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return max_streak


def yearly_dry_spells(df):
    result = (
        df.groupby(['Country', 'Year'])['PRECTOTCORR']
        .apply(max_consecutive_dry)
        .reset_index()
    )
    result.columns = ['Country', 'Year', 'MaxDryDays']
    return result


def filter_year_range(df, start_year, end_year):
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]


def summary_stats(df, variable):
    return (
        df.groupby('Country')[variable]
        .agg(Mean='mean', Median='median', Std='std')
        .round(3)
        .sort_values('Mean', ascending=False)
    )