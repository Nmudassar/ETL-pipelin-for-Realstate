import pandas as pd


# Silver file path 
silver_file_path = "data/silver/land_registry/land_registry_cleaned.parquet"


# Read silver parquet file
df = pd.read_parquet(
    silver_file_path,
)


# step 1: Show first five records of the silver dataset
print("\nFirst 5 rows of the Silver dataset:")
print(df.head())

# Step 2: check the number and column of the silver dataset
print("\nSliver dataset shape:")
print (df.shape)

#step 3: check the columns names
print("\ncolumn names of the Silver dataset:")
print(df.columns)

#step 4: # Check data types
print("\nSilver data types:")
print(df.dtypes)


# Check missing postcodes
print("\nMissing postcodes:")
print(df["postcode"].isnull().sum())


# Check duplicate transaction IDs
print("\nDuplicate transaction IDs:")
print(df["transaction_id"].duplicated().sum())

