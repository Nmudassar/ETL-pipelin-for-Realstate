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

# Basic source profiling
print("\nMissing values:")
print(df.isnull().sum())


print("\nDuplicate transaction IDs:")
print(df["transaction_id"].duplicated().sum())

