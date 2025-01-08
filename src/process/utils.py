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

   print("\nAgent Execution Times:")
   for agent, t in zip(executions, execution_time):
       print(f"{agent}: {t:.2f} seconds")

   print("\nAgent tokens:")
   for agent, tok in zip(executions, token):
       print(f"{agent}: {tok}")

   print("\nAgent outputs:")
   for agent, out in zip(executions, outputs):
       print(f"{agent}: {out}")

   print(f"\nUsage metrics: {summary_crew.usage_metrics}")