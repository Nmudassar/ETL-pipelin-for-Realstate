import pandas as pd


# Step1 :Column names for HM Land Registry Price Paid Data
columns = [
    "transaction_id",
    "price",
    "transfer_date",
    "postcode",
    "property_type",
    "old_new",
    "tenure",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category",
    "record_status",
]


#step 2:  Location of the raw Land Registry CSV
file_path = "data/bronze/land_registry/pp-monthly-update-new-version.csv"


# step 3: Read the CSV into a Pandas DataFrame
df = pd.read_csv(
    file_path,
    names=columns,
    header=None,
)


# step 4: Show the first 5 property records
print("\nFirst 5 rows:")
print(df.head())


# step 5:Show the number of rows and columns
print("\nDataset shape:")
print(df.shape)


# step 6: Show all column names
print("\nColumn names:")
print(df.columns)


# step 7: Show the data type of each column
print("\nData Types:")
print(df.dtypes)

# step 8: convert the transfer_date column to datetime format
df["transfer_date"] = pd.to_datetime(
    df["transfer_date"],
    errors="coerce"
)

# step 9: Check the datatype after conversion
print("\nTransfer date datatype after conversion:")
print(df["transfer_date"].dtype)

# step 10: Count any dates that could not be converted
print("\nInvalid transfer dates:")
print(df["transfer_date"].isnull().sum())

# step 11: check the current data type in price column
print("\nPrice datatype")
print(df["price"].dtype)

# step 12; Count hte missing price values
print("\nMissing price values")
print(df["price"].isnull().sum())

# step13:Count invalid prices that are zero or negative
print("\nInvalid price values:")
print((df["price"] <= 0).sum())

# step 14: convert the coded property values into readable descriptions.
propery_type_mapping = {
    "D" : "Detached",
    "S" : "Semi-Detached",
    "T" : "Terraced",
    "F" : "Flats/Maisonettes",
    "O" : "Other"
}
df["property_type"] = df["property_type"].map(propery_type_mapping)

#step 15: # Show property type values after transformation
print("\nProperty types after transformation:")
print(df["property_type"].value_counts())

#step 16:  Convert old/new property codes into readable descriptions
property_age_mapping = {
    "Y" : "New",
    "N" : "Existing",
}

df["old_new"] = df["old_new"].map(property_age_mapping)

print("\nOld/New values after transformation:")
print(df["old_new"].value_counts())

# step 17: Convert tenure codes into readable descriptions
tenure_mapping = {
    "F" : "Freehold",
    "L" : "Leasehold",
}

df["tenure"] = df["tenure"].map(tenure_mapping)

print("\nTenure values after transformation:")
print(df["tenure"].value_counts())

# step 18: Create a full address from the separate address columns.For every property row, take the address fields, remove missing values, convert the remaining values to text, join them with commas, and save the result in a new column called full_address.
address_columns = [
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "postcode",
]
# Create full address and ignore missing address parts
df["full_address"] = df[address_columns].apply(
    lambda row: ", ".join(row.dropna().astype(str)),
    axis=1
)


# Show the first 10 full addresses
print("\nSample full addresses:")
print(df["full_address"].head(10))

# step 19: Clean the postcode
df["postcode"] = (
    df ["postcode"]
    .str.strip() # remove leading and trailing whitespace
    .str.upper() # convert to uppercase
)

# Show sample postcodes after cleaning
print("\nCleaned postcodes:")
print(df["postcode"].head(10))


# Count properties with missing postcodes
print("\nMissing postcodes:")
print(df["postcode"].isnull().sum())

# step 20: Count the duplicate transcations ID
print("\nDuplicate transaction IDs:")
print(df["transaction_id"].duplicated().sum())

# step 21: Because postcode will be important later when joining with EPC and ONS data, we should understand those 296 missing records before deciding what to do with them.
# 21a: Find rows where postcode is missing

missing_postcodes = df [df["postcode"].isnull()]

print("\nRows with the missing postcodes:")
print(missing_postcodes.shape[0])

print("\nSample record with missing postcodes")
print(
    missing_postcodes[
        [
            "transaction_id",
            "paon",
            "saon",
            "street",
            "locality",
            "town_city",
            "county",
            "postcode"
        ]
    ].head(10)
)
    #A better Data Engineering approach is to keep them and flag them.

# Step  — Create a postcode quality flag

# Create a flag whter property have postcode or not 
df["has_postcode"] = df["postcode"].notnull()

print('\nPostcode availability flag:')
print(df["has_postcode"].value_counts())
