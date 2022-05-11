import gradio as gr
import requests


def search(query: str):
    resp = requests.get(f"http://host.docker.internal:8000/search/?query={query}")
    return resp.json()


def main():
    iface = gr.Interface(search, inputs="text", outputs="json")
    iface.launch( server_name="0.0.0.0", server_port=7000)

if __name__ == "__main__":
    main()