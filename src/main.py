import os
from dotenv import load_dotenv
import streamlit as st
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
import time

from process.multi_agents import MultiAgentSystem
from process.logger import Logger


load_dotenv()

logger = Logger()

FACTS = [
    "The first credit card was introduced in 1950 by Diners Club",
    "The NYSE processes over 5 billion trades per day",
    "The word 'salary' comes from the Latin word for salt, as Roman soldiers were paid in salt",
    "The first ATM was installed in London in 1967",
    "The Federal Reserve was founded in 1913",
    "The longest bull market lasted 11 years, from 2009 to 2020",
    "The first stock exchange was established in Amsterdam in 1602",
    "Japan has the world's highest debt-to-GDP ratio, over 230%",
    "The first mutual fund was created in Belgium in 1822",
    "Mobile payments first emerged in Finland in 1997",
    "The global financial system processes $5.4 trillion in daily forex trades",
    "The first cryptocurrency, Bitcoin, was created in 2009",
    "The largest banknote ever printed was worth $100,000",
    r"Less than 10% of the world's money exists as physical cash",
    "Warren Buffett bought his first stock at age 11",
    "The term 'bull market' comes from how bulls attack with upward horns",
    "The first ETF was launched in 1993",
    "The best-performing stock of all time is Monster Beverage, up over 100,000%",
    r"90% of day traders lose money",
    "The first modern mutual fund was created in 1924",
    r"The S&P 500 has averaged 10% annual returns historically",
    "The rule of 72 helps estimate investment doubling time",
    r"Only 20% of actively managed funds beat their benchmark",
    "The first hedge fund was created in 1949",
    "Real estate has outperformed stocks in some 30-year periods",
    "The term 'hedge fund' comes from 'hedging' risk",
    "Index funds were first introduced by John Bogle in 1975",
    "Compound interest was called the '8th wonder of the world' by Einstein",
    "The VIX 'fear index' was introduced in 1993",
    r"The largest single-day stock market drop was 22.6% in 1987",
    "Most financial models assume normal distribution of returns",
    "Value at Risk (VaR) was developed by JP Morgan in the 1990s",
    "Systematic risk cannot be diversified away",
    "The first credit default swap was created in 1994",
    "Beta measures a stock's volatility compared to the market",
    "Modern Portfolio Theory was introduced in 1952",
    "Options trading dates back to ancient Greece",
    "The Black-Scholes model revolutionized options pricing",
    "Correlation between assets tends to increase during crises",
    "Risk parity strategies were first used in the 1990s",
    "The first risk management department was created in 1970",
    "Stress testing became mandatory after the 2008 crisis",
    "Double-entry bookkeeping was invented in 1494",
    "GAAP was first established in 1939",
    "The world's first accountants worked in ancient Mesopotamia",
    r"The Big Four accounting firms audit 80% of US public companies",
    "Accounting is called the 'language of business'",
    "The first CPA exam was administered in 1896",
    "IFRS is used in over 140 countries",
    "The word 'audit' comes from Latin 'audire' meaning 'to hear'",
    "Luca Pacioli is known as the father of accounting",
    "The first digital calculator was created for accounting",
    "Accounting scandals led to the creation of Sarbanes-Oxley",
    "The first accounting organization was formed in Venice in 1581",
    "Blockchain is revolutionizing accounting practices",
    "The first accounting software was released in 1978",
    "The oldest written law code is the Code of Ur-Nammu",
    "The term 'corporate veil' was first used in 1809",
    r"Delaware is home to 66% of Fortune 500 companies",
    "The SEC was created in response to the 1929 crash",
    "The first patent law was enacted in Venice in 1474",
    "The longest court case lasted 60 years in India",
    "Corporate personhood was established in 1886",
    "The first commercial arbitration dated back to ancient Egypt",
    "International law began with the Peace of Westphalia",
    "The first trademark was registered in 1870",
    "The UCC has been adopted by all 50 US states",
    "The first copyright law was the Statute of Anne in 1710",
    "Legal precedent comes from the Latin 'stare decisis'",
    "Alternative dispute resolution began in ancient China"
]

def main(user_input, st_status):
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
        user_input = user_input,
        st_status = st_status
    )

    return result

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
            with st.status("Processing your request...", expanded=True) as status:
                result = main(text, status)
                status.update(
                    label = "Completed!",
                    expanded = False,
                    state = "complete"
                )
            
            st.markdown(result, unsafe_allow_html=True)