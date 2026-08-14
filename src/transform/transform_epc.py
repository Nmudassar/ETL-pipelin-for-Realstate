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
print("\nFirst % records of the epc dataset:")
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