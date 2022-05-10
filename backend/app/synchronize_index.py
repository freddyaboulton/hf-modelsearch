import requests
from typing import List
import argparse
import json

MODELS_API = "https://huggingface.co/api/models"
README_API = "https://huggingface.co/{model_id}/raw/main/README.md"
SERVER_API = "http://localhost:8000/model/"


def get_model_ids(limit: int) -> List[str]:
    models = requests.get(MODELS_API)
    return [m["id"] for m in models.json()][:limit]


def add_to_index(model_id: str) -> None:
    try:
        readme = requests.get(README_API.format(model_id=model_id))
        body = {"id": model_id, "readme_text": readme.text}
        resp = requests.post(SERVER_API, data=json.dumps(body))
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"message": f"Error cannot add {model_id} to index. Probably missing a readme file."}



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize the model index with the latest info in huggingface model hub')
    parser.add_argument('--number', dest="number", metavar='N', type=int, help='Number of models to pull from https://huggingface.co/api/models and add to index')
    args = parser.parse_args()
    ids = get_model_ids(args.number)
    for id_ in ids:
        resp = add_to_index(id_)
        print(resp)



