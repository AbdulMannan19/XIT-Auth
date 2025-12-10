"""Google Drive Adapter"""
import os
from typing import Optional, Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
import io
import json

from ..interface import ICloudStorageProvider

SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveAdapter(ICloudStorageProvider):
    """Adapter for Google Drive API"""
    
    def __init__(self, user_credentials: Dict, client_config: Dict):
        """
        Initialize Google Drive adapter
        
        Args:
            user_credentials: Dict with user's OAuth tokens
            client_config: OAuth client configuration from Google Cloud Console
        """
        self.user_credentials = user_credentials
        self.client_config = client_config
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with user's stored credentials"""
        try:
            # Create credentials from stored token
            creds = Credentials.from_authorized_user_info(
                self.user_credentials,
                SCOPES
            )
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("[Google Drive] Refreshing access token...")
                creds.refresh(Request())
                self.user_credentials = json.loads(creds.to_json())
            
            self.service = build('drive', 'v3', credentials=creds)
            print("[Google Drive] Successfully authenticated")
            
        except Exception as e:
            print(f"[Google Drive] Authentication failed: {e}")
            raise
    
    def get_updated_credentials(self) -> Dict:
        """Get updated credentials (in case token was refreshed)"""
        return self.user_credentials
    
    def read_file(self, file_id: str) -> bytes:
        """Read a file from Google Drive"""
        try:
            print(f"[Google Drive] Reading file: {file_id}")
            request = self.service.files().get_media(fileId=file_id)
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"[Google Drive] Download: {int(status.progress() * 100)}%")
            
            print("[Google Drive] ✓ File downloaded")
            return file_buffer.getvalue()
            
        except HttpError as error:
            print(f"[Google Drive] ✗ Error: {error}")
            raise
    
    def upload_file(self, file_content: bytes, path: str, mime_type: str = 'application/octet-stream') -> str:
        """Upload a file to Google Drive"""
        try:
            print(f"[Google Drive] Uploading: {path}")
            
            file_metadata = {'name': path}
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            print(f"[Google Drive] ✓ Uploaded: {file_id}")
            return file_id
            
        except HttpError as error:
            print(f"[Google Drive] ✗ Error: {error}")
            raise
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from Google Drive"""
        try:
            print(f"[Google Drive] Deleting: {file_id}")
            self.service.files().delete(fileId=file_id).execute()
            print("[Google Drive] ✓ Deleted")
            return True
            
        except HttpError as error:
            print(f"[Google Drive] ✗ Error: {error}")
            return False


class GoogleDriveOAuthHelper:
    """Helper class for OAuth flow"""
    
    @staticmethod
    def get_authorization_url(client_config: Dict, redirect_uri: str, state: str = None) -> str:
        """
        Generate OAuth authorization URL for users to visit
        
        Args:
            client_config: OAuth client configuration
            redirect_uri: Your callback URL (e.g., https://yoursite.com/oauth/callback)
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL to redirect user to
        """
        from google_auth_oauthlib.flow import Flow
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',  # Get refresh token
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Force consent to get refresh token
        )
        
        return auth_url
    
    @staticmethod
    def exchange_code_for_token(client_config: Dict, redirect_uri: str, code: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Args:
            client_config: OAuth client configuration
            redirect_uri: Your callback URL (must match the one used in authorization)
            code: Authorization code from callback
            
        Returns:
            Credentials dict to store in database
        """
        from google_auth_oauthlib.flow import Flow
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return json.loads(credentials.to_json())
