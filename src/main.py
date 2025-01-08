import os
from dotenv import load_dotenv
import streamlit as st
from IPython.display import Markdown

from process.multi_agents import MultiAgentSystem
from process.logger import Logger


load_dotenv()

logger = Logger()

# Usage
def main(user_input):
    llm_endpoint = {
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "model": {
            "gpt-4o-mini": "gpt-4o-mini", 
            "gpt-4o": "gpt-4o"
        },
        "version": os.getenv("AZURE_OPENAI_VERSION")
    }

    logger.log_info(
        message = "Starting workflow",
        module_name = "main()"
    )

    multi_agent_system = MultiAgentSystem(
        azure_endpoint = f'{llm_endpoint["endpoint"]}{llm_endpoint["model"]["gpt-4o"]}/chat/completions?api-version={llm_endpoint["version"]}',
        azure_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version= os.getenv("AZURE_OPENAI_VERSION")
    )
 
    result = multi_agent_system.process_request(
        user_input = user_input
    )

    st.markdown(result, unsafe_allow_html=True)

if __name__ == "__main__":

    st.title("🕵️ Sistema Multiagente v0.1 🕵️")
    st.markdown("""
        ---
        > Our software is here to simplify complex topics like finance, accounting, legal matters, risk assestments, and investment by combining the expertise of specialized agents with data sourced from trusted providers like the Financial Modeling Prep API. Think of it as a team of experts working behind the scenes to analyze data and provide you with clear, actionable insights.
        > 
        > Here's what each agent does:
        > - **Financial Agent**: Helps you understand financial trends, create budgets, and analyze data, leveraging up-to-date financial information sourced from the Financial Modeling Prep API.
        > - **Accounting Agent**: Assists with bookkeeping, financial records, and interpreting your financial statements using real-time and historical data for accuracy.
        > - **Legal Agent**: Simplifies legal concepts and helps you navigate compliance, contracts, and regulations without overwhelming legal jargon.
        > - **Risk Agent**: Evaluates potential risks in your decisions, identifies trends, and offers strategies to mitigate them based on reliable financial data.
        > - **Investment Agent**: Provides insights into investment opportunities, evaluates their potencial, and helps you create a long-term growth plan using the latest market data.
        > 
        > This system is designed for everyone, regardless of your background. You don't need to be an expert, simply ask a question or select an area of interest, and our agents will process the data from sources like Financial Modeling Prep API to deliver easy-to-understand recommendations tailored to your needs.

        ---
    """)

    with st.form("my_form"):
        
        text = st.text_input(
            label = "What kind of analysis and which company would you like to check? Please write it down here",
            placeholder = "I want a general evaluation on Apple"
        )
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            main(user_input=text)
