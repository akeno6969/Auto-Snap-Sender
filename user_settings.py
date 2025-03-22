import json

def load_user_settings():
    try:
        with open("user_settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            return settings
    except FileNotFoundError:
        print("User settings file not found. Exiting.")
        exit(1)