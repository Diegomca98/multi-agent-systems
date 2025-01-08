import os
import json
from .utils import get_endpoint_mapping
from process.logger import Logger

logger = Logger()

class PreprocessResponse:        
    def json_exploration(self, user_input, agents, api_responses):
        def serialize_object(obj):
            """
            Recursive function to convert objects to JSON-serializable format
            """
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            elif isinstance(obj, (list, tuple)):
                return [serialize_object(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): serialize_object(v) for k, v in obj.items()}
            else:
                return str(obj)

        exploration = {
            'user_input': {
                'type': str(type(user_input)),
                'content': user_input  # Keep original content
            },
            'agents': {
                'type': str(type(agents)),
                'content': agents  # Keep original list
            },
            'api_responses': {
                'type': str(type(api_responses)),
                'content': api_responses  # Keep original dictionary
            }
        }
        
        # Writing dictionary to a JSON file
        with open('./aia-lab-mx-finance-multiagent/draft_pipeline/data/preprocess_exploration.json', 'w', encoding='utf-8') as json_file:
            json.dump(exploration, json_file, indent=4, ensure_ascii=False)
  
    def clean_api_response(self, agents, api_responses):
        logger.log_info(
            message = "Getting only the keys from JSON response",
            module_name = "PreprocessResponse.clean_api_response"
        )

        to_send_llm = {}
        
        endpoint_mapping = get_endpoint_mapping(
            agent_list = agents
        )
        endpoint_keys = list(endpoint_mapping.keys())

        # print(endpoint_mapping[agent])
        for agent in endpoint_keys:
            to_send_llm[agent] = {}
            for endpoint in endpoint_mapping[agent]:
                #print(api_responses[endpoint])
                to_send_llm[agent][endpoint] = list(
                    api_responses[endpoint][0].keys()
                )

        return to_send_llm

    def llm_preprocess(self, key_cleanup, llm_router):
        logger.log_info(
            message = "Sending JSON keys to LLM for dynamic cleanup",
            module_name = "PreprocessResponse.llm_preprocessing"
        )

        # Send to LLM for preprocessing
        result_key_cleanup = llm_router.preprocess_data(
            data = key_cleanup,
            process = "preprocess"
        )

        return result_key_cleanup 

    def json_key_cleanup(self, keys_to_discard, api_responses):
        logger.log_info(
            message = "JSON key cleanup based on LLM evaluation of necessary information",
            module_name = "PreprocessResponse.json_key_cleanup"
        )

        # Create a single pass to collect keys to eliminate
        eliminate_keys = {
            key: value 
            for agent, endpoints in keys_to_discard.items() 
            for key, value in endpoints.items() 
            if value  # Only include non-empty lists
        }

        # Efficient single-pass key elimination
        for key, discard_list in eliminate_keys.items():
            # Check if the key exists in api_responses
            if key in api_responses:
                # Modify in-place using list comprehension
                api_responses[key] = [
                    {k: v for k, v in response.items() if k not in discard_list}
                    for response in api_responses[key]
                ]

        return api_responses
        
    def remove_unnecesary_keys(self, api_responses, selected_agents):
        to_clean = {
        "Financial" : {
            "income-statement" : ['cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'finalLink', 'link'],
            "cash-flow-statement" : ['cik', 'fillingDate', 'acceptedDate', 'link', 'finalLink', 'calendarYear'],
            "balance-sheet-statement" : ['cik','fillingDate','acceptedDate','calendarYear','period','link','finalLink','minorityInterest','othertotalStockholdersEquity','totalLiabilitiesAndTotalEquity','otherAssets']
            },
        "Accounting" : {
            "cash-flow-statement-growth": ['symbol', 'calendarYear', 'period'],
            "balance-sheet-statement-growth" : ['symbol', 'date', 'calendarYear', 'period', 'growthGoodwill', 'growthIntangibleAssets', 'growthGoodwillAndIntangibleAssets', 'growthDeferredRevenueNonCurrent', 'growthDeferrredTaxLiabilitiesNonCurrent', 'growthOthertotalStockholdersEquity'],
            "income-statement-growth" : [ 'symbol', 'calendarYear', 'period']
            },
        "Legal" : {
            "profile" : ['price', 'beta', 'volAvg', 'lastDiv', 'range', 'changes', 'website', 'image', 'fullTimeEmployees', 'phone', 'address', 'city', 'state', 'zip', 'dcfDiff', 'dcf', 'defaultImage', 'isEtf', 'isActivelyTrading', 'isAdr', 'isFund', 'description', 'ceo', 'ipoDate']
            },
        "Risk" : {
            "rating" : ['symbol', 'date'],
            "financial-growth" : ['calendarYear', 'period','symbol', 'date']
            }
        }
        for agent in selected_agents:
            try:
                for endpoint in to_clean[agent]:
                    for key in to_clean[agent][endpoint]:
                        del api_responses[endpoint][0][key]
            except KeyError:
                pass
                    
        return api_responses