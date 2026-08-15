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

# Number of Land Registry postcodes to process
POSTCODE_LIMIT = 10

# Step 7: Get first 10 unique postcodes
postcodes = (
    land_df["postcode"]
    .dropna()
    .drop_duplicates()
    .head(POSTCODE_LIMIT)
    .tolist()
)

print("\nPostcodes to search:")
print(postcodes)


# Step 8: Store all EPC records
all_records = []


# Step 9: Loop through each postcode
for postcode in postcodes:

    current_page = 1

    while True:

        params = [
            ("postcode", postcode),
            ("efficiency_rating[]", "A"),
            ("efficiency_rating[]", "B"),
            ("efficiency_rating[]", "C"),
            ("current_page", current_page),
            ("page_size", 10),
        ]

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=60,
            )

            print(
                "\nSearching postcode:",
                postcode,
                "- page:",
                current_page,
            )

            print("Status code:", response.status_code)

            # No EPC records found for this postcode
            if response.status_code == 404:
                print("No EPC records found.")
                break

            response.raise_for_status()

            # Step 10: Convert API response to Python data
            data = response.json()

            # Step 11: Extract EPC certificate records
            records = data["data"]

            # Step 12: Add records from this page
            all_records.extend(records)

            print("EPC records found:", len(records))

            # Step 13: Check if another page exists
            next_page = data["pagination"]["nextPage"]

            # Stop pagination if there is no next page
            if next_page is None:
                break

            # Move to the next page
            current_page = next_page

        except requests.exceptions.ReadTimeout:
            print("Request timed out for:", postcode)
            break


# Step 14: Show total EPC records collected
print("\nTotal EPC records extracted:")
print(len(all_records))


# Step 15: Convert all EPC records into a DataFrame
epc_df = pd.DataFrame(all_records)


# Step 16: Show the shape of the EPC dataset
print("\nEPC dataset shape:")
print(epc_df.shape)


# Step 17: Show EPC column names
print("\nEPC column names:")
print(epc_df.columns)


# Step 18: Show EPC data types
print("\nEPC data types:")
print(epc_df.dtypes)

# Step 19: Define the Bronze EPC output file
bronze_epc_file = "data/bronze/epc/epc_energy_efficient_raw.json"

# Step 20: Save all EPC records to Bronze JSON
with open(bronze_epc_file, "w") as file:
    json.dump(
        {"data": all_records},
        file,
        indent=4
    )


# Step 21: Confirm that the Bronze file was created
print("\nEPC Bronze file created successfully.")
print("Saved to:", bronze_epc_file)