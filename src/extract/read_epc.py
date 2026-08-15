import os
import requests
import pandas as pd
import json
from dotenv import load_dotenv
# Step 1: Load variables from the .env file
load_dotenv()

# Step 2: Read the EPC API token
epc_token = os.getenv("EPC_API_TOKEN")

# Step 3: Check that the token was loaded
if not epc_token:
    raise ValueError("EPC_API_TOKEN was not found in the .env file")

print("EPC API token loaded successfully")

# step 4 : EPC deomstice search endpoint
url = "https://api.get-energy-performance-data.communities.gov.uk/api/domestic/search"

# step 5: 
headers = {
    "Authorization": f"Bearer {epc_token}",
    "Accept" : "application/json",
}

# Step 6: Read Land Registry Silver data
land_df = pd.read_parquet(
    "data/silver/land_registry/land_registry_cleaned.parquet"
)


# Step 7: Get first 10 unique postcodes
postcodes = (
    land_df["postcode"]
    .dropna()
    .drop_duplicates()
    .head(10)
    .tolist()
)

print("\nPostcodes to search:")
print(postcodes)


# Step 8: Store all EPC records
all_records = []


# Step 9: Loop through each postcode
for postcode in postcodes:

    params = [
        ("postcode", postcode),
        ("efficiency_rating[]", "A"),
        ("efficiency_rating[]", "B"),
        ("efficiency_rating[]", "C"),
        ("current_page", 1),
        ("page_size", 10),
    ]

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=60,
        )

        print("\nSearching postcode:", postcode)
        print("Status code:", response.status_code)

        # No EPC found for this postcode
        if response.status_code == 404:
            print("No EPC records found.")
            continue

        response.raise_for_status()

    except requests.exceptions.ReadTimeout:
        print("Request timed out for:", postcode)
        continue


# Step 10: Convert API response to Python data
    data = response.json()


# Step 11: Extract EPC certificate records
    records = data["data"]


# Step 12: Add these records to all_records
    all_records.extend(records)

print("EPC records found:", len(records))


# Step 13: Convert all EPC records into a DataFrame
epc_df = pd.DataFrame(all_records)

# Step 14: Show the first 5 EPC records
print("\nFirst 5 EPC records:")
print(epc_df.head())


# Step 15: Show the shape of the EPC dataset
print("\nEPC dataset shape:")
print(epc_df.shape)


# Step 16: Show EPC column names
print("\nEPC column names:")
print(epc_df.columns)


# Step 17: Show EPC data types
print("\nEPC data types:")
print(epc_df.dtypes)

# Step 18: Define the Bronze EPC output file
bronze_epc_file = "data/bronze/epc/epc_energy_efficient_raw.json"

# Step 19: Save all EPC records to Bronze JSON
with open(bronze_epc_file, "w") as file:
    json.dump(
        {"data": all_records},
        file,
        indent=4
    )


# Step 20: Confirm that the Bronze file was created
print("\nEPC Bronze file created successfully.")
print("Saved to:", bronze_epc_file)