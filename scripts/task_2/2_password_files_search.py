import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Folder to search
extracted_folder = "../extracted_files"

# File names to search for
target_files = [
    "password.txt",
    "passwords.txt",
    "pass.txt",
    "all passwords.txt",
    "_allPasswords_list.txt",
    "password list.txt",
]

# Prepare the search pattern for the find command
search_patterns = [f"-name '{file_name}' -type f" for file_name in target_files]
find_command_template = f"find {{}} {' -o '.join(search_patterns)}"


def find_files_in_subfolder(subfolder):
    """Uses the `find` command to search for target files in a subfolder."""
    try:
        # Construct and execute the find command for the subfolder
        command = find_command_template.format(subfolder)
        logging.info(f"Searching in: {subfolder}")

        # Adding a timeout to avoid hanging
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )

        # Collect and return the output paths, filter out empty results
        return [path for path in result.stdout.strip().split("\n") if path]
    except subprocess.TimeoutExpired:
        logging.error(f"Search in {subfolder} timed out.")
        return []
    except Exception as e:
        logging.error(f"Error searching subfolder {subfolder}: {e}")
        return []


def save_results_to_file(file_paths, output_file, batch_size=500):
    """Saves the list of found file paths to a text file in batches."""
    try:
        with open(output_file, "w") as f:
            for i in range(0, len(file_paths), batch_size):
                f.writelines(f"{path}\n" for path in file_paths[i : i + batch_size])
        logging.info(f"Saved {len(file_paths)} file paths to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results to file {output_file}: {e}")


def main():
    # Get all subfolders in the extracted folder
    subfolders = [
        os.path.join(extracted_folder, d)
        for d in os.listdir(extracted_folder)
        if os.path.isdir(os.path.join(extracted_folder, d))
    ]

    # Check if there are no subfolders
    if not subfolders:
        logging.info("No subfolders found in the extracted folder.")
        return

    # Optimize the number of threads
    num_cores = min(
        len(subfolders), os.cpu_count() * 2
    )  # Double the number of CPU cores
    found_files = []

    # Thread-safe way to manage found files
    with ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = {
            executor.submit(find_files_in_subfolder, subfolder): subfolder
            for subfolder in subfolders
        }

        # Progress bar for subfolder searching
        with tqdm(
            total=len(subfolders), desc="Searching", unit="subfolder", mininterval=1
        ) as pbar:
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        found_files.extend(result)
                except Exception as e:
                    logging.error(f"Error searching subfolder {futures[future]}: {e}")
                pbar.update(1)

    if found_files:
        logging.info(f"Found {len(found_files)} matching files.")

        # Save the found files to a text file
        output_file = "../search_results.txt"
        save_results_to_file(found_files, output_file)
    else:
        logging.info("No matching files found.")


if __name__ == "__main__":
    main()
