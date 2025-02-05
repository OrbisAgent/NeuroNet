import hashlib
from typing import List, Dict, Any
from datetime import datetime
import random

class NeuroToken:
    def __init__(self, amount: float):
        self.amount = amount
        self.id = self._generate_token_id()

    def _generate_token_id(self) -> str:
        return hashlib.sha256(f"{self.amount}{datetime.now().timestamp()}".encode()).hexdigest()[:16]

class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.neuro_balance = 0.0
        self.data_contributions = []
        self.ai_model_access = []

class DataContribution:
    def __init__(self, user_id: str, data_type: str, data_size: int, quality_score: float):
        self.user_id = user_id
        self.data_type = data_type
        self.data_size = data_size
        self.quality_score = quality_score
        self.timestamp = datetime.now()
        self.contribution_id = self._generate_contribution_id()

    def _generate_contribution_id(self) -> str:
        return hashlib.sha256(f"{self.user_id}{self.data_type}{self.timestamp}".encode()).hexdigest()[:24]

class AIModel:
    def __init__(self, model_id: str, access_cost: float):
        self.model_id = model_id
        self.access_cost = access_cost
        self.performance_score = random.uniform(0.7, 0.99)  # Simulated performance score

class NeuroExchange:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.available_models: Dict[str, AIModel] = {}
        self.data_pool: List[DataContribution] = []
        self.token_supply = 1_000_000  # Total supply of NEURO tokens

    def register_user(self, user_id: str) -> None:
        if user_id not in self.users:
            self.users[user_id] = User(user_id)
            print(f"User {user_id} registered successfully.")
        else:
            print(f"User {user_id} already exists.")

    def contribute_data(self, user_id: str, data_type: str, data_size: int) -> None:
        if user_id not in self.users:
            print(f"User {user_id} not found. Please register first.")
            return

        quality_score = random.uniform(0.5, 1.0)  # Simulated quality assessment
        contribution = DataContribution(user_id, data_type, data_size, quality_score)
        self.data_pool.append(contribution)
        self.users[user_id].data_contributions.append(contribution.contribution_id)

        # Calculate reward based on data size and quality
        reward = (data_size / 1000) * quality_score * 10  # 10 NEURO per 1000 high-quality data points
        self._mint_and_transfer(user_id, reward)

        print(f"User {user_id} contributed {data_size} data points of type {data_type}.")
        print(f"Reward: {reward} NEURO tokens.")

    def _mint_and_transfer(self, user_id: str, amount: float) -> None:
        if self.token_supply >= amount:
            self.users[user_id].neuro_balance += amount
            self.token_supply -= amount
            print(f"Minted and transferred {amount} NEURO tokens to user {user_id}.")
        else:
            print("Error: Insufficient token supply for minting.")

    def add_ai_model(self, model_id: str, access_cost: float) -> None:
        if model_id not in self.available_models:
            self.available_models[model_id] = AIModel(model_id, access_cost)
            print(f"AI Model {model_id} added with access cost of {access_cost} NEURO.")
        else:
            print(f"AI Model {model_id} already exists.")

    def request_model_access(self, user_id: str, model_id: str) -> None:
        if user_id not in self.users:
            print(f"User {user_id} not found. Please register first.")
            return

        if model_id not in self.available_models:
            print(f"AI Model {model_id} not found.")
            return

        model = self.available_models[model_id]
        if self.users[user_id].neuro_balance >= model.access_cost:
            self.users[user_id].neuro_balance -= model.access_cost
            self.users[user_id].ai_model_access.append(model_id)
            print(f"User {user_id} granted access to AI Model {model_id}.")
            print(f"Remaining balance: {self.users[user_id].neuro_balance} NEURO.")
        else:
            print(f"Insufficient NEURO balance for user {user_id} to access AI Model {model_id}.")

    def get_user_balance(self, user_id: str) -> float:
        if user_id in self.users:
            return self.users[user_id].neuro_balance
        else:
            print(f"User {user_id} not found.")
            return 0.0

    def get_user_contributions(self, user_id: str) -> List[str]:
        if user_id in self.users:
            return self.users[user_id].data_contributions
        else:
            print(f"User {user_id} not found.")
            return []

    def get_user_model_access(self, user_id: str) -> List[str]:
        if user_id in self.users:
            return self.users[user_id].ai_model_access
        else:
            print(f"User {user_id} not found.")
            return []

# Example usage
exchange = NeuroExchange()

# Register users
exchange.register_user("alice")
exchange.register_user("bob")

# Contribute data
exchange.contribute_data("alice", "image", 1000)
exchange.contribute_data("bob", "text", 500)

# Add AI models
exchange.add_ai_model("image_classifier_v1", 100)
exchange.add_ai_model("text_analyzer_v1", 75)

# Request model access
exchange.request_model_access("alice", "image_classifier_v1")
exchange.request_model_access("bob", "text_analyzer_v1")

# Check balances and access
print(f"Alice's balance: {exchange.get_user_balance('alice')} NEURO")
print(f"Bob's balance: {exchange.get_user_balance('bob')} NEURO")
print(f"Alice's model access: {exchange.get_user_model_access('alice')}")
print(f"Bob's model access: {exchange.get_user_model_access('bob')}")

