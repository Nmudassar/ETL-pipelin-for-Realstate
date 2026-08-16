import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Step 1: Load environment variables
load_dotenv()


# Step 2: Read PostgreSQL connection details
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database = os.getenv("POSTGRES_DATABASE")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_port = os.getenv("POSTGRES_PORT")


# Step 3: Check required settings
if not postgres_host:
    raise ValueError("POSTGRES_HOST was not found in .env")

if not postgres_database:
    raise ValueError("POSTGRES_DATABASE was not found in .env")

if not postgres_user:
    raise ValueError("POSTGRES_USER was not found in .env")

if not postgres_password:
    raise ValueError("POSTGRES_PASSWORD was not found in .env")

if not postgres_port:
    postgres_port = "5432"


# Step 4: Define Gold dataset path
gold_file = (
    "data/gold/property_analytics/"
    "property_analytics_gold.parquet"
)


# Step 5: Read Gold dataset
gold_df = pd.read_parquet(gold_file)

print("\nGold dataset loaded successfully.")
print("Gold dataset shape:", gold_df.shape)


# Step 6: Create PostgreSQL connection URL
database_url = (
    f"postgresql+psycopg2://"
    f"{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/"
    f"{postgres_database}"
)


# Step 7: Create SQLAlchemy engine
engine = create_engine(
    database_url,
    connect_args={
        "sslmode": "require"
    },
)


# Step 8: Load Gold dataset into PostgreSQL
gold_df.to_sql(
    name="property_analytics",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
)


print("\nGold dataset loaded into PostgreSQL successfully.")
print("Table name: property_analytics")