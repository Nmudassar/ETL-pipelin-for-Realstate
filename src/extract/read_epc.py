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

# step 6 : Search the filter
params = [
    ("efficiency_rating[]", "A"),
    ("efficiency_rating[]", "B"),
    ("efficiency_rating[]", "C"),
    ("current_page", 1),
    ("page_size", 10),
]

#step 7 : send GET request to the EPC API
try:
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=60,
    )

    # Show the final URL sent to the API
    print("\nRequest URL:")
    print(response.url)

    # Step 8: Print status code
    print("\nStatus code:")
    print(response.status_code)

    # Step 9: Stop if API returned an error
    response.raise_for_status()

except requests.exceptions.ReadTimeout:
    print("\nEPC API request timed out.")
    print("Please try again later.")
    exit()

# Step 10: Convert JSON response into Python data
data = response.json()


# Step 11: Show the response
print("\nEPC API response:")
print(data)

# Step 12: Extract certificate records from the API response
records = data["data"]


# Step 13: Convert the records into a Pandas DataFrame
epc_df = pd.DataFrame(records)

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


# Step 19: Save the raw EPC API response as JSON
with open(bronze_epc_file, "w") as file:
    json.dump(data, file, indent=4)


# Step 20: Confirm that the Bronze file was created
print("\nEPC Bronze file created successfully.")
print("Saved to:", bronze_epc_file)