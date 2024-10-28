import os
import yaml

class Config:
    def __init__(self):
        env = os.getenv("APP_ENV", "dev")  # Default to 'dev' if not set
        config_file = f"config/application-{env}.yml"
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        
        with open(config_file, "r") as file:
            self.settings = yaml.safe_load(file)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.settings
        for k in keys:
            value = value.get(k, {})
        return value or default

config = Config()
