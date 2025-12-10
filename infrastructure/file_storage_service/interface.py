from abc import ABC, abstractmethod


class ICloudStorageProvider(ABC):
    
    
    @abstractmethod
    def read_file(self, path: str) -> bytes:
        
        pass
    
    @abstractmethod
    def upload_file(self, file_content: bytes, path: str) -> str:
        
        pass
    
    @abstractmethod
    def delete_file(self, file_id: str) -> bool:
        
        pass
