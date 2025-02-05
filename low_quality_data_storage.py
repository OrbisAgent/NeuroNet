import hashlib
from typing import Dict, List, Any
from datetime import datetime
import json
import os

class LowQualityDataPoint:
    def __init__(self, data: Any, metadata: Dict[str, Any], quality_score: float):
        self.data = data
        self.metadata = metadata
        self.quality_score = quality_score
        self.timestamp = datetime.now()
        self.hash = self._generate_hash()

    def _generate_hash(self) -> str:
        data_string = json.dumps(self.data, sort_keys=True)
        metadata_string = json.dumps(self.metadata, sort_keys=True)
        hash_input = f"{data_string}{metadata_string}{self.quality_score}{self.timestamp}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

class LowQualityDataStorage:
    def __init__(self, storage_path: str, retention_period: int = 30):
        self.storage_path = storage_path
        self.retention_period = retention_period  # in days
        self.data_points: List[LowQualityDataPoint] = []
        self.index: Dict[str, int] = {}  # Hash to index mapping

    def add_data_point(self, data_point: LowQualityDataPoint) -> bool:
        if data_point.quality_score >= 0.8:  # Threshold for low-quality data
            return False
        
        self.data_points.append(data_point)
        self.index[data_point.hash] = len(self.data_points) - 1
        self._persist_data_point(data_point)
        return True

    def get_data_point(self, hash_value: str) -> LowQualityDataPoint:
        if hash_value in self.index:
            return self.data_points[self.index[hash_value]]
        return None

    def update_data_point(self, hash_value: str, new_data: Any, new_metadata: Dict[str, Any]) -> bool:
        if hash_value not in self.index:
            return False
        
        index = self.index[hash_value]
        data_point = self.data_points[index]
        data_point.data = new_data
        data_point.metadata.update(new_metadata)
        data_point.timestamp = datetime.now()
        data_point.hash = data_point._generate_hash()
        
        self.index.pop(hash_value)
        self.index[data_point.hash] = index
        
        self._persist_data_point(data_point)
        return True

    def _persist_data_point(self, data_point: LowQualityDataPoint):
        file_path = os.path.join(self.storage_path, f"{data_point.hash}.json")
        with open(file_path, 'w') as f:
            json.dump({
                'data': data_point.data,
                'metadata': data_point.metadata,
                'quality_score': data_point.quality_score,
                'timestamp': data_point.timestamp.isoformat(),
                'hash': data_point.hash
            }, f)

    def load_from_disk(self):
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                with open(os.path.join(self.storage_path, filename), 'r') as f:
                    data = json.load(f)
                    data_point = LowQualityDataPoint(
                        data['data'],
                        data['metadata'],
                        data['quality_score']
                    )
                    data_point.timestamp = datetime.fromisoformat(data['timestamp'])
                    data_point.hash = data['hash']
                    self.data_points.append(data_point)
                    self.index[data_point.hash] = len(self.data_points) - 1

    def cleanup_expired_data(self):
        current_time = datetime.now()
        expired_hashes = []
        
        for data_point in self.data_points:
            if (current_time - data_point.timestamp).days > self.retention_period:
                expired_hashes.append(data_point.hash)
        
        for hash_value in expired_hashes:
            self._remove_data_point(hash_value)

    def _remove_data_point(self, hash_value: str):
        if hash_value in self.index:
            index = self.index[hash_value]
            del self.data_points[index]
            del self.index[hash_value]
            os.remove(os.path.join(self.storage_path, f"{hash_value}.json"))
            
            # Update indices for remaining data points
            for i, dp in enumerate(self.data_points[index:], start=index):
                self.index[dp.hash] = i

    def get_all_data_points(self) -> List[LowQualityDataPoint]:
        return self.data_points

    def search_by_metadata(self, query: Dict[str, Any]) -> List[LowQualityDataPoint]:
        results = []
        for data_point in self.data_points:
            if all(data_point.metadata.get(k) == v for k, v in query.items()):
                results.append(data_point)
        return results

    def get_data_point_count(self) -> int:
        return len(self.data_points)

    def get_average_quality_score(self) -> float:
        if not self.data_points:
            return 0.0
        return sum(dp.quality_score for dp in self.data_points) / len(self.data_points)

# Example usage (not functional, just for illustration)
if __name__ == "__main__":
    storage = LowQualityDataStorage("/path/to/low_quality_storage", retention_period=15)
    
    # Add a new low-quality data point
    new_data_point = LowQualityDataPoint(
        data="Sample low-quality data",
        metadata={"type": "text", "source": "automated_generation"},
        quality_score=0.6
    )
    storage.add_data_point(new_data_point)
    
    # Retrieve a data point
    retrieved_data_point = storage.get_data_point(new_data_point.hash)
    
    # Update a data point
    storage.update_data_point(
        new_data_point.hash,
        new_data="Updated low-quality data",
        new_metadata={"type": "text", "source": "automated_generation", "version": 2}
    )
    
    # Search for data points
    search_results = storage.search_by_metadata({"type": "text"})
    
    # Cleanup expired data
    storage.cleanup_expired_data()
    
    # Get statistics
    data_point_count = storage.get_data_point_count()
    avg_quality_score = storage.get_average_quality_score()
    
    print(f"Total low-quality data points: {data_point_count}")
    print(f"Average quality score: {avg_quality_score:.2f}")

