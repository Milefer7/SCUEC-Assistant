# be/models/llm_model.py
import os

import yaml


class LLMClient:
    def __init__(self):
        # print(os.getcwd())
        with open("be/config/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
        self.url = config["LLM"]["url"]
        self.APPID = config["LLM"]["APPID"]
        self.APIKey = config["LLM"]["APIKey"]
        self.APISecret = config["LLM"]["APISecret"]
        self.host = config["LLM"]["host"]
        self.patch_id = config["LLM"]["resourceId"]
        self.serviceId = config["LLM"]["serviceId"]
        self.temperature = config["LLM"]["temperature"]
        self.max_tokens = config["LLM"]["max_tokens"]
        self.top_k = config["LLM"]["top_k"]
