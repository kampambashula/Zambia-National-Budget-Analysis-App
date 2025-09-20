import pandas as pd

# Load the ENSO CSV
file_path = "data/clean.csv"  # replace with your actual file path
df = pd.read_csv(file_path)

# Convert 'Month' column to datetime (format: MonthName-Year)
df['Month'] = pd.to_datetime(df['Month'], format='%B-%Y')  # %B = full month name, %Y = year

# Extract year and month
df['Year'] = df['Month'].dt.year
df['Month_Num'] = df['Month'].dt.month  # optional, numeric month

# Calculate annual average of SOI
annual_enso = df.groupby('Year')['soi_index'].mean().reset_index()

# Filter for 2007 to 2025
annual_enso = annual_enso[(annual_enso['Year'] >= 2007) & (annual_enso['Year'] <= 2025)]

# Optional: round values
annual_enso['soi_index'] = annual_enso['soi_index'].round(3)

# Save to CSV
output_file = "enso_annual_2007_2025.csv"
annual_enso.to_csv(output_file, index=False)

print(f"Annual ENSO data (2007–2025) saved to {output_file}")
