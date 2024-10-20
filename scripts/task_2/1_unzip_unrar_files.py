import os
import zipfile
import rarfile

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import subprocess
import logging
import multiprocessing


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Folder containing the downloaded files and target extraction folder
download_folder = "../downloads"
extracted_folder = "../extracted_files"  # Folder where files will be extracted

# Create the extraction folder if it doesn't exist
os.makedirs(extracted_folder, exist_ok=True)

target_files = [
    "passwords.txt",
    "password.txt",
    "pass.txt",
    "all passwords.txt",
    "_allPasswords_list.txt",
    "password list.txt",
]

# Password for RAR files
rar_password = "https://t.me/FehuCloud"


def extract_zip_archive(file_path, dest_folder):
    """Extracts files from a ZIP archive with progress bar and flattens nested directories."""
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            total_files = len(z.namelist())
            with tqdm(
                total=total_files,
                desc=f"Extracting {os.path.basename(file_path)}",
                unit="file",
            ) as pbar:
                for file_info in z.infolist():
                    # Use only the file name, ignore the path to flatten the structure
                    file_name = os.path.basename(file_info.filename)

                    # Construct the extraction path
                    extracted_path = os.path.join(dest_folder, file_name)

                    # Check if the full path is too long
                    if len(extracted_path) > 255:
                        logging.error(
                            f"Skipping extraction due to long path: {extracted_path}"
                        )
                        continue

                    # Extract the file
                    try:
                        z.extract(file_info, extracted_path)
                        pbar.update(1)
                    except OSError as e:
                        # logging.error(f"Error extracting {file_info.filename}: {e}")
                        continue

        logging.info(f"Extracted ZIP archive: {file_path}")
    except Exception as e:
        logging.error(f"Error extracting ZIP archive {file_path}: {e}")


def extract_rar_archive(file_path, dest_folder):
    """Extracts RAR file using the 'unrar' command and flattens nested directories."""
    try:
        total_files_command = ["unrar", "l", file_path]
        total_files_process = subprocess.Popen(
            total_files_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        total_files_output, _ = total_files_process.communicate()

        total_files = len(
            [
                line
                for line in total_files_output.decode("utf-8").splitlines()
                if "  " in line and "Extracting" not in line
            ]
        )

        command = ["unrar", "x", "-p" + rar_password, file_path, dest_folder]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )

        with tqdm(
            total=total_files,
            desc=f"Extracting {os.path.basename(file_path)}",
            unit="file",
        ) as pbar:
            for line in process.stdout:
                if "Extracting" in line:
                    file_name = line.split()[-1]  # Get the file name from the line
                    extracted_path = os.path.join(
                        dest_folder, os.path.basename(file_name)
                    )

                    # Check if the full path is too long
                    if len(extracted_path) > 255:
                        logging.error(
                            f"Skipping extraction due to long path: {extracted_path}"
                        )
                        continue

                    pbar.update(1)

        process.wait()

        if process.returncode != 0:
            logging.error(
                f"Error extracting {file_path}: {process.stderr.read().decode('utf-8')}"
            )
        else:
            logging.info(f"Extracted RAR archive: {file_path}")
    except Exception as e:
        logging.error(f"Error extracting RAR archive {file_path}: {e}")


def extract_archive(file_path):
    """Extracts files from ZIP or RAR archives."""
    if zipfile.is_zipfile(file_path):
        extract_zip_archive(file_path, extracted_folder)
    elif rarfile.is_rarfile(file_path):
        extract_rar_archive(file_path, extracted_folder)


def main():
    # Collect all files in the download folder
    file_paths = []
    for root, dirs, files in os.walk(download_folder):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))

    # Number of files to process
    num_files = len(file_paths)
    num_cores = multiprocessing.cpu_count()

    # Set max_workers to the lesser of the number of files or a multiple of CPU cores
    max_workers = min(num_files, num_cores * 2)
    logging.info(f"Using {max_workers} threads for file processing")

    # Use multithreading to process files and archives concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use a progress bar for the overall process
        with tqdm(total=len(file_paths), desc="Processing Files", unit="file") as pbar:
            futures = {
                executor.submit(extract_archive, file_path): file_path
                for file_path in file_paths
            }

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    future.result()  # Process the result (raises exceptions if any)
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")
                pbar.update(1)


if __name__ == "__main__":
    main()
