from openai import AzureOpenAI

class AzureOpenAIClient:
    def __init__(self, endpoint, key):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=key,
            api_version="2024-02-01"
        )