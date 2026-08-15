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


# Step 7: Create normalised address key for Land Registry
land_df["address_key"] = (
    land_df["full_address"]
    .str.upper()
    .str.replace(",", "", regex=False)
    .str.replace(" ", "", regex=False)
)


# Step 8: Create normalised address key for EPC
epc_df["address_key"] = (
    epc_df["full_address"]
    .str.upper()
    .str.replace(",", "", regex=False)
    .str.replace(" ", "", regex=False)
)


# Step 9: Join using postcode and normalised address
property_join_df = land_df.merge(
    epc_df,
    on=["postcode", "address_key"],
    how="left",
    suffixes=("_land", "_epc")
)


# Step 10: Keep successful property matches
matched_properties = property_join_df[
    property_join_df["certificate_number"].notnull()
]


# Step 11: Count successful matches
print("\nProperty-level matches:")
print(len(matched_properties))


# Step 12: Show matched property details
print("\nMatched property details:")

print(
    matched_properties[
        [
            "transaction_id",
            "postcode",
            "full_address_land",
            "certificate_number",
            "current_energy_efficiency_band",
            "full_address_epc",
        ]
    ].head(10)
)