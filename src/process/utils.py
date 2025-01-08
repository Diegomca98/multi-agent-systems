import pandas as pd
import os
from datetime import datetime

def get_endpoint_mapping(agent_list):
    selected_agents_endpoints = {}

    endpoints = {
        "Financial": [
            "income-statement", 
            "cash-flow-statement", 
            "balance-sheet-statement"
        ],
        "Accounting": [
            "cash-flow-statement-growth", 
            "balance-sheet-statement-growth", 
            "income-statement-growth"
        ],
        "Legal" : [
            "profile", 
        ],
        "Risk": [
            "rating", 
            "financial-growth"
        ],
        "Investment" : [
            "stock-price-change", 
            "historical-market-capitalization", 
            "discounted-cash-flow"
        ]
    }

    if agent_list == list(endpoints.keys()):
        return endpoints
    else:
        for agent in agent_list:
            selected_agents_endpoints[agent] = endpoints[agent]
        return selected_agents_endpoints


def show_example_cleaned(data):
    print(data)

def print_metrics(times, token, outputs, executions, summary_crew):
    execution_time = []
    for i in range(len(times)-1):
        execution_time.append(times[i+1] - times[i])

    # DataFrame para métricas
    metrics_data = {
        'agent': executions,
        'execution_time': execution_time,
        'output_agent_tokens': token,
        'total_tokens': summary_crew.usage_metrics.total_tokens,
        'prompt_tokens': summary_crew.usage_metrics.prompt_tokens,
        'completion_tokens': summary_crew.usage_metrics.completion_tokens,
        'timestamp': [datetime.now()] * len(executions),
    }
    
    # DataFrame para outputs
    outputs_data = {
        'agent': executions,
        'output': outputs
    }

    df_metrics = pd.DataFrame(metrics_data)
    df_outputs = pd.DataFrame(outputs_data)

    # Appendear a CSVs existentes
    metrics_file = "Metrics.csv"
    outputs_file = "Outputs_Agents.csv"

    # Para métricas
    if not os.path.exists(metrics_file):
        df_metrics.to_csv(metrics_file, index=False)
    else:
        df_metrics.to_csv(metrics_file, mode='a', header=False, index=False)

    # Para outputs
    if not os.path.exists(outputs_file):
        df_outputs.to_csv(outputs_file, index=False)
    else:
        df_outputs.to_csv(outputs_file, mode='a', header=False, index=False)

    print(f"\nData appended to:")
    print(f"Metrics: {metrics_file}")
    print(f"Outputs: {outputs_file}")