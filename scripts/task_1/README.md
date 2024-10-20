## This script helps you download files from a public Telegram channel using Telethon and multithreading.

### Installation

1.  Install required libraries:

<!-- end list -->

```
pip install telethon tqdm
```

2.  Create a Telegram application and obtain your API ID and hash from [https://core.telegram.org/](https://www.google.com/url?sa=E&source=gmail&q=https://core.telegram.org/).

### Usage

1.  Update the script with your credentials:

      - Replace `api_id` and `api_hash` with your actual values.
      - Edit `channel_username` to match the public channel name (without the '@').

2.  Set the desired download folder location in `download_folder`.

3.  Run the script:

    ```
    python download_files.py
    ```

### Features

  * Downloads files from a public Telegram channel with progress bars.
  * Utilizes multithreading for efficient downloads.
  * Verifies downloaded files and handles errors.

### Notes

  * Make sure you have a session file named `session_name` in the same directory as the script. This file is used to store authentication details. If you don't have one, the first run will initiate a login flow.
  * You may need to adjust the `max_workers` parameter in the `ThreadPoolExecutor` depending on your system resources and desired performance.

