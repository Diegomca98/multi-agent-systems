import os
from dotenv import load_dotenv

load_dotenv()

class EndpointBuilder():
    """
    Initializes the EndpointBuilder with Financial Modeling Prep API configuration.

    Attributes:
        api_key (str): API key retrieved from environment variable 'FMP_API_KEY'.
        base_url (str): Base URL for Financial Modeling Prep API.
        api_version (str): API version used for endpoint construction.
    """
    def __init__(self):
        self.api_key =  os.getenv("FMP_API_KEY")
        self.base_url = "https://financialmodelingprep.com/api"
        self.api_version = "v3"
        
    def setup_endpoint(self, operation, **kwargs):
        """
        Constructs a URL endpoint for the Financial Modeling Prep API.

        Args:
            operation (str): The specific API operation to perform.
            **kwargs: Flexible keyword arguments for endpoint customization.

        Returns:
            str: A fully constructed API endpoint URL.

        Handling scenarios:
        1. Single ticker or company name
        2. Multiple parameters for non-search endpoints
        3. Search ticker endpoint
        4. Basic endpoint without parameters

        Special handling:
        - Converts '_from' parameter to 'from'
        - Dynamically builds query parameters
        - Appends API key to all endpoints
        """
        if len(kwargs.keys()) == 1:
            if "ticker" in kwargs:
                return f"{self.base_url}/{self.api_version}/{operation}/{kwargs['ticker']}?apikey={self.api_key}"
            elif "company_name" in kwargs:
                return f"{self.base_url}/{self.api_version}/{operation}/{kwargs['company_name']}?apikey={self.api_key}"

        if kwargs and operation != "search-ticker":
            count = 0
            query_params = ''
            for key, value in kwargs.items():
                if count == 0:
                    query_params += f"{value}?"
                elif count > 0 and count < len(kwargs.keys()):
                    extend_args = f"{key}={value}"
                    if key == "_from":
                        extend_args = f"from={value}"
                    query_params += extend_args + "&"
                count +=1
            return f"{self.base_url}/{self.api_version}/{operation}/{query_params}apikey={self.api_key}"
        elif kwargs and operation == "search-ticker":
            query_params = ''
            for key, value in kwargs.items():
                extend_args = f"{key}={value}"
                query_params += extend_args + "&"
            return f"{self.base_url}/{self.api_version}/{operation}?{query_params}apikey={self.api_key}"
        
        return f"{self.base_url}/{self.api_version}/{operation}?apikey={self.api_key}"


    def income_statement(self, ticker):
        """
        Generates the income statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual income statement.
        """
        period = "annual"
        operation = "income-statement"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def balance_sheet_statement(self, ticker):
        """
        Generates the balance sheet statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual balance sheet statement.
        """
        period = "annual"
        operation = "balance-sheet-statement"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def cash_flow_statement(self, ticker):
        """
        Generates the cash flow statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual cash flow statement.
        """
        period = "annual"
        operation = "cash-flow-statement"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def cash_flow_statement_growth(self, ticker):
        """
        Generates the cash flow growth statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual cash flow growth statement.
        """
        period = "annual"
        operation = "cash-flow-statement-growth"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def balance_sheet_statement_growth(self, ticker):
        """
        Generates the balance sheet growth statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual balance sheet growth statement.
        """
        period = "annual"
        operation = "balance-sheet-statement-growth"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def income_statement_growth(self, ticker):
        """
        Generates the income growth statement endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual income growth statement.
        """
        period = "annual"
        operation = "income-statement-growth"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def profile(self, ticker):
        """
        Generates the company profile endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for company profile.
        """
        operation = "profile"
        return self.setup_endpoint(operation, ticker = ticker)
        
    def delisted_companies(self):
        """
        Generates the delisted companies endpoint URL.

        Returns:
            str: Constructed API endpoint URL for delisted companies.
        """
        operation = "delisted-companies"
        return self.setup_endpoint(operation)

    def stock_price_change(self, ticker):
        """
        Generates the stock price change endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for stock price change.
        """
        operation = "stock-price-change"
        return self.setup_endpoint(operation, ticker = ticker)
        
    def discounted_cash_flow(self, ticker):
        """
        Generates the discounted cash flow endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for discounted cash flow.
        """
        operation = "discounted-cash-flow"
        return self.setup_endpoint(operation, ticker = ticker)

    def rating(self, ticker):
        """
        Generates the rating company endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for rating company.
        """
        operation = "rating"
        return self.setup_endpoint(operation, ticker = ticker)

    def historical_market_capitalization(self, ticker, limit, _from, to):
        """
        Generates endpoint URL for historical market capitalization data.

        Args:
            ticker (str): Stock ticker symbol.
            limit (int): Number of historical records to retrieve.
            _from (str): Start date for historical data.
            to (str): End date for historical data.

        Returns:
            str: Constructed API endpoint URL for market capitalization history.
        """
        operation = "historical-market-capitalization"
        return self.setup_endpoint(operation, ticker = ticker, limit = limit, _from = _from, to = to)

    def search_ticker(self, query, exchange):
        """
        Generates endpoint URL for ticker search.

        Args:
            query (str): Search term for ticker.
            exchange (str): Stock exchange to search.

        Returns:
            str: Constructed API endpoint URL for ticker search.
        """
        limit = 10
        operation = "search-ticker"
        return self.setup_endpoint(operation, query = query, limit = limit, exchange = exchange)
        
    def cik_search(self, company_name):
        """
        Generates endpoint URL for CIK (Central Index Key) search.

        Args:
            company_name (str): Name of the company to search.

        Returns:
            str: Constructed API endpoint URL for CIK search.
        """
        operation = "cik-search"
        return self.setup_endpoint(operation, company_name = company_name)
        
    def financial_statement_symbol_lists(self):
        """
        Generates the financial symbol list statement endpoint URL.

        Returns:
            str: Constructed API endpoint URL for financial symbol list statement.
        """
        operation = "financial-statement-symbol-lists"
        return self.setup_endpoint(operation)

    def key_metrics(self, ticker):
        """
        Generates the company key metrics endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual company key metrics.
        """
        period = "annual"
        operation = "key-metrics"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def fmp(self):
        """
        Generates endpoint URL for Financial Modeling Prep (FMP) articles.

        Returns:
            str: Constructed API endpoint URL for fetching FMP articles.

        Details:
            - Retrieves 5 articles 
            - Starts from first page (page 0)
        """
        fmp = "articles"
        page = 0
        size = 5
        operation = "fmp"
        return self.setup_endpoint(operation, fmp = fmp, page = page, size = size)

    def financial_statement_full_as_reported(self, ticker):
        """
        Generates the company financial statement as reported on API endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual company financial statement as reported on API.
        """
        period = "annual"
        limit = 50
        operation = "financial-statement-full-as-reported"
        return self.setup_endpoint(operation, ticker = ticker, period = period, limit = limit)

    def financial_growth(self, ticker):
        """
        Generates the financial growth endpoint URL for a specific ticker.

        Args:
            ticker (str): Stock ticker symbol.
        Returns:
            str: Constructed API endpoint URL for annual financial growth.
        """
        period = "annual"
        operation = "financial-growth"
        return self.setup_endpoint(operation, ticker = ticker, period = period)

    def orchestrator(self, endpoint, ticker, limit, _from, to, query, exchange, company_name):
        """
        Centralized method to route API endpoint requests based on endpoint type.

        Args:
            endpoint (str): Specific API endpoint to retrieve.
            ticker (str): Stock ticker symbol.
            limit (int): Limit for historical data.
            _from (str): Start date for historical data.
            to (str): End date for historical data.
            query (str): Search query for ticker.
            exchange (str): Stock exchange.
            company_name (str): Company name for CIK search.

        Returns:
            str: Constructed API endpoint URL for the specified endpoint.
       """
        builder = {
            "income-statement" : self.income_statement(ticker),
            "balance-sheet-statement" : self.balance_sheet_statement(ticker),
            "cash-flow-statement" : self.cash_flow_statement(ticker),
            "cash-flow-statement-growth" : self.cash_flow_statement_growth(ticker),
            "balance-sheet-statement-growth" : self.balance_sheet_statement_growth(ticker),
            "income-statement-growth" : self.income_statement_growth(ticker),
            "profile" : self.profile(ticker),
            "delisted-companies" : self.delisted_companies(),
            "stock-price-change" : self.stock_price_change(ticker),
            "discounted-cash-flow" : self.discounted_cash_flow(ticker),
            "rating" : self.rating(ticker),
            "historical-market-capitalization" : self.historical_market_capitalization(
                ticker, 
                limit, 
                _from, 
                to
            ),
            "search-ticker" : self.search_ticker(query, exchange),
            "cik-search" : self.cik_search(company_name),
            "financial-statement-symbol-lists" : self.financial_statement_symbol_lists(),
            "key-metrics" : self.key_metrics(ticker),
            "fmp" : self.fmp(),
            "financial-statement-full-as-reported" : self.financial_statement_full_as_reported(ticker),
            "financial-growth" : self.financial_growth(ticker)
        }

        return builder[endpoint]