import json

class Services:
    def __init__(self, path):
        self.path = path

    def read_confid(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)
