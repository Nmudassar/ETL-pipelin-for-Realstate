import json
import pandas as pd

bronze_file_path = "data/bronze/epc/epc_energy_efficient_raw.json"

# step 2: read the raw Bronze EPC data from the JSON file
with open(bronze_file_path, "r") as file:
    epc_data = json.load(file)


# step 3: extract data from EPC Certificate record

records = epc_data["data"]

# Step 4: Convert the records into a panada DataFrame
df = pd.DataFrame(records)

#Step 5: Show first 5 records
print("\nFirst five records of the epc dataset:")
print(df.head()
      )

# Step 6: Show the number of rows and columns
print("\nEPC dataset shape:", df.shape)

print("\nEPC columns names:", df.columns)

print("\nEPC data type :", df.dtypes)


# Step 9: Rename EPC columns to snake_case
df = df.rename(columns={
    "certificateNumber": "certificate_number",
    "addressLine1": "address_line_1",
    "addressLine2": "address_line_2",
    "addressLine3": "address_line_3",
    "addressLine4": "address_line_4",
    "postTown": "post_town",
    "currentEnergyEfficiencyBand": "current_energy_efficiency_band",
    "registrationDate": "registration_date",
    "schemaType": "schema_type",
})

print("\nEPC columns names:", df.columns)

 
# Step 10: Convert registration_date to datetime
df["registration_date"] = pd.to_datetime(
    df["registration_date"],
    errors="coerce"
)

# Step 11: Check registration_date data type
print("\nRegistration date datatype:")
print(df["registration_date"].dtype)

# Step 12: Check for invalid registration dates
print("\nInvalid registration dates:")
print(df["registration_date"].isnull().sum())

# Step 13: Check energy efficiency ratings
print("\nEnergy efficiency ratings:")
print(df["current_energy_efficiency_band"].value_counts())

# Step 14: Check invalid energy ratings
valid_ratings = ["A", "B", "C"]

print("\nInvalid energy ratings:")
print((~df["current_energy_efficiency_band"].isin(valid_ratings)).sum())

# Step 15: Clean postcode
df["postcode"] = (
    df["postcode"]
    .str.strip()
    .str.upper()
)

# Step 16: Check missing postcodes
print("\nMissing EPC postcodes:")
print(df["postcode"].isnull().sum())

# Step 17: Show cleaned postcodes
print("\nCleaned EPC postcodes:")
print(df["postcode"].head())

# Step 18: Create full EPC address
address_columns = [
    "address_line_1",
    "address_line_2",
    "address_line_3",
    "address_line_4",
    "post_town",
    "postcode",
]

df["full_address"] = df[address_columns].apply(
    lambda row: ", ".join(row.dropna().astype(str)),
    axis=1
)

# Step 19: Show sample full addresses
print("\nSample EPC full addresses:")
print(df["full_address"].head())
  
# Step 20: Check duplicate certificate numbers
print("\nDuplicate certificate numbers:")
print(df["certificate_number"].duplicated().sum())

# Step 22: Define Silver EPC output path
silver_file_path = "data/silver/epc/epc_energy_efficient_cleaned.parquet"


# Step 23: Save cleaned EPC data as Parquet
df.to_parquet(
    silver_file_path,
    index=False
)


# Step 24: Confirm Silver file was created
print("\nEPC Silver dataset created successfully.")
print("Saved to:", silver_file_path)