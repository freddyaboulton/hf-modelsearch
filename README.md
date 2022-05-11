# Huggingface Model Search

REST API for searching models in Huggingface model hub based on the contents of their README files.

# Getting started

1. Make sure you have docker installed
2. Make the directory to store the readmes: `mkdir es-data`. `chmod 777 es-data`
3. Run: `docker-compose up`
4. Run the synchronization script to populate the index with READMEs. `python backend/app/synchronize_index.py --number k`. `k` can be from `1` to `40,000`. I tried with `5,000`.
5. Search for models whose README contain `bert`, `curl -X 'GET' 'http://localhost:8000/search/?query=bert' -H 'accept: application/json'`
6. You can also visit `http://localhost:8000/docs/`. To visit the swagger doc. Note that you can `POST` to `/model/` endpoint to manually add data to the index as well.

# Design

Model README contents are stored in a local elasticsearch cluster. The REST api is built with FastAPI. The contents of the elasticsearch cluster are synched manually by running the `backend/app/synchronize_index.py` script. 

## Why Elasticsearch?

I considered the following options for storing the READMEs:

1. A python dictionary mapping `model_id` to README content. We would retrive 