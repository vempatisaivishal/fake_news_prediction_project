import json
import requests
class subjective:
    def __init__(self):
        self.headers = {"Authorization": "Bearer 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"}
        self.API_URL = "https://api-inference.huggingface.co/models/lighteternal/fact-or-opinion-xlmr-el"

    def send_request(self, text):
        data = self.query({"inputs": text})
        print(data)
        data1, label = data[0][0]['score'], data[0][0]['label']
        if label == 'LABEL_0':
            return "subjective"
        else:
            return "objective"

    def query(self, payload):
        send_data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=send_data)
        return json.loads(response.content.decode("utf-8"))