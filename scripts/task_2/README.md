# Credential Management Scripts

This repository contains a set of Python scripts designed to manage credential files downloaded from a specified source. The scripts perform the following tasks:

1. **Extract ZIP and RAR files** from a download folder.
2. **Search for specific password files** within the extracted content.
3. **Save the credentials** found in those files into a MongoDB database.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [1. Extracting Files](#1-extracting-files)
  - [2. Searching for Credential Files](#2-searching-for-credential-files)
  - [3. Saving Credentials to MongoDB](#3-saving-credentials-to-mongodb)
- [Requirements](#requirements)
- [Logging](#logging)

## Installation

1. Change directory to scripts/task_2/

2. Install the required packages:
   ```bash
   pip install tqdm pymongo rarfile
   ```

3. Ensure you have the `unrar` command-line tool installed on your system for RAR file extraction.

## Usage

### 1. Extracting Files

The script `1_unzip_unrar_files.py` extracts ZIP and RAR files from the specified `download_folder` and saves the extracted files in the `extracted_folder`. 

To run the extraction script:

```bash
python 1_unzip_unrar_files.py
```

### 2. Searching for Credential Files

The script `2_password_files_search.py` searches for specific password files in the `extracted_folder`. The target filenames are defined in the `target_files` list within the script.

To run the search script:

```bash
python 2_password_files_search.py
```

This will generate a file named `search_results.txt` in the parent directory containing the paths of found files.

### 3. Saving Credentials to MongoDB

The script `3_save_credentials_in_db.py` reads the paths from `search_results.txt` and saves the credentials into a MongoDB database. 

Make sure your MongoDB server is running, and adjust the connection string in the script as needed.

To run the saving script:

```bash
python 3_save_credentials_in_db.py
```

## Requirements

- Python 3.x
- `tqdm` for progress bars
- `pymongo` for MongoDB interactions
- `rarfile` for handling RAR files
- `unrar` command-line utility (for RAR file extraction)

## Logging

Each script utilizes the `logging` module to provide real-time feedback on its progress and any issues encountered during execution. Logs are printed to the console, but can be redirected to a file if desired.
