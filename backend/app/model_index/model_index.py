import abc
from elasticsearch import Elasticsearch
from .data_models import Model
from typing import List, Optional

class ModelIndex(abc.ABC):
    
    @abc.abstractmethod
    def add_to_index(self, id: str, readme_text: str) -> None:
        """Add to index."""
    
    @abc.abstractmethod
    def search(self, readme_text: str) -> List[str]:
        """Return a list of model ids that match a readme text."""
    
    @abc.abstractmethod
    def get_hash_by_id(self, id: str) -> str:
        """Return a hash of the model document corresponding to an id."""



class ElasticSearchModelIndex(ModelIndex):

    def __init__(self, host: str, port: str) -> None:
        self.client = Elasticsearch([{'host': host, 'port': port}])

    def add_to_index(self, id: str, readme_text: str) -> None:
        model = Model(meta={'id': id}, readme=readme_text)
        model.save(using=self.client)
    
    def search(self, readme_text: str) -> List[str]:
        search = Model.search(using=self.client)
        # Turn into a scan so we can return all matches
        # Product requirements state the ids do not have to be sorted in a specific order
        search = search.query("match", readme=readme_text).scan()
        return [hit.meta['id'] for hit in search]
    
    def get_hash_by_id(self, id: str) -> Optional[str]:
        exists = Model.exists(id, using=self.client)
        if exists:
            return Model.get(id, using=self.client).hash()
        return None

    def init_index(self):
        Model.init(using=self.client)
    
    def close(self):
        self.client.close()
