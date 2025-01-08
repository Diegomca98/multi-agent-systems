import requests
from process.endpoint import EndpointBuilder
from process.logger import Logger

logger = Logger()

class FinancialModelingPrepAPI():
    """
    Client for interacting with the Financial Modeling Prep API.
    This class provides methods to build and retrieve data from various Financial Modeling Prep API endpoints.
    Attributes:
        build_endpoint (EndpointBuilder): An instance used to construct API endpoint URLs.
    """
    def __init__(self):
        """
        Initializes the EndpointBuilder class.
        Creates an EndpointBuilder instance for constructing API endpoint URLs.
        """
        self.build_endpoint = EndpointBuilder()

    def get_endpoints_data(self, endpoints, ticker, limit, _from, to, query, exchange, company_name):
        """
        Retrieves data from multiple API endpoints.
        Args:
            endpoints (list): A list of endpoint names to retrieve data from.
            **kwargs: Variable keyword arguments to be passed to the endpoint URL construction.
        """

        logger.log_info(
            message = "Retrieving data from multiple API endpoints dynamically",
            module_name = "FinancialModelingPrepAPI.get_endpoints_data"
        )

        responses = {}
        for endpoint in endpoints:
            url = self.build_endpoint.orchestrator(
                endpoint, 
                ticker, 
                limit, 
                _from,
                to,
                query,
                exchange,
                company_name
            )
            response = requests.get(url)
            # Check if a response contains any error, if it does you can use:
            ## logger.log_critical(
            #      message = "There was an error with the API"
            #      module_name = ""FinancialModelingPrepAPI.get_endpoints_data""
            # )
            # raise ResponseError(f"{response['Error']}")
            responses[endpoint] = response.json()

        return responses