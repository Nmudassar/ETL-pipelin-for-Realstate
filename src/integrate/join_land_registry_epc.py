import pandas as pd


# Step 1: Define Silver file paths
land_registry_file = (
    "data/silver/land_registry/"
    "land_registry_cleaned.parquet"
)

epc_file = (
    "data/silver/epc/"
    "epc_energy_efficient_cleaned.parquet"
)


# Step 2: Read Land Registry Silver data
land_df = pd.read_parquet(land_registry_file)


# Step 3: Read EPC Silver data
epc_df = pd.read_parquet(epc_file)


# Step 4: Check dataset sizes
print("\nLand Registry shape:", land_df.shape)
print("EPC shape:", epc_df.shape)


# Step 5: Show sample Land Registry postcodes
print("\nSample Land Registry postcodes:")
print(land_df["postcode"].dropna().head(10))


# Step 6: Check EPC postcodes that exist in Land Registry
matching_postcodes = epc_df[
    epc_df["postcode"].isin(land_df["postcode"])
]

print("\nEPC records with matching Land Registry postcodes:")
print(matching_postcodes.shape[0])