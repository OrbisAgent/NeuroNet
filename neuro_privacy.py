import hashlib
from typing import Dict, List, Any
from datetime import datetime, timedelta
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PrivacyManager:
    def __init__(self):
        self.user_privacy_settings: Dict[str, Dict[str, Any]] = {}
        self.data_access_logs: List[Dict[str, Any]] = []
        self.encryption_keys: Dict[str, bytes] = {}

    def create_user_privacy_settings(self, user_id: str):
        if user_id not in self.user_privacy_settings:
            self.user_privacy_settings[user_id] = {
                "data_sharing": False,
                "anonymize_contributions": True,
                "third_party_access": False,
                "notification_preferences": {
                    "email": True,
                    "push": False,
                    "in_app": True
                }
            }
            self._generate_encryption_key(user_id)
            print(f"Privacy settings created for user {user_id}")
        else:
            print(f"Privacy settings already exist for user {user_id}")

    def update_privacy_settings(self, user_id: str, settings: Dict[str, Any]):
        if user_id in self.user_privacy_settings:
            self.user_privacy_settings[user_id].update(settings)
            print(f"Privacy settings updated for user {user_id}")
        else:
            print(f"User {user_id} not found")

    def get_privacy_settings(self, user_id: str) -> Dict[str, Any]:
        return self.user_privacy_settings.get(user_id, {})

    def _generate_encryption_key(self, user_id: str):
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(user_id.encode()))
        self.encryption_keys[user_id] = key

    def encrypt_data(self, user_id: str, data: str) -> str:
        if user_id not in self.encryption_keys:
            raise ValueError(f"Encryption key not found for user {user_id}")
        
        f = Fernet(self.encryption_keys[user_id])
        return f.encrypt(data.encode()).decode()

    def decrypt_data(self, user_id: str, encrypted_data: str) -> str:
        if user_id not in self.encryption_keys:
            raise ValueError(f"Encryption key not found for user {user_id}")
        
        f = Fernet(self.encryption_keys[user_id])
        return f.decrypt(encrypted_data.encode()).decode()

    def log_data_access(self, user_id: str, data_type: str, purpose: str):
        log_entry = {
            "user_id": user_id,
            "data_type": data_type,
            "purpose": purpose,
            "timestamp": datetime.now()
        }
        self.data_access_logs.append(log_entry)

    def get_user_data_access_logs(self, user_id: str) -> List[Dict[str, Any]]:
        return [log for log in self.data_access_logs if log["user_id"] == user_id]

class DataAnonymizer:
    @staticmethod
    def anonymize_user_id(user_id: str) -> str:
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]

    @staticmethod
    def anonymize_ip_address(ip_address: str) -> str:
        # Anonymize the last octet of IPv4 or last 80 bits of IPv6
        ip_parts = ip_address.split('.')
        if len(ip_parts) == 4:  # IPv4
            return f"{'.'.join(ip_parts[:3])}.0"
        else:  # IPv6
            return ip_address[:20] + ':0000:0000:0000:0000'

    @staticmethod
    def anonymize_location(latitude: float, longitude: float, precision: int = 1) -> tuple:
        # Reduce precision of coordinates
        return (round(latitude, precision), round(longitude, precision))

class ConsentManager:
    def __init__(self):
        self.user_consents: Dict[str, Dict[str, Any]] = {}

    def record_consent(self, user_id: str, purpose: str, consented: bool):
        if user_id not in self.user_consents:
            self.user_consents[user_id] = {}
        
        self.user_consents[user_id][purpose] = {
            "consented": consented,
            "timestamp": datetime.now()
        }

    def check_consent(self, user_id: str, purpose: str) -> bool:
        if user_id in self.user_consents and purpose in self.user_consents[user_id]:
            return self.user_consents[user_id][purpose]["consented"]
        return False

    def revoke_consent(self, user_id: str, purpose: str):
        if user_id in self.user_consents and purpose in self.user_consents[user_id]:
            self.user_consents[user_id][purpose]["consented"] = False
            self.user_consents[user_id][purpose]["timestamp"] = datetime.now()

class DataRetentionManager:
    def __init__(self):
        self.data_retention_policies: Dict[str, timedelta] = {
            "user_data": timedelta(days=365),
            "transaction_data": timedelta(days=730),
            "log_data": timedelta(days=90)
        }
        self.data_store: Dict[str, List[Dict[str, Any]]] = {}

    def add_data(self, data_type: str, data: Dict[str, Any]):
        if data_type not in self.data_store:
            self.data_store[data_type] = []
        
        data["timestamp"] = datetime.now()
        self.data_store[data_type].append(data)

    def cleanup_expired_data(self):
        now = datetime.now()
        for data_type, retention_period in self.data_retention_policies.items():
            if data_type in self.data_store:
                self.data_store[data_type] = [
                    data for data in self.data_store[data_type]
                    if now - data["timestamp"] <= retention_period
                ]

    def get_data(self, data_type: str) -> List[Dict[str, Any]]:
        return self.data_store.get(data_type, [])

class NeuroPrivacy:
    def __init__(self):
        self.privacy_manager = PrivacyManager()
        self.data_anonymizer = DataAnonymizer()
        self.consent_manager = ConsentManager()
        self.data_retention_manager = DataRetentionManager()

    def setup_user_privacy(self, user_id: str):
        self.privacy_manager.create_user_privacy_settings(user_id)

    def update_user_privacy_settings(self, user_id: str, settings: Dict[str, Any]):
        self.privacy_manager.update_privacy_settings(user_id, settings)

    def anonymize_user_data(self, user_id: str, ip_address: str, latitude: float, longitude: float) -> Dict[str, Any]:
        return {
            "anonymized_id": self.data_anonymizer.anonymize_user_id(user_id),
            "anonymized_ip": self.data_anonymizer.anonymize_ip_address(ip_address),
            "anonymized_location": self.data_anonymizer.anonymize_location(latitude, longitude)
        }

    def record_user_consent(self, user_id: str, purpose: str, consented: bool):
        self.consent_manager.record_consent(user_id, purpose, consented)

    def check_user_consent(self, user_id: str, purpose: str) -> bool:
        return self.consent_manager.check_consent(user_id, purpose)

    def handle_data_access(self, user_id: str, data_type: str, purpose: str):
        if self.check_user_consent(user_id, purpose):
            self.privacy_manager.log_data_access(user_id, data_type, purpose)
            # Proceed with data access
            print(f"Access granted for user {user_id} to {data_type} for {purpose}")
        else:
            print(f"Access denied for user {user_id} to {data_type} for {purpose}")

    def encrypt_sensitive_data(self, user_id: str, data: str) -> str:
        return self.privacy_manager.encrypt_data(user_id, data)

    def decrypt_sensitive_data(self, user_id: str, encrypted_data: str) -> str:
        return self.privacy_manager.decrypt_data(user_id, encrypted_data)

    def add_user_data(self, user_id: str, data: Dict[str, Any]):
        self.data_retention_manager.add_data("user_data", {
            "user_id": user_id,
            **data
        })

    def cleanup_expired_data(self):
        self.data_retention_manager.cleanup_expired_data()

    def get_user_data_access_logs(self, user_id: str) -> List[Dict[str, Any]]:
        return self.privacy_manager.get_user_data_access_logs(user_id)

# Example usage
neuro_privacy = NeuroPrivacy()

# Setup user privacy
neuro_privacy.setup_user_privacy("user123")

# Update privacy settings
neuro_privacy.update_user_privacy_settings("user123", {"data_sharing": True})

# Anonymize user data
anonymized_data = neuro_privacy.anonymize_user_data("user123", "192.168.1.1", 40.7128, -74.0060)
print("Anonymized data:", anonymized_data)

# Record user consent
neuro_privacy.record_user_consent("user123", "data_analysis", True)

# Handle data access
neuro_privacy.handle_data_access("user123", "transaction_history", "data_analysis")

# Encrypt and decrypt sensitive data
sensitive_data = "My secret $NEURO balance"
encrypted_data = neuro_privacy.encrypt_sensitive_data("user123", sensitive_data)
decrypted_data = neuro_privacy.decrypt_sensitive_data("user123", encrypted_data)
print("Original:", sensitive_data)
print("Encrypted:", encrypted_data)
print("Decrypted:", decrypted_data)

# Add user data
neuro_privacy.add_user_data("user123", {"name": "Alice", "email": "alice@example.com"})

# Cleanup expired data
neuro_privacy.cleanup_expired_data()

# Get user data access logs
access_logs = neuro_privacy.get_user_data_access_logs("user123")
print("Data access logs:", access_logs)

