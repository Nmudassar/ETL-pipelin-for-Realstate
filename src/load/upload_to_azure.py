from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient


# Step 1: Storage account name
storage_account_name = "stpropertyetlnadia01"


# Step 2: Azure Data Lake account URL
account_url = (
    f"https://{storage_account_name}.dfs.core.windows.net"
)


# Step 3: Authenticate using your Azure login
credential = DefaultAzureCredential()


# Step 4: Connect to Azure Data Lake
service_client = DataLakeServiceClient(
    account_url=account_url,
    credential=credential,
)


# Step 5: Connect to property-data container
file_system_client = service_client.get_file_system_client(
    file_system="property-data"
)


# Step 6: Reusable upload function
def upload_file(local_file_path, azure_file_path):

    file_client = file_system_client.get_file_client(
        azure_file_path
    )

    with open(local_file_path, "rb") as local_file:
        file_client.upload_data(
            local_file,
            overwrite=True,
        )

    print("Uploaded:", azure_file_path)


# Step 7: Upload Bronze Land Registry
upload_file(
    "data/bronze/land_registry/pp-monthly-update-new-version.csv",
    "bronze/land_registry/pp-monthly-update-new-version.csv",
)


# Step 8: Upload Bronze EPC
upload_file(
    "data/bronze/epc/epc_energy_efficient_raw.json",
    "bronze/epc/epc_energy_efficient_raw.json",
)


# Step 9: Upload Silver Land Registry
upload_file(
    "data/silver/land_registry/land_registry_cleaned.parquet",
    "silver/land_registry/land_registry_cleaned.parquet",
)


# Step 10: Upload Silver EPC
upload_file(
    "data/silver/epc/epc_energy_efficient_cleaned.parquet",
    "silver/epc/epc_energy_efficient_cleaned.parquet",
)


# Step 11: Upload Gold dataset
upload_file(
    "data/gold/property_energy/property_energy_gold.parquet",
    "gold/property_energy_gold.parquet",
)


print("\nAll property ETL files uploaded successfully.")