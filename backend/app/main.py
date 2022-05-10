from fastapi import FastAPI, Depends, HTTPException, status
from app.model_index import ElasticSearchModelIndex, Model
from app.pydantic_models import ModelBody
from typing import Dict, Union


app = FastAPI()

def get_index() -> ElasticSearchModelIndex:
    index = ElasticSearchModelIndex("172.18.0.2", "9200")
    try:
        yield index
    finally:
        index.close()


@app.get("/")
async def root():
    return {"message": "Server is up"}


@app.get("/search/", summary="Get a list of model ids whose ReadMe contain the query")
def search_readmetext(query: str, index: ElasticSearchModelIndex = Depends(get_index)):
    return {"data": index.search(query)}


def add_to_index(model: ModelBody, index: ElasticSearchModelIndex) -> Dict[str, str]:
    """Helper method to add a given model to the index.
    
    Return a 500 when we can't add to the index.
    """
    try:
        index.add_to_index(model.id, model.readme_text)
        return {"message": f"model {model.id} added to index."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to upload {model.id} because{str(e)}")


@app.post("/model/", summary="Add a model to the index")
def add_model_to_index(model: ModelBody, index: ElasticSearchModelIndex = Depends(get_index)):
    """Add a model to the index.
    
    If the contents of the request match what's already stored in the index, the index will not be updated.
    """
    model_hash = index.get_hash_by_id(model.id)
    if model_hash == Model(readme=model.readme_text).hash():
        return {"message": f"Not adding model {model.id} to index since contents match what's currently in the index"}
    else:
        return add_to_index(model, index)
    


    


