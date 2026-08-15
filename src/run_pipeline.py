import subprocess


print("\nStep 1: Extract EPC data")
subprocess.run(
    ["python3", "src/extract/read_epc.py"],
    check=True
)


print("\nStep 2: Transform EPC data")
subprocess.run(
    ["python3", "src/transform/transform_epc.py"],
    check=True
)


print("\nStep 3: Validate EPC Silver data")
subprocess.run(
    ["python3", "src/validate/validate_epc_silver.py"],
    check=True
)


print("\nStep 4: Join Land Registry and EPC data")
subprocess.run(
    ["python3", "src/integrate/join_land_registry_epc.py"],
    check=True
)


print("\nStep 5: Upload data to Azure")
subprocess.run(
    ["python3", "src/load/upload_to_azure.py"],
    check=True
)


print("\nETL pipeline completed successfully.")
