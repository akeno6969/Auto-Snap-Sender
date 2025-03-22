import json

def load_credentials(file: str):
    with open(file, 'r') as f:
        return json.load(f)

credentials = load_credentials("config.json")
username = credentials["username"]
password = credentials["password"]