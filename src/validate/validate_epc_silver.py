import pandas as pd


# Step 1: Define the Silver EPC file path
silver_file_path = "data/silver/epc/epc_energy_efficient_cleaned.parquet"


# Step 2: Read the Silver EPC Parquet file
df = pd.read_parquet(silver_file_path)


# Step 3: Show first 5 records
print("\nFirst 5 EPC Silver records:")
print(df.head())


# Step 4: Check dataset shape
print("\nEPC Silver dataset shape:", df.shape)


# Step 5: Check column names
print("\nEPC Silver columns:")
print(df.columns)


# Step 6: Check data types
print("\nEPC Silver data types:")
print(df.dtypes)


# Step 7: Check invalid registration dates
print("\nInvalid registration dates:")
print(df["registration_date"].isnull().sum())


# Step 8: Check missing postcodes
print("\nMissing postcodes:")
print(df["postcode"].isnull().sum())


# Step 9: Check EPC ratings
print("\nEnergy efficiency ratings:")
print(df["current_energy_efficiency_band"].value_counts(dropna=False))


# Step 10: Check duplicate certificate numbers
print("\nDuplicate certificate numbers:")
print(df["certificate_number"].duplicated().sum())


## Step 11: Check duplicate UPRNs and ignore missing values
duplicate_uprns = (
    df["uprn"]
    .dropna()
    .duplicated()
    .sum()
)

print("\nDuplicate UPRNs:")
print(duplicate_uprns)


print("\nEPC Silver validation completed.")