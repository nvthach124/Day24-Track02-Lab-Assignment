from src.encryption.vault import SimpleVault
from src.quality.validation import build_patient_expectation_suite, validate_anonymized_data
import pandas as pd
import os
import json

def test_encryption():
    print("Testing Encryption...")
    vault = SimpleVault(".test_vault_key")
    data = "Secret Patient Data"
    encrypted = vault.encrypt_data(data)
    print(f"  Encrypted: {json.dumps(encrypted, indent=2)}")
    
    decrypted = vault.decrypt_data(encrypted)
    print(f"  Decrypted: {decrypted}")
    
    if data == decrypted:
        print("  ✅ Encryption/Decryption Success")
    else:
        print("  ❌ Encryption/Decryption Failure")
    
    if os.path.exists(".test_vault_key"):
        os.remove(".test_vault_key")
    print("-" * 40)

def test_data_quality():
    print("Testing Data Quality...")
    # Thử validate raw data trước
    results = validate_anonymized_data("data/raw/patients_raw.csv")
    print(f"  Validation Results (Raw Data): {json.dumps(results, indent=2)}")
    
    # Ở lab này chúng ta chỉ check logic cơ bản trong validate_anonymized_data
    if results["success"] == False: # Raw data should fail some checks if they are for anonymized data
        print("  ✅ Validation Logic Working (detected raw data)")
    else:
        print("  ⚠️ Validation Logic might be too loose")
    print("-" * 40)

if __name__ == "__main__":
    test_encryption()
    test_data_quality()
