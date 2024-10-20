import os
import asyncio
from telethon import TelegramClient
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


# Your API details (replace with your actual credentials)
api_id = "API_ID"
api_hash = "API_HASH"

channel_username = "t.me/interview_siaforce"

# Define the folder where files will be saved
download_folder = "../downloads"

# Ensure the folder exists
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Create the Telegram client
client = TelegramClient("session_name", api_id, api_hash)

# Create a ThreadPoolExecutor for multithreading
# executor = ThreadPoolExecutor(max_workers=4)


# Function to download media with progress tracking
async def download_media(message):
    if message.file:
        try:
            file_name = message.file.name or f"file_{message.id}.dat"
            file_path = os.path.join(download_folder, file_name)

            print(
                f"Downloading {file_name} ({message.file.size / (1024 ** 2):.2f} MB)..."
            )

            with tqdm(
                total=message.file.size,
                unit="B",
                unit_scale=True,
                desc=file_name,
                leave=False,
            ) as pbar:
                # Define a progress callback for updating the tqdm progress bar
                def progress_callback(current, total):
                    pbar.update(current - pbar.n)  # update by the difference

                # Download the file with the progress callback
                await message.download_media(
                    file=file_path, progress_callback=progress_callback
                )

            # Verify if the file was downloaded
            if os.path.exists(file_path):
                print(f"Downloaded {file_name} to {file_path}")
            else:
                print(f"Failed to download {file_name}.")
        except Exception as e:
            print(f"Error downloading media from message {message.id}: {e}")
    else:
        print(f"Message {message.id} does not contain a file.")


# Main function to initiate the download
async def main():
    # Connect to Telegram
    await client.start()

    # Get the channel entity
    entity = await client.get_entity(channel_username)

    # Prepare to download files concurrently
    tasks = []
    async for message in client.iter_messages(entity):
        if message.file:
            print(f"Found file: {message.file.name or 'Unnamed file'}")
            # Add a task to download each file
            tasks.append(download_media(message))

    # Run all the download tasks concurrently
    await asyncio.gather(*tasks)

    # Notify when all downloads are completed
    print("All files have been downloaded.")


# Start the script
with client:
    client.loop.run_until_complete(main())
