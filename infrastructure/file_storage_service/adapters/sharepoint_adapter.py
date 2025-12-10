from ..interface import ICloudStorageProvider


class SharePointAdapter(ICloudStorageProvider):
    """Adapter for SharePoint API"""
    
    def read_file(self, path: str) -> bytes:
        print(f"[SharePoint] Reading file from: {path}")
        print("[SharePoint] API call: ctx.web.get_file_by_server_relative_url(...).download()")
        return b"Mock content from SharePoint"
    
    def upload_file(self, file_content: bytes, path: str) -> str:
        print(f"[SharePoint] Uploading {len(file_content)} bytes to: {path}")
        print("[SharePoint] API call: target_folder.upload_file(...)")
        return f"sharepoint_item_{path.replace('/', '_')}"
    
    def delete_file(self, file_id: str) -> bool:
        print(f"[SharePoint] Deleting file: {file_id}")
        print("[SharePoint] API call: file.delete_object()")
        return True
