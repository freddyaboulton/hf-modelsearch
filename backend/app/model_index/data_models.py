from elasticsearch_dsl import Document, Text
import hashlib


class Model(Document):
    """Representation of a model in our index.
    
    Currently only storing the readme.
    """
    readme = Text()

    class Index:
        name = "model"
    
    def save(self, **kwargs):
        return super().save(**kwargs)

    def hash(self):
        """Method to get a unique hash from a model document. 
        
        As we add more fields to the model, this method will evolve as well.
        """
        return hashlib.md5(self.readme.encode()).hexdigest()