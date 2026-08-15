import os

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv


# Step 1: Load environment variables
load_dotenv()


# Step 2: Read Azure settings
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
file_system_name = os.getenv("AZURE_FILE_SYSTEM")


# Step 3: Check settings exist
if not storage_account_name:
    raise ValueError("AZURE_STORAGE_ACCOUNT was not found in .env")

if not file_system_name:
    raise ValueError("AZURE_FILE_SYSTEM was not found in .env")


# Step 4: Create Azure Data Lake URL
account_url = (
    f"https://{storage_account_name}.dfs.core.windows.net"
)


# Step 5: Authenticate
credential = DefaultAzureCredential()


# Step 6: Connect to Azure Data Lake
service_client = DataLakeServiceClient(
    account_url=account_url,
    credential=credential,
)


# Step 7: Connect to container
file_system_client = service_client.get_file_system_client(
    file_system=file_system_name
)


# Step 8: Create reusable upload function
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


# Step 9: Upload Bronze Land Registry
upload_file(
    "data/bronze/land_registry/pp-monthly-update-new-version.csv",
    "bronze/land_registry/pp-monthly-update-new-version.csv",
)


# Step 10: Upload Bronze EPC
upload_file(
    "data/bronze/epc/epc_energy_efficient_raw.json",
    "bronze/epc/epc_energy_efficient_raw.json",
)


# Step 11: Upload Silver Land Registry
upload_file(
    "data/silver/land_registry/land_registry_cleaned.parquet",
    "silver/land_registry/land_registry_cleaned.parquet",
)


# Step 12: Upload Silver EPC
upload_file(
    "data/silver/epc/epc_energy_efficient_cleaned.parquet",
    "silver/epc/epc_energy_efficient_cleaned.parquet",
)


# Step 13: # Upload Gold analytics dataset
upload_file(
    "data/gold/property_analytics/property_analytics_gold.parquet",
    "gold/property_analytics/property_analytics_gold.parquet",
)


print("\nAll property ETL files uploaded successfully.")