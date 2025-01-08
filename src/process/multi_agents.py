from openai import AzureOpenAI
import streamlit as st
import os
import time
from datetime import datetime
from pathlib import Path
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
from process.agents import AgentFactory
from process.api_call import FinancialModelingPrepAPI
from process.llm_router import LLMRouter
from process.api_response_preprocessing import PreprocessResponse
from .utils import metrics_data
from process.logger import Logger

logger = Logger()

class MultiAgentSystem:
    def __init__(self, azure_endpoint, azure_key, api_version):
        self.azure_client = AzureOpenAI(
            api_key=azure_key,  
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self.llm_router = LLMRouter(self.azure_client)
        self.api_client = FinancialModelingPrepAPI()
        self.preprocess = PreprocessResponse()

        logger.log_info(
            message = "Instantiated AzureOpenAI, LLMRouter, FinancialModelingPrepAPI and PreprocessResponse",
            module_name = "MultiAgentSystem.__init__"
        )

    def process_request(self, user_input, st_status):
        # Route agents
        st.write("Creating the necessary agents...")
        routing_result = self.llm_router.defining_agents(user_input, "define_agents")

        if "Error" in routing_result:
            logger.log_error(
                message = "Error - Check the LLM response, there seems to be an error",
                module_name = "MultiAgentSystem.process_request"
            )
            return routing_result["Error"]
        
        logger.log_info(
            message = "Preparing API Request",
            module_name = "MultiAgentSystem.process_request"
        )
        selected_agents = routing_result["agentes"]
        st.write(f"└── Agents Created... {selected_agents}")

        st.write("Fetching and Preprocessing Data...")
        # Fetch API data
        endpoints = self.get_endpoints_for_agents(selected_agents)
        # Data needed to make an API call
        company_name = routing_result["empresa"]
        ticker = routing_result["ticker"]
        exchange = routing_result["exchange"]
        limit = 100
        _from = "2023-12-04"
        to = "2024-12-04"
        query = ""
        
        api_responses = self.api_client.get_endpoints_data(endpoints, ticker, limit, _from, to, query, exchange, company_name)

        # Call Preprocessing Module
        """
        Send user_input, selected_agents, api_respones, 
        """
        ##Dinamic Cleanup##
        # to_preprocess = self.preprocess.clean_api_response(
        #     agents = selected_agents,
        #     api_responses = api_responses
        # )
        # unnecesary_keys = self.preprocess.llm_preprocess(
        #     key_cleanup = to_preprocess,
        #     llm_router = self.llm_router
        # )

        # data_final = self.preprocess.json_key_cleanup(
        #     keys_to_discard = unnecesary_keys,
        #     api_responses = api_responses
        # )
        ##Static Cleanup##
        data_final = self.preprocess.remove_unnecesary_keys(api_responses, selected_agents)

        st.write("└── Data Preprocessed...")

        agent_factory = AgentFactory()
        agents = []
        tasks = []
        times = []
        token = []

        st.write("Sending data to each agent...")
        if selected_agents:
            agents_qty = len(selected_agents)
            for agent_name in selected_agents:
                AgentClass = agent_factory.get_agent_class(agent_name)
                if AgentClass:
                    agent_ins, task_ins = AgentClass(routing_result["empresa"], data_final)
                    agents.append(agent_ins)
                    tasks.append(task_ins)
                else:
                    print(f"Warning: No agent class found for {agent_name}")
            
            qa_agent, qa_task = agent_factory.create_qa_agent(selected_agents, tasks)
            agents.append(qa_agent)
            tasks.append(qa_task)

            st.write("└── Data Sent...")
            st.write("The data is beign analyzed, you'll see a response soon...")

            result_crew, times, token, outputs = agent_factory.create_crew(agents, tasks, st_status=st_status, agents_qty = agents_qty)
            final_result = result_crew.kickoff()

            executions = list(selected_agents) + ["QA Agent"]
            metrics_data(times, token, outputs, executions, result_crew)
            
            return final_result

    def get_endpoints_for_agents(self, agents):
        # Map agents to relevant endpoints
        logger.log_info(
            message = "Map agents to relevant endpoints",
            module_name = "MultiAgentSystem.get_endpoints_for_agents"
        )

        endpoint_mapping = {
            "Financial": ["income-statement", "cash-flow-statement", "balance-sheet-statement"],
            "Accounting": ["cash-flow-statement-growth", "balance-sheet-statement-growth", "income-statement-growth"],
            "Legal" : ["profile"],
            "Risk": ["rating", "financial-growth"],
            "Investment" : ["stock-price-change", "historical-market-capitalization", "discounted-cash-flow"]
        }
        
        endpoints = []
        for agent in agents:
            endpoints.extend(endpoint_mapping.get(agent, []))
        
        return list(set(endpoints))
