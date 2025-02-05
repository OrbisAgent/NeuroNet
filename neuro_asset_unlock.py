from typing import Dict, List, Any
import hashlib
from datetime import datetime, timedelta

class NeuroAsset:
    def __init__(self, asset_id: str, asset_type: str, unlock_cost: float, duration: int):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.unlock_cost = unlock_cost
        self.duration = duration  # Duration in days

    def __str__(self):
        return f"{self.asset_type} (ID: {self.asset_id}) - Cost: {self.unlock_cost} NEURO, Duration: {self.duration} days"

class UserAssetAccess:
    def __init__(self, user_id: str, asset_id: str, expiry_date: datetime):
        self.user_id = user_id
        self.asset_id = asset_id
        self.expiry_date = expiry_date

class NeuroAssetPlatform:
    def __init__(self):
        self.assets: Dict[str, NeuroAsset] = {}
        self.user_balances: Dict[str, float] = {}
        self.user_asset_access: Dict[str, List[UserAssetAccess]] = {}

    def add_asset(self, asset: NeuroAsset):
        self.assets[asset.asset_id] = asset
        print(f"Added new asset: {asset}")

    def register_user(self, user_id: str, initial_balance: float = 0):
        if user_id not in self.user_balances:
            self.user_balances[user_id] = initial_balance
            self.user_asset_access[user_id] = []
            print(f"Registered user {user_id} with initial balance of {initial_balance} NEURO")
        else:
            print(f"User {user_id} already registered")

    def unlock_asset(self, user_id: str, asset_id: str):
        if user_id not in self.user_balances:
            print(f"User {user_id} not found")
            return

        if asset_id not in self.assets:
            print(f"Asset {asset_id} not found")
            return

        asset = self.assets[asset_id]
        if self.user_balances[user_id] < asset.unlock_cost:
            print(f"Insufficient balance to unlock {asset.asset_type}")
            return

        self.user_balances[user_id] -= asset.unlock_cost
        expiry_date = datetime.now() + timedelta(days=asset.duration)
        access = UserAssetAccess(user_id, asset_id, expiry_date)
        self.user_asset_access[user_id].append(access)

        print(f"User {user_id} unlocked {asset.asset_type} until {expiry_date}")
        print(f"Remaining balance: {self.user_balances[user_id]} NEURO")

    def check_asset_access(self, user_id: str, asset_id: str) -> bool:
        if user_id not in self.user_asset_access:
            return False

        for access in self.user_asset_access[user_id]:
            if access.asset_id == asset_id and access.expiry_date > datetime.now():
                return True

        return False

    def list_user_assets(self, user_id: str):
        if user_id not in self.user_asset_access:
            print(f"User {user_id} not found")
            return

        print(f"Assets unlocked by user {user_id}:")
        for access in self.user_asset_access[user_id]:
            if access.expiry_date > datetime.now():
                asset = self.assets[access.asset_id]
                print(f"- {asset.asset_type} (ID: {asset.asset_id}), Expires: {access.expiry_date}")

class AIModelAsset(NeuroAsset):
    def __init__(self, asset_id: str, model_name: str, unlock_cost: float, duration: int, performance_score: float):
        super().__init__(asset_id, "AI Model", unlock_cost, duration)
        self.model_name = model_name
        self.performance_score = performance_score

class DatasetAsset(NeuroAsset):
    def __init__(self, asset_id: str, dataset_name: str, unlock_cost: float, duration: int, num_records: int):
        super().__init__(asset_id, "Dataset", unlock_cost, duration)
        self.dataset_name = dataset_name
        self.num_records = num_records

class PlatformFeatureAsset(NeuroAsset):
    def __init__(self, asset_id: str, feature_name: str, unlock_cost: float, duration: int):
        super().__init__(asset_id, "Platform Feature", unlock_cost, duration)
        self.feature_name = feature_name

# Example usage
platform = NeuroAssetPlatform()

# Add assets
platform.add_asset(AIModelAsset("model1", "Advanced Image Classifier", 100, 30, 0.95))
platform.add_asset(AIModelAsset("model2", "Natural Language Processor", 150, 30, 0.92))
platform.add_asset(DatasetAsset("data1", "Large Scale Image Dataset", 50, 60, 1000000))
platform.add_asset(PlatformFeatureAsset("feature1", "Advanced Analytics Dashboard", 75, 90))

# Register users
platform.register_user("alice", 500)
platform.register_user("bob", 300)

# Unlock assets
platform.unlock_asset("alice", "model1")
platform.unlock_asset("alice", "data1")
platform.unlock_asset("bob", "model2")

# Check asset access
print(f"Alice has access to model1: {platform.check_asset_access('alice', 'model1')}")
print(f"Bob has access to data1: {platform.check_asset_access('bob', 'data1')}")

# List user assets
platform.list_user_assets("alice")
platform.list_user_assets("bob")

