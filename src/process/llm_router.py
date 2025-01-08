import json
import os
from dotenv import load_dotenv

import process.prompts as prompts
from process.logger import Logger

load_dotenv()

logger = Logger()

class LLMRouter:
    def __init__(self, azure_client):
        self.client = azure_client
        self.prompts_available = {
            "define_agents": prompts.sys_defining_agents,
            "preprocess": prompts.sys_preprocess_data,
            "postprocess": prompts.sys_defining_agents,
        }

    def defining_agents(self, user_input, process):
        logger.log_info(
            message = "Defining Agents to answer user input",
            module_name = "LLMRouter.defininf_agents"
        )

        response = self.client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "system", "content": self.prompts_available[process]},
                {"role": "user", "content": f"####{user_input}####"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def preprocess_data(self, data, process):
        logger.log_info(
            message = "Preprocess - Identify unnecessary keys received from API",
            module_name = "LLMRouter.preprocess_data"
        )

        response = self.client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = [
                {
                    "role": "system",
                    "content": self.prompts_available[process] # process = "preprocess"
                },
                {
                    "role": "user",
                    "content": f"###{data}###"
                },
            ],
            response_format = {
                "type": "json_object"
            }
        )
        return json.loads(response.choices[0].message.content)
    
    def postprocess_data(self, data, process):
        response = self.client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = [
                {
                    "role": "system",
                    "content": self.prompts_available[process] # process = "postprocess"
                },
                {
                    "role": "user",
                    "content": f"###{data}###"
                },
            ],
            response_format = {
                "type": "json_object"
            }
        )
        return json.loads(response.choices[0].message.content)
