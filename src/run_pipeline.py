import logging
import subprocess


# Step 1: Configure logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Step 2: Create reusable function
def run_step(step_name, script_path):

    print(f"\nRunning: {step_name}")
    logging.info("Starting: %s", step_name)

    try:
        subprocess.run(
            ["python", script_path],
            check=True,
        )

        print(f"Completed: {step_name}")
        logging.info("Completed: %s", step_name)

    except subprocess.CalledProcessError:
        print(f"Failed: {step_name}")
        logging.exception("Failed: %s", step_name)
        raise


# Step 3: Extract EPC data
run_step(
    "Extract EPC data",
    "src/extract/read_epc.py",
)


# Step 4: Transform EPC data
run_step(
    "Transform EPC data",
    "src/transform/transform_epc.py",
)


# Step 5: Validate EPC Silver data
run_step(
    "Validate EPC Silver data",
    "src/validate/validate_epc_silver.py",
)


# Step 6: Join Land Registry and EPC
run_step(
    "Create Gold analytics dataset",
    "src/integrate/join_land_registry_epc.py",
)


# Step 7: Upload datasets to Azure Data Lake
run_step(
    "Upload data to Azure Data Lake",
    "src/load/upload_to_azure.py",
)


# Step 8: Load Gold data from Azure into PostgreSQL
run_step(
    "Load Gold data into PostgreSQL",
    "src/load/load_to_postgres.py",
)


print("\nETL pipeline completed successfully.")
logging.info("ETL pipeline completed successfully.")