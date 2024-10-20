import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
from pymongo import MongoClient


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["credentials_db"]
collection = db["credentials"]

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_file(file_path):
    """Parses a file and returns a list of dictionaries with extracted data."""
    entries = []
    with open(file_path, "r") as file:
        entry = {}
        for line in file:
            line = line.strip()
            if line:  # Ignore empty lines
                try:
                    key, value = line.split(": ", 1)  # Split line into key and value
                    entry[key.lower()] = (
                        value  # Store data in lower case for consistency
                    )
                    if key.lower() == "password":  # If the entry is complete
                        entries.append(entry.copy())  # Append a copy of the entry
                        entry = {}  # Reset for the next entry
                except ValueError as e:
                    logging.warning(
                        f"Skipping line in {file_path}: {line} (Error: {e})"
                    )
    return entries


def save_to_mongodb(entries):
    """Saves a list of entries to MongoDB."""
    if entries:
        collection.insert_many(entries)  # Insert all entries in one go
        logging.info(f"Inserted {len(entries)} entries into MongoDB.")
    else:
        logging.info("No entries to insert.")


def process_file(file_path):
    """Process a single file: Parse and save its entries."""
    logging.info(f"Processing file: {file_path}")
    entries = parse_file(file_path)
    save_to_mongodb(entries)
    logging.info(f"Finished processing file: {file_path}")


def main():
    # Path to the file that contains the list of relative file paths
    file_with_paths = "../search_results.txt"

    # Check if the file with paths exists
    if not os.path.exists(file_with_paths):
        logging.error(f"File {file_with_paths} does not exist.")
        return

    # Read all paths from the file
    with open(file_with_paths, "r") as f:
        file_paths = [line.strip() for line in f.readlines() if line.strip()]

    if not file_paths:
        logging.info("No file paths found to process.")
        return

    # Progress bar and multithreading to process files
    num_workers = min(10, len(file_paths))  # Number of threads to use, adjust as needed
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_file, file_path): file_path
            for file_path in file_paths
        }

        # Use tqdm to track progress
        with tqdm(total=len(file_paths), desc="Processing files", unit="file") as pbar:
            for future in as_completed(futures):
                try:
                    future.result()  # Process the result (no return value here)
                except Exception as e:
                    logging.error(f"Error processing file {futures[future]}: {e}")
                pbar.update(1)

    logging.info("All files have been processed.")


if __name__ == "__main__":
    main()
