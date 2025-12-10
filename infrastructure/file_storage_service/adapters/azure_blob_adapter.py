"""Azure Blob Storage Adapter"""
from ..interface import ICloudStorageProvider


class AzureBlobAdapter(ICloudStorageProvider):
    """Adapter for Azure Blob Storage API"""
    
    def read_file(self, path: str) -> bytes:
        print(f"[Azure Blob] Reading blob from: {path}")
        print("[Azure Blob] API call: blob_client.download_blob().readall()")
        return b"Mock content from Azure Blob Storage"
    
    def upload_file(self, file_content: bytes, path: str) -> str:
        print(f"[Azure Blob] Uploading {len(file_content)} bytes to: {path}")
        print("[Azure Blob] API call: blob_client.upload_blob(data=...)")
        return f"azure_blob_{path}"
    
    def delete_file(self, file_id: str) -> bool:
        print(f"[Azure Blob] Deleting blob: {file_id}")
        print("[Azure Blob] API call: blob_client.delete_blob()")
        return True
