import os
import requests

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

    with open(file_path, 'rb') as file:
        file_content = file.read()

    headers = {
        'x-ms-blob-type': 'BlockBlob'
    }

    response = requests.put(url, headers=headers, data=file_content)

    if response.status_code == 201:
        print(f"File {blob_name} uploaded successfully.")
    else:
        print(f"Failed to upload file {blob_name}. Status code: {response.status_code}")
        print(response.text)