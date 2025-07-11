import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', 100)


filename = 'final.csv'  
df = pd.read_csv(filename)

df_filtered = df[df['stars'] >= 0].copy()

# Convert date columns to datetime, handling any parsing errors
df_filtered['first_commit'] = pd.to_datetime(df_filtered['first_commit'], errors='coerce', utc=True)
df_filtered['latest_commit'] = pd.to_datetime(df_filtered['latest_commit'], errors='coerce', utc=True)
df_filtered['introduced_at'] = pd.to_datetime(df_filtered['introduced_at'], errors='coerce', utc=True)

# Drop any rows where date conversion failed (if any)
df_filtered = df_filtered.dropna(subset=['first_commit', 'latest_commit', 'introduced_at'])

# Calculate total days and days to introduced
df_filtered['total_days'] = (df_filtered['latest_commit'] - df_filtered['first_commit']).dt.days
df_filtered['days_to_introduced'] = (df_filtered['introduced_at'] - df_filtered['first_commit']).dt.days

# Calculate dev percentage
df_filtered['dev_percentage'] = np.where(
    df_filtered['total_days'] > 0,
    (df_filtered['days_to_introduced'] / df_filtered['total_days']) * 100,
    np.nan
)
df_filtered['dev_percentage'] = df_filtered['dev_percentage'].clip(lower=0, upper=100)

days_stats = df_filtered['days_to_introduced'].agg(['min', 'max', 'median', 'mean'])
percentage_stats = df_filtered['dev_percentage'].agg(['min', 'max', 'median', 'mean'])

# Display results
print("=== FILTERED DATA OVERVIEW ===")
print(f"Original rows: {df.shape[0]}, Filtered rows: {df_filtered.shape[0]}")
print("\nStats for Days to Introduced:")
print(days_stats)
print("\nStats for Dev % Time:")
print(percentage_stats)
print("\nSample of calculated metrics (first 5 rows):")
print(df_filtered[['REPO', 'days_to_introduced', 'total_days', 'dev_percentage']].head())


days_quartiles = df_filtered['days_to_introduced'].quantile([0.25, 0.5, 0.75])
percentage_quartiles = df_filtered['dev_percentage'].quantile([0.25, 0.5, 0.75])

extreme_days = df_filtered.nlargest(5, 'days_to_introduced')[['REPO', 'days_to_introduced', 'dev_percentage']]
extreme_days_min = df_filtered.nsmallest(5, 'days_to_introduced')[['REPO', 'days_to_introduced', 'dev_percentage']]

# Print additional insights
print("=== ADDITIONAL ANALYSIS ===")
print("\nQuartiles for Days to Introduced:")
print(days_quartiles)
print("\nQuartiles for Dev % Time:")
print(percentage_quartiles)
print("\nTop 5 Repos with Maximum Days to Introduced:")
print(extreme_days)
print("\nTop 5 Repos with Minimum Days to Introduced:")
print(extreme_days_min)