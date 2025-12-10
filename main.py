"""Client code demonstrating the cloud storage system"""
from infrastructure.file_storage_service import CloudProviderFactory, ICloudStorageProvider


def main():
    """Client code demonstrating the usage of the cloud storage system"""
    
    print("=" * 60)
    print("Cloud Storage Integration System Demo")
    print("=" * 60)
    
    # Test data
    test_file_content = b"Hello, Cloud Storage!"
    test_path = "documents/test_file.txt"
    
    # List of providers to test
    providers_to_test = ["GDRIVE", "AZURE", "SHAREPOINT"]
    
    for provider_name in providers_to_test:
        print(f"\n{'=' * 60}")
        print(f"Testing Provider: {provider_name}")
        print("=" * 60)
        
        try:
            # Get provider instance from factory
            provider: ICloudStorageProvider = CloudProviderFactory.get_provider(provider_name)
            
            # Upload file
            print("\n1. Uploading file...")
            file_id = provider.upload_file(test_file_content, test_path)
            print(f"   ✓ File uploaded with ID: {file_id}")
            
            # Read file
            print("\n2. Reading file...")
            content = provider.read_file(test_path)
            print(f"   ✓ File content: {content.decode()}")
            
            # Delete file
            print("\n3. Deleting file...")
            success = provider.delete_file(file_id)
            print(f"   ✓ File deleted: {success}")
            
        except ValueError as e:
            print(f"   ✗ Error: {e}")
    
    # Test invalid provider
    print(f"\n{'=' * 60}")
    print("Testing Invalid Provider")
    print("=" * 60)
    try:
        invalid_provider = CloudProviderFactory.get_provider("DROPBOX")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print(f"\n{'=' * 60}")
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
