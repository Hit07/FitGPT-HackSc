import json
import os
from pathlib import Path

import requests

# Configure your OpenSearch details
OPENSEARCH_ENDPOINT = "https://search-hackscexercisedb-ziw2dlmnimotyfx2lgtjtqfdpy.aos.us-west-2.on.aws"
INDEX_NAME = "exercise_index"
USERNAME = "master"  # Replace with your OpenSearch username
PASSWORD = "Password1234#"  # Replace with your OpenSearch password

# Directory containing the JSON files
JSON_DIR = "/Users/navneet/Documents/free-exercise-db/exercises"


def index_to_opensearch(file_path):
    """
    Reads a JSON file and indexes it into the OpenSearch cluster.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Use the "name" field as the document ID
            doc_id = data.get("name", None)
            if not doc_id:
                print(f"Skipping file {file_path}: Missing 'name' field")
                return
            # OpenSearch URL for indexing
            url = f"{OPENSEARCH_ENDPOINT}/{INDEX_NAME}/_doc/{doc_id}"

            # # Send the data to OpenSearch
            response = requests.put(
                url,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"},
                json=data
            )

            if response.status_code in [200, 201]:
                print(f"Successfully indexed: {doc_id}")
            else:
                print(f"Failed to index: {doc_id}, Response: {response.status_code}, {response.text}")



    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def main():
    """
    Main function to iterate over all JSON files in the directory and index them.
    """
    # Check if directory exists
    if not os.path.exists(JSON_DIR):
        print(f"Directory {JSON_DIR} does not exist.")
        return

    # Iterate over JSON files in the directory
    for file_name in os.listdir(JSON_DIR):
        if file_name.endswith(".json"):
            file_path = Path(JSON_DIR) / file_name
            index_to_opensearch(file_path)


if __name__ == "__main__":
    main()
