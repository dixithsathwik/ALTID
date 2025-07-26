import os
import random
from datetime import datetime, timedelta
import uuid
from lxml import etree

def validate_xml_signature(xml_path: str) -> bool:
    """
    MOCK IMPLEMENTATION for hackathon purposes.
    Simulates XML signature validation for Aadhaar documents.
    Returns True 90% of the time to simulate successful validation.
    """
    try:
        # For demo purposes, randomly fail 10% of the time
        if random.random() < 0.9:  # 90% success rate
            print("✅ [MOCK] XML signature validation successful (simulated for hackathon)")
            return True
        else:
            print("❌ [MOCK] XML signature validation failed (simulated for hackathon)")
            return False
    except Exception as e:
        print(f"❌ [MOCK] XML signature validation error: {e}")
        return False

def validate_aadhaar_oky_signature(xml_data: bytes) -> bool:
    """
    MOCK IMPLEMENTATION for hackathon purposes.
    Simulates Aadhaar OKY XML signature validation.
    Returns True 90% of the time to simulate successful validation.
    """
    try:
        # For demo purposes, randomly fail 10% of the time
        if random.random() < 0.9:  # 90% success rate
            print("✅ [MOCK] Aadhaar OKY signature is valid (simulated for hackathon)")
            return True
        else:
            print("❌ [MOCK] Aadhaar OKY signature validation failed (simulated for hackathon)")
            return False
    except Exception as e:
        print(f"❌ [MOCK] Aadhaar OKY signature validation error: {e}")
        return False

def validate_xml_signature_block(xml_data: bytes) -> bool:
    """
    MOCK IMPLEMENTATION for hackathon purposes.
    Simulates XML signature block validation.
    Returns True 90% of the time to simulate successful validation.
    """
    try:
        # For demo purposes, randomly fail 10% of the time
        if random.random() < 0.9:  # 90% success rate
            print("✅ [MOCK] XML signature block is valid (simulated for hackathon)")
            return True
        else:
            print("❌ [MOCK] XML signature block validation failed (simulated for hackathon)")
            return False
        if not os.path.exists(uidai_cert_path):
            print(f"❌ UIDAI public key not found at: {uidai_cert_path}")
            return False
            
        with open(uidai_cert_path, 'r') as cert_file:
            uidai_cert = cert_file.read()

        # Allow SHA1-based signature (commonly used in UIDAI XML)
        allowed_methods = [
            SignatureMethod.RSA_SHA1,
            SignatureMethod.RSA_SHA256,
            SignatureMethod.RSA_SHA512
        ]

        # Perform XML signature verification using UIDAI public key
        XMLVerifier().verify(
            xml_data,
            x509_cert=uidai_cert,
            require_x509=False,
            signature_methods=allowed_methods
        )

        print("✅ XML Signature block is valid.")
        return True

    except Exception as e:
        print(f"❌ XML signature block validation failed: {e}")
        return False

def validate_pdf_signature(pdf_path: str) -> bool:
    """
    MOCK IMPLEMENTATION for hackathon purposes.
    Simulates PDF signature validation.
    Returns True 90% of the time to simulate successful validation.
    """
    try:
        # For demo purposes, randomly fail 10% of the time
        if random.random() < 0.9:  # 90% success rate
            print("✅ [MOCK] PDF signature is valid and trusted (simulated for hackathon)")
            return True
        else:
            print("❌ [MOCK] PDF signature validation failed (simulated for hackathon)")
            return False
    except Exception as e:
        print(f"❌ [MOCK] PDF signature validation error: {e}")
        return False
