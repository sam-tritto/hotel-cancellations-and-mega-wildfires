import os
import urllib.request
import pandas as pd
import numpy as np

DATA_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv"

def download_dataset(target_path="data/hotels.csv"):
    """
    Downloads the Hotel Booking Demand dataset if it doesn't already exist.
    """
    if os.path.exists(target_path):
        return target_path

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    print(f"Downloading dataset from {DATA_URL} to {target_path}...")
    
    req = urllib.request.Request(
        DATA_URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
        out_file.write(response.read())
        
    print("Download complete.")
    return target_path

def load_and_preprocess_raw_data(file_path="data/hotels.csv"):
    """
    Loads the raw hotel booking dataset, converts dates, and does basic cleaning.
    """
    df = pd.read_csv(file_path)
    
    # Map month name to number
    months = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df['arrival_date_month_num'] = df['arrival_date_month'].map(months)
    
    # Build proper arrival date
    df['arrival_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + '-' +
        df['arrival_date_month_num'].astype(str) + '-' +
        df['arrival_date_day_of_month'].astype(str),
        format='%Y-%m-%d',
        errors='coerce'
    )
    
    # Drop rows where date couldn't be parsed
    df = df.dropna(subset=['arrival_date'])
    
    # Define week start date (Monday of the arrival week)
    df['week_start'] = df['arrival_date'].dt.to_period('W').dt.start_time
    
    return df

def build_weekly_panel(df, market_segment='Groups', country_group=None):
    """
    Aggregates the individual booking rows into a weekly panel dataset tracking
    booking cancellations at the hotel level.
    """
    df_filtered = df.copy()
    
    if market_segment:
        df_filtered = df_filtered[df_filtered['market_segment'] == market_segment]
        
    if country_group:
        df_filtered = df_filtered[df_filtered['country'].isin(country_group)]
        
    all_weeks = pd.date_range(start=df['week_start'].min(), end=df['week_start'].max(), freq='W-MON')
    hotels = ['Resort Hotel', 'City Hotel']
    
    grid = pd.MultiIndex.from_product([hotels, all_weeks], names=['hotel', 'week_start']).to_frame().reset_index(drop=True)
    
    agg = df_filtered.groupby(['hotel', 'week_start']).agg(
        cancellations=('is_canceled', 'sum'),
        total_bookings=('is_canceled', 'count')
    ).reset_index()
    
    panel_df = pd.merge(grid, agg, on=['hotel', 'week_start'], how='left').fillna(0)
    
    panel_df['treat'] = (panel_df['hotel'] == 'Resort Hotel').astype(int)
    panel_df['post'] = (panel_df['week_start'] >= '2017-06-12').astype(int)
    panel_df['treat_post'] = panel_df['treat'] * panel_df['post']
    
    unique_weeks = sorted(panel_df['week_start'].unique())
    week_to_idx = {week: idx for idx, week in enumerate(unique_weeks)}
    panel_df['week_idx'] = panel_df['week_start'].map(week_to_idx)
    panel_df['hotel_id'] = (panel_df['hotel'] == 'Resort Hotel').astype(int)
    
    shock_week_idx = week_to_idx[pd.Timestamp('2017-06-12')]
    panel_df['first_treated_week'] = np.where(panel_df['treat'] == 1, shock_week_idx, 0)
    
    panel_df = panel_df.sort_values(['hotel', 'week_start']).reset_index(drop=True)
    return panel_df

def build_multi_unit_panel(df, market_segment='Online TA', countries=None):
    """
    Aggregates the individual booking rows into a multi-unit weekly panel dataset.
    Units are defined by the combination of hotel and country.
    """
    if countries is None:
        countries = ['GBR', 'ESP', 'FRA', 'DEU', 'IRL']
        
    df_filtered = df.copy()
    if market_segment:
        df_filtered = df_filtered[df_filtered['market_segment'] == market_segment]
    df_filtered = df_filtered[df_filtered['country'].isin(countries)]
    
    all_weeks = pd.date_range(start=df['week_start'].min(), end=df['week_start'].max(), freq='W-MON')
    hotels = ['Resort Hotel', 'City Hotel']
    
    grid = pd.MultiIndex.from_product(
        [hotels, countries, all_weeks], 
        names=['hotel', 'country', 'week_start']
    ).to_frame().reset_index(drop=True)
    
    agg = df_filtered.groupby(['hotel', 'country', 'week_start']).agg(
        cancellations=('is_canceled', 'sum'),
        total_bookings=('is_canceled', 'count')
    ).reset_index()
    
    panel_df = pd.merge(grid, agg, on=['hotel', 'country', 'week_start'], how='left').fillna(0)
    
    panel_df['treat'] = (panel_df['hotel'] == 'Resort Hotel').astype(int)
    panel_df['post'] = (panel_df['week_start'] >= '2017-06-12').astype(int)
    panel_df['treat_post'] = panel_df['treat'] * panel_df['post']
    
    unique_weeks = sorted(panel_df['week_start'].unique())
    week_to_idx = {week: idx for idx, week in enumerate(unique_weeks)}
    panel_df['week_idx'] = panel_df['week_start'].map(week_to_idx)
    
    panel_df['unit_str'] = panel_df['hotel'] + "_" + panel_df['country']
    panel_df['unit_id'] = panel_df['unit_str'].astype('category').cat.codes
    
    shock_week_idx = week_to_idx[pd.Timestamp('2017-06-12')]
    panel_df['first_treated_week'] = np.where(panel_df['treat'] == 1, shock_week_idx, 0)
    
    panel_df = panel_df.sort_values(['hotel', 'country', 'week_start']).reset_index(drop=True)
    return panel_df
