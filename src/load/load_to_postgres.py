import io
import os

import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient


# Step 1: Load environment variables
load_dotenv()


# Step 2: Read Azure Storage settings
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
file_system_name = os.getenv("AZURE_FILE_SYSTEM")


# Step 3: Read PostgreSQL connection details
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database = os.getenv("POSTGRES_DATABASE")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_port = os.getenv("POSTGRES_PORT")


# Step 4: Check Azure Storage settings
if not storage_account_name:
    raise ValueError(
        "AZURE_STORAGE_ACCOUNT was not found in .env"
    )

if not file_system_name:
    raise ValueError(
        "AZURE_FILE_SYSTEM was not found in .env"
    )


# Step 5: Check PostgreSQL settings
if not postgres_host:
    raise ValueError(
        "POSTGRES_HOST was not found in .env"
    )

if not postgres_database:
    raise ValueError(
        "POSTGRES_DATABASE was not found in .env"
    )

if not postgres_user:
    raise ValueError(
        "POSTGRES_USER was not found in .env"
    )

if not postgres_password:
    raise ValueError(
        "POSTGRES_PASSWORD was not found in .env"
    )

if not postgres_port:
    postgres_port = "5432"


# Step 6: Create Azure Data Lake account URL
account_url = (
    f"https://{storage_account_name}.dfs.core.windows.net"
)


# Step 7: Authenticate to Azure
credential = DefaultAzureCredential()


# Step 8: Connect to Azure Data Lake
service_client = DataLakeServiceClient(
    account_url=account_url,
    credential=credential,
)


# Step 9: Connect to property-data container
file_system_client = service_client.get_file_system_client(
    file_system=file_system_name
)


# Step 10: Define Gold file path in Azure Data Lake
azure_gold_file = (
    "gold/property_analytics/"
    "property_analytics_gold.parquet"
)


# Step 11: Create a client for the Gold file
file_client = file_system_client.get_file_client(
    azure_gold_file
)


# Step 12: Download Gold file from Azure
download = file_client.download_file()


# Step 13: Read downloaded file as bytes
gold_file_bytes = download.readall()


# Step 14: Convert Parquet bytes into a Pandas DataFrame
gold_df = pd.read_parquet(
    io.BytesIO(gold_file_bytes)
)


print(
    "\nGold dataset downloaded from Azure Data Lake."
)

print(
    "Gold dataset shape:",
    gold_df.shape
)


# Step 15: Create PostgreSQL connection URL
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=postgres_user,
    password=postgres_password,
    host=postgres_host,
    port=int(postgres_port),
    database=postgres_database,
)


# Step 16: Create PostgreSQL connection engine
engine = create_engine(
    database_url,
    connect_args={
        "sslmode": "require"
    },
)


# Step 17: Load Gold data into PostgreSQL
gold_df.to_sql(
    name="property_analytics",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
)


print(
    "\nGold dataset loaded into PostgreSQL successfully."
)

print(
    "Table name: property_analytics"
)