from typing import Dict, Type
from .interface import ICloudStorageProvider
from .adapters import GoogleDriveAdapter, AzureBlobAdapter, SharePointAdapter


class CloudProviderFactory:
    """Factory for creating cloud storage provider instances"""
    
    _providers: Dict[str, Type[ICloudStorageProvider]] = {
        "GDRIVE": GoogleDriveAdapter,
        "AZURE": AzureBlobAdapter,
        "SHAREPOINT": SharePointAdapter,
    }
    
    @staticmethod
    def get_provider(provider_name: str, user_credentials: Dict = None, client_config: Dict = None) -> ICloudStorageProvider:
        """
        Get a cloud storage provider instance
        
        Args:
            provider_name: Name of the provider (GDRIVE, AZURE, SHAREPOINT)
            user_credentials: User's OAuth credentials (required for GDRIVE)
            client_config: OAuth client configuration (required for GDRIVE)
            
        Returns:
            Instance of the requested provider
        """
        provider_name = provider_name.upper()
        provider_class = CloudProviderFactory._providers.get(provider_name)
        
        if provider_class is None:
            available = ", ".join(CloudProviderFactory._providers.keys())
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available providers: {available}"
            )
        
        # Google Drive requires credentials
        if provider_name == "GDRIVE":
            if not user_credentials or not client_config:
                raise ValueError("Google Drive requires user_credentials and client_config")
            return provider_class(user_credentials, client_config)
        
        # Other providers use mock implementation for now
        return provider_class()
