import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def upload_to_azure_blob(container_name, blob_name, file_path):
    """
    Upload a file to an Azure Blob Storage container using a SAS token.

    :param container_name: Name of the Azure Blob Storage container
    :param blob_name: Name of the blob (file) to be created in the container
    :param file_path: Path to the local file to be uploaded
    """
    account_name = os.getenv('AZURE_ACCOUNT_NAME')  # Replace with your Azure Storage account name
    sas_token = os.getenv('AZURE_SAS_TOKEN')  # Read SAS token from environment variable

    if not sas_token:
        raise ValueError("SAS token not found in environment variables.")

    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

    headers = {
        'x-ms-blob-type': 'BlockBlob'
    }

    file_size = os.path.getsize(file_path)
    chunk_size = 4 * 1024 * 1024  # 1 MB

    with open(file_path, 'rb') as file, tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {blob_name}") as pbar:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            response = requests.put(url, headers=headers, data=chunk)
            if response.status_code not in (201, 202):
                print(f"Failed to upload file {blob_name}. Status code: {response.status_code}")
                print(response.text)
                return
            pbar.update(len(chunk))

    print(f"File {blob_name} uploaded successfully.")

def upload_files_in_parallel(container_name, files):
    """
    Upload multiple files to an Azure Blob Storage container in parallel.

    :param container_name: Name of the Azure Blob Storage container
    :param files: List of tuples containing blob_name and file_path
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(upload_to_azure_blob, container_name, blob_name, file_path) for blob_name, file_path in files]

        # Use tqdm to display a progress bar
        for future in tqdm(futures, desc="Uploading files", unit="file"):
            future.result()

# Example usage:
# files_to_upload = [
#     ('blob1.webp', '/path/to/file1.webp'),
#     ('blob2.webp', '/path/to/file2.webp'),
#     # Add more files as needed
# ]
# upload_files_in_parallel('mycontainer', files_to_upload)