import time
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai import LLM
from tiktoken import encoding_for_model

load_dotenv()
"""
class QualityAssurance:
    def __init__(self, conf):
        self.conf = conf
    
    def create_qa_agent(self, agents_type, tasks): 
        qa_agent = Agent(
            role=f'Quality Assurance Analyst for this types of agents: {", ".join(agents_type)}',
            goal=f'Verify and improve quality of the respective {", ".join(agents_type)} analysis',
            backstory=f'''
            Expert in validating agents like {", ".join(agents_type)} analysis content. 
            Ensures information is relevant, accurate, and properly formatted.
            ''',
            llm=self.conf
        )
        
        qa_task = Task(
            description=f'''
            Review and validate the agents {", ".join(agents_type)} analysis.

            Requirements:
            1. Content must be relevant to the agents {", ".join(agents_type)} analysis
            2. Analysis must be clear and well-structured
            3. Remove any redundant or irrelevant information
            4. Ensure numerical data is properly contextualized

            Return only the high-quality, relevant content.
            ''',
            expected_output=f'''
            High-quality {", ".join(agents_type)} analysis with:
            - Relevant information only
            - Clear structure
            - Properly formatted numbers
            - No redundancies
            ''',
            agent=qa_agent,
            context=tasks
        )
        
        return qa_agent, qa_task
        """
        
class AgentFactory:
    def __init__(self):
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        self.conf = LLM(
            model="azure/gpt-4o",
            base_url="https://demos-mexico.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
            api_key=api_key,
            max_tokens=350
        )
        self.allow_delegation = False


    def get_agent_class(self, agent_name):
        agent_mapping = {
            "Financial": self.FinancialAgent,
            "Risk": self.RiskAgent,
            "Investment": self.InvestmentAgent,
            "Accounting": self.AccountingAgent,
            "Legal": self.LegalAgent
        }
        return agent_mapping.get(agent_name)

    def FinancialAgent(self, company, data):
        financial_agent = Agent(
            role = 'Financial Analyst',
            goal = f"Write an insightful and factually accurate financial analysis",
            backstory = """
                You are an agent specialized in financial analysis. 
                Your role is to provide accurate and relevant information about the financial data presented to you. 
                You must act as a financial expert, able to interpret and analyze complex data to offer valuable insights.
                Also you are an expert who creates perfectly formatted Markdown reports. 
                Specializes in consistent number formatting and maintains readability 
                by treating numbers and their units as single, inseparable elements.
                    CRITICAL: You must format ALL output in pure Markdown only:
                    - Use # for main headers
                    - Use ## for subheaders 
                    - Use ** for bold numbers and metrics
                    - NEVER use LaTeX formatting
                    - NEVER use $ symbols for formatting           
            """,
            llm = self.conf,
            allow_delegation = self.allow_delegation,
        )
        financial_task = Task(
            description = f"""
                Your task is to analyze the following financial information that will be provided to you. 
                You must identify patterns, trends and any relevant data that can influence financial decision making. 
                Use your analytical skills to break down information in a clear and understandable way, 
                highlighting the most important aspects.
                Analize Financial data from the company: {company}:
                income-statement:{data['income-statement']},
                cash-flow-statement:{data['cash-flow-statement']},
                balance-sheet-statement:{data['balance-sheet-statement']}
                Avoid the creation of any Latex format, just focus in
                create a Markdown report for {company}
                OUTPUT FORMAT REQUIREMENTS:
                    1. Use ONLY Markdown syntax
                    2. Format numbers like: **50 million**, **25%**, **1.2 billion**
                    3. NEVER use LaTeX or $ symbols
                    4. Use headers: # for titles, ## for sections
                    5. Use bullet points with -
            """,
            expected_output = """
                Based on the analysis of the information provided, 
                you must offer a concise and decisive answer that helps the user make an informed decision. 
                Make sure your answer is clear, direct and based on the data analyzed, 
                highlighting the key points that the user should consider for their financial strategy.
                Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
                Provide a clear Markdown report with:
                    - Proper headers (#, ##)
                    - Bold numbers (**number**)
                    - NO LaTeX formatting
                    - NO $ symbols
                    - Clean bullet points
            """,
            agent = financial_agent
        )
        return financial_agent, financial_task


    def RiskAgent(self, company, data):
        risk_agent = Agent(
            role = 'Risk Analyst',
            goal = f"""
            Write an insightful and factually accurrate risk analysis
            """,
            backstory = """
                You are an agent specialized in the evaluation and management of financial risks. 
                Your role is to identify, analyze and evaluate potential risks associated with financial decisions. 
                You act as a risk mitigation advisor, 
                providing critical information to help minimize uncertainties and maximize financial security.
                Also you are an expert who creates perfectly formatted Markdown reports. 
                Specializes in consistent number formatting and maintains readability 
                by treating numbers and their units as single, inseparable elements.
                    CRITICAL: You must format ALL output in pure Markdown only:
                    - Use # for main headers
                    - Use ## for subheaders 
                    - Use ** for bold numbers and metrics
                    - NEVER use LaTeX formatting
                    - NEVER use $ symbols for formatting     
            """,
            llm = self.conf,
            allow_delegation = self.allow_delegation,
        )
        risk_task = Task(
            description = f"""
                Your task is to analyze the following financial information with a focus on identifying risks. 
                You must evaluate the possible financial, economic and market risks that may affect strategic decisions. 
                Use your skills to break down information and highlight the most significant risks and their potential impacts.
                Evaluate financial risks data from this company: {company}:
                rating:{data['rating']},
                financial-growth:{data['financial-growth']}
                Avoid the creation of any Latex format, just focus in
                create a Markdown report for {company}
                OUTPUT FORMAT REQUIREMENTS:
                    1. Use ONLY Markdown syntax
                    2. Format numbers like: **50 million**, **25%**, **1.2 billion**
                    3. NEVER use LaTeX or $ symbols
                    4. Use headers: # for titles, ## for sections
                    5. Use bullet points with -
            """,
            expected_output = """
                Based on the analysis of the information provided, 
                you must offer a clear and concise response that identifies the key risks and suggests strategies to mitigate them. 
                Make sure your response is direct and based on the data analyzed, 
                providing practical recommendations to manage the identified risks.
                Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
                Provide a clear Markdown report with:
                    - Proper headers (#, ##)
                    - Bold numbers (**number**)
                    - NO LaTeX formatting
                    - NO $ symbols
                    - Clean bullet points
            """,
            agent = risk_agent
        )
        return risk_agent, risk_task

    def InvestmentAgent(self, company, data):
        investment_agent = Agent(
            role = 'Investment Analyst',
            goal = f" Write an insightful and factually accurrate investment analysis",
            backstory = """
                You are an agent specialized in investment strategies and analysis of market opportunities. 
                Your role is to provide accurate and relevant information on available investment options, 
                acting as a trusted advisor in portfolio optimization. 
                You must interpret and analyze financial data to offer valuable insights that help in making investment decisions.
                Also you are an expert who creates perfectly formatted Markdown reports. 
                Specializes in consistent number formatting and maintains readability 
                by treating numbers and their units as single, inseparable elements.
                    CRITICAL: You must format ALL output in pure Markdown only:
                    - Use # for main headers
                    - Use ## for subheaders 
                    - Use ** for bold numbers and metrics
                    - NEVER use LaTeX formatting
                    - NEVER use $ symbols for formatting     
            """,
            llm = self.conf,
            allow_delegation = self.allow_delegation,
        )
        investment_task = Task(
            description = f"""
                Your task is to analyze the following financial information with a focus on identifying investment opportunities. 
                You should evaluate the investment options available, considering factors such as expected return, 
                associated risk and market trends. 
                Use your analytical skills to break down information and highlight the most promising opportunities.
                Make an analysis investment potential from this company: {company}:
                stock-price-change:{data['stock-price-change']},
                discounted-cash-flow:{data['discounted-cash-flow']},
                historical-market-capitalization:{data['historical-market-capitalization']}
                Avoid the creation of any Latex format, just focus in
                create a Markdown report for {company}
                OUTPUT FORMAT REQUIREMENTS:
                    1. Use ONLY Markdown syntax
                    2. Format numbers like: **50 million**, **25%**, **1.2 billion**
                    3. NEVER use LaTeX or $ symbols
                    4. Use headers: # for titles, ## for sections
                    5. Use bullet points with -
            """,
            expected_output = """
                Based on the analysis of the information provided, 
                You must offer a clear and concise answer that identifies the best investment opportunities. 
                Make sure your answer is direct and based on the data analyzed, 
                providing practical recommendations to optimize the user's investment portfolio.
                Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
                Provide a clear Markdown report with:
                    - Proper headers (#, ##)
                    - Bold numbers (**number**)
                    - NO LaTeX formatting
                    - NO $ symbols
                    - Clean bullet points
            """,
            agent = investment_agent
        )
        return investment_agent, investment_task

    def AccountingAgent(self, company, data):
        accounting_agent = Agent(
            role = 'Accounting Specialist Analyst',
            goal = f" Write an insightful and factually accurrate accounting analysis",
            backstory = """
                You are an agent specialized in accounting and financial management. 
                Your role is to provide accurate and relevant information about the company's accounting records 
                and financial situation. You act as a trusted advisor in the interpretation of financial statements 
                and in the optimization of accounting processes.
                Also you are an expert who creates perfectly formatted Markdown reports. 
                Specializes in consistent number formatting and maintains readability 
                by treating numbers and their units as single, inseparable elements.
                    CRITICAL: You must format ALL output in pure Markdown only:
                    - Use # for main headers
                    - Use ## for subheaders 
                    - Use ** for bold numbers and metrics
                    - NEVER use LaTeX formatting
                    - NEVER use $ symbols for formatting     
            """,
            llm = self.conf,
            allow_delegation = self.allow_delegation,
        )
        accounting_task = Task(
            description = f"""
                Your task is to analyze the following accounting information that will be provided to you. 
                You must review financial records, identify discrepancies, and ensure the accuracy of accounting data. 
                Use your skills to break down information in a clear and understandable way, 
                highlighting the most important aspects for financial management.
                Analyze accounting records data from this company: {company}:
                cash-flow-statement-growth:{data['cash-flow-statement-growth']},
                balance-sheet-statement-growth:{data['balance-sheet-statement-growth']},
                income-statement-growth:{data['income-statement-growth']}
                Avoid the creation of any Latex format, just focus in
                create a Markdown report for {company}
                OUTPUT FORMAT REQUIREMENTS:
                    1. Use ONLY Markdown syntax
                    2. Format numbers like: **50 million**, **25%**, **1.2 billion**
                    3. NEVER use LaTeX or $ symbols
                    4. Use headers: # for titles, ## for sections
                    5. Use bullet points with -
            """,
            expected_output = """
                Based on the analysis of the accounting information provided, 
                you must offer a clear and concise answer that summarizes the current financial situation. 
                Make sure your answer is direct and based on the data analyzed, 
                providing practical recommendations to improve accounting efficiency and the accuracy of financial records.
                Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
                Provide a clear Markdown report with:
                    - Proper headers (#, ##)
                    - Bold numbers (**number**)
                    - NO LaTeX formatting
                    - NO $ symbols
                    - Clean bullet points
            """,
            agent = accounting_agent
        )
        return accounting_agent, accounting_task

    def LegalAgent(self, company, data):
        legal_agent = Agent(
            role = 'Legal Compliance Expert Analyst',
            goal = f" Write an insightful and factually accurrate legal analysis",
            backstory = """
                You are an agent specialized in legal matters and regulatory compliance in the financial field. 
                Your role is to provide accurate and relevant information on the legal implications of financial decisions, 
                acting as a trusted advisor on regulatory and compliance issues. 
                You must interpret and analyze legal and regulatory documents to provide valuable insights
                that help ensure compliance and minimize legal risks.
                Also you are an expert who creates perfectly formatted Markdown reports. 
                Specializes in consistent number formatting and maintains readability 
                by treating numbers and their units as single, inseparable elements.
                    CRITICAL: You must format ALL output in pure Markdown only:
                    - Use # for main headers
                    - Use ## for subheaders 
                    - Use ** for bold numbers and metrics
                    - NEVER use LaTeX formatting
                    - NEVER use $ symbols for formatting     
            """,
            llm = self.conf,
            allow_delegation = self.allow_delegation,
        )
        legal_task = Task(
            description = f"""
                Your task is to analyze the following information that will be provided to you. 
                You should identify legal implications, assess regulatory compliance, and highlight any potential legal risks. 
                Use your skills to break down information in a clear and understandable manner, 
                ensuring that all applicable regulations are met.
                Reviwe legal compliance data from this company: {company}:
                profile:{data['profile']}
                Avoid the creation of any Latex format, just focus in
                create a Markdown report for {company}
                OUTPUT FORMAT REQUIREMENTS:
                    1. Use ONLY Markdown syntax
                    2. Format numbers like: **50 million**, **25%**, **1.2 billion**
                    3. NEVER use LaTeX or $ symbols
                    4. Use headers: # for titles, ## for sections
                    5. Use bullet points with -
            """,
            expected_output = """
                Based on your analysis of the legal information provided, 
                you should provide a clear and concise response that summarizes the legal and regulatory implications. 
                Make sure your response is direct and based on the data analyzed, 
                providing practical recommendations to ensure compliance and mitigate any legal risks identified.
                Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
                Provide a clear Markdown report with:
                    - Proper headers (#, ##)
                    - Bold numbers (**number**)
                    - NO LaTeX formatting
                    - NO $ symbols
                    - Clean bullet points
                            """,
            agent = legal_agent
        )

        return legal_agent, legal_task

    def create_qa_agent(self, agents_type, tasks): 
        qa_agent = Agent(
            role=f'Quality Assurance Analyst for this types of agents: {", ".join(agents_type)}',
            goal=f'Verify and improve quality of the respective {", ".join(agents_type)} analysis',
            backstory=f'''
            Expert in validating agents like {", ".join(agents_type)} analysis content. 
            Ensures information is relevant, accurate, and properly formatted.
            Also you are an expert who creates perfectly formatted Markdown reports.
            Expert in validating and ensuring pure Markdown formatting.
            NEVER allow LaTeX formatting to pass through.
            Convert any LaTeX to proper Markdown formatting. 
            ''',
            llm=self.conf
        )
        
        qa_task = Task(
            description=f'''
            Review and validate the agents {", ".join(agents_type)} analysis.

            Requirements:
            1. Content must be relevant to the agents {", ".join(agents_type)} analysis
            2. Analysis must be clear and well-structured
            3. Remove any redundant or irrelevant information
            4. Ensure numerical data is properly contextualized

            Return only the high-quality, relevant content.
            Avoid the creation of any Latex format, just focus in
            create a Markdown report
            FORMATTING REQUIREMENTS:
            - Pure Markdown only
            - NO LaTeX allowed
            - Replace $ with "USD" in text
            - Bold numbers with **
            ''',
            expected_output=f'''
            High-quality {", ".join(agents_type)} analysis with:
            - Relevant information only
            - Clear structure
            - Properly formatted numbers
            - No redundancies
            Make sure the report is a perfectly formatted Markdown with proper headers and consistent number formatting
            ''',
            agent=qa_agent,
            context=tasks
        )
        
        return qa_agent, qa_task

    def create_crew(self, agents, tasks, st_status, agents_qty):
        timing = []
        timing.append(time.time())
        token = []
        self.encoding = encoding_for_model("gpt-4")
        outputs = []
        count = 0 
        
        def step_callback(formatted_answer, st_status=st_status, c_agents = count, agents_qty = agents_qty):
            timing.append(time.time())
            outputs.append(formatted_answer.output)
            c_agents += 1
            
            if c_agents <= agents_qty:
                st_status.write(formatted_answer.output)

            if timing[-1] - timing[-2] < 15:
                time.sleep(15)

            tokens = len(self.encoding.encode(str(formatted_answer.output)))
            token.append(tokens)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            manager_llm=self.conf,
            verbose=True,
            step_callback=step_callback
        )
        
        return crew, timing, token, outputs




        