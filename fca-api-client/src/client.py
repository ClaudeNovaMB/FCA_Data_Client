from typing import Optional, List, Dict, Any
import requests
from fca_models import FirmData, FirmNames, FirmAddress, FirmControlledFunction, FirmQuery
from fca_models import FirmControlledFunctionDetail, IndividualData, FirmRequirement, FirmRegulator
from fca_models import FirmWaiver, FirmExclusion, FirmDisciplinaryHistory, FirmAppointedRepresentative
from fca_models import FirmActivitiesAndPermissions, FirmActivityDetail, FirmInvestmentType
from fca_models import IndividualControlFunction, IndividualControlFunctionDetail, IndividualDisciplinaryHistory
from auth import get_auth_headers
from utils import setup_logging_to_db
import time
from threading import Lock

class FCAApiClient:
    BASE_URL = "https://register.fca.org.uk/services/V0.1"
    RATE_LIMIT_INTERVAL = 10  # 10 seconds
    MAX_REQUESTS = 50

    def __init__(self):
        self.headers = get_auth_headers()
        self.lock = Lock()
        self.request_timestamps = []
        self.client_logger = setup_logging_to_db(logger_name='fca_client_logger', log_type='client')

    def _rate_limit(self):
        """
        Enforce a global rate limit for the client.
        """
        with self.lock:
            now = time.time()
            # Remove timestamps older than the rate limit interval
            self.request_timestamps = [
                ts for ts in self.request_timestamps if now - ts < self.RATE_LIMIT_INTERVAL
            ]
            if len(self.request_timestamps) >= self.MAX_REQUESTS:
                # Calculate the time to wait before the next request
                sleep_time = self.RATE_LIMIT_INTERVAL - (now - self.request_timestamps[0])
                time.sleep(sleep_time)
            # Add the current timestamp
            self.request_timestamps.append(time.time())

    def search_firms(self, query: str) -> Optional[List[FirmQuery]]:
        """
        Search for firms by query string.

        This function sends a GET request to the FCA API's search endpoint to retrieve
        a list of firms matching the provided query. It depends on:
        - The `rate_limiter` decorator to enforce API rate limits.
        - The `parse_firm_data` function to parse the raw JSON response into structured data.
        - The `requests` library for making HTTP requests.

        Args:
            query (str): The search query string.

        Returns:
            List[Dict[str, Any]]: Parsed firm data from the API response.
        """
        self._rate_limit()
        try:
            # Construct the URL for the search endpoint
            'Example : Search?q=Example Ltd&type=firm'
            url = f"{self.BASE_URL}/Search"
            params = {'q': query, 'type': 'firm'}
            response = requests.get(url, headers=self.headers , params=params)
            if response.status_code == 200:
                raw_output = response.json()
                self.client_logger.info(f"Search results retrieved successfully for query: {query}")
                while 'Next' in raw_output['ResultInfo'] and raw_output['ResultInfo']['Next'] is not None:
                    next_url = raw_output['ResultInfo']['Next']
                    next_response = requests.get(next_url, headers=self.headers)
                    if next_response.status_code == 200:
                        next_data = next_response.json()
                        raw_output['Data'].extend(next_data['Data'])
                        raw_output['ResultInfo']['Next'] = next_data['ResultInfo'].get('Next')
                    else:
                        self.client_logger.error(f"Failed to fetch next page: {next_response.status_code}")
                        break
                if raw_output['Data'] is None:
                    self.client_logger.warning(f"No data found for query: {query}")
                    self.client_logger.warning(f"API MESSAGE: {raw_output['Message']}")
                    return []
                else:
                    if 'Data' in raw_output and isinstance(raw_output['Data'], list) and len(raw_output['Data']) > 0:
                        return [FirmQuery(**item) for item in raw_output['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a list")

            else:
                response.raise_for_status()
            return []  # Return an empty list as a fallback
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed: {e}")
            return []
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred: {e}")
            return []
        return []  # Return an empty list as a fallback
    
    def get_firm_data(self, frn: int) -> Optional[FirmData]:
        """
        Retrieve data for a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm endpoint to fetch
        detailed information about a firm. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmData` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[FirmData]: A `FirmData` object if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}"
            headers = self.headers
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                firm_data = response.json()
                self.client_logger.info(f"Firm data retrieved successfully for FRN: {frn}")
                if firm_data['Data'] is None:
                    self.client_logger.warning(f"Firm data not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {firm_data['Message']}")
                    return None
                else:
                    if 'Data' in firm_data and isinstance(firm_data['Data'], list) and len(firm_data['Data']) > 0:
                        return FirmData(**firm_data['Data'][0])
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_names(self, frn: int) -> Optional[List[FirmNames]]:
        """
        Retrieve the names associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm names endpoint to fetch
        detailed information about the firm's names. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmNames` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmNames]]: A list of `FirmNames` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Names"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                firm_names_data = response.json()
                self.client_logger.info(f"Firm names retrieved successfully for FRN: {frn}")
                if firm_names_data['Data'] is None:
                    self.client_logger.warning(f"Firm names not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {firm_names_data['Message']}")
                    return None
                else:
                    if 'Data' in firm_names_data and isinstance(firm_names_data['Data'], list) and len(firm_names_data['Data']) > 0:
                        return [FirmNames(**name) for name in firm_names_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback
    
    def get_firm_addresses(self, frn: int) -> Optional[List[FirmAddress]]:
        """
        Retrieve the addresses associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm addresses endpoint to fetch
        detailed information about the firm's addresses. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmAddress` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmAddress]]: A list of `FirmAddress` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Address"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                firm_addresses_data = response.json()
                self.client_logger.info(f"Firm addresses retrieved successfully for FRN: {frn}")
                if firm_addresses_data['Data'] is None:
                    self.client_logger.warning(f"Firm addresses not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {firm_addresses_data['Message']}")
                    return None
                else:
                    if 'Data' in firm_addresses_data and isinstance(firm_addresses_data['Data'], list) and len(firm_addresses_data['Data']) > 0: 
                        return [FirmAddress(**address) for address in firm_addresses_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_controlled_functions(self, frn: int) -> Optional[FirmControlledFunction]:
        """
        Retrieve the controlled functions associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm controlled functions endpoint to fetch
        detailed information about the firm's controlled functions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmControlledFunction` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[FirmControlledFunction]: A `FirmControlledFunction` object if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/CF"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                controlled_functions_data = response.json()
                self.client_logger.info(f"Controlled functions retrieved successfully for FRN: {frn}")
                if controlled_functions_data['Data'] is None:
                    self.client_logger.warning(f"Controlled functions not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {controlled_functions_data['Message']}")
                    return None
                else:
                    if 'Data' in controlled_functions_data and isinstance(controlled_functions_data['Data'], list) and len(controlled_functions_data['Data']) > 0:
                        # Map the response data to the FirmControlledFunction model
                        data = controlled_functions_data['Data'][0]
                        current = {key: FirmControlledFunctionDetail(**value) for key, value in data.get('Current', {}).items()} if data.get('Current') else {}
                        previous = {key: FirmControlledFunctionDetail(**value) for key, value in data.get('Previous', {}).items()} if data.get('Previous') else {}
                        return FirmControlledFunction(Current=current, Previous=previous)
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_activities_and_permissions(self, frn: int) -> Optional[List[FirmActivitiesAndPermissions]]:
        """
        Retrieve the activities and permissions associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm activities and permissions endpoint to fetch
        detailed information about the firm's activities and permissions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmActivitiesAndPermissions` and `FirmActivityDetail` Pydantic models to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmActivitiesAndPermissions]]: A list of `FirmActivitiesAndPermissions` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Permissions"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                activities_permissions_data = response.json()
                self.client_logger.info(f"Activities and permissions retrieved successfully for FRN: {frn}")
                #check if Data value is None
                if activities_permissions_data['Data'] is None:
                    self.client_logger.warning(f"Activities and permissions not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {activities_permissions_data['Message']}")
                    return None
                else:
                    if 'Data' in activities_permissions_data and isinstance(activities_permissions_data['Data'], dict) :

                        parsed_activities = []
                        for activity_name, details in activities_permissions_data['Data'].items():
                            participation_list = []
                            for detail in details:
                                for participation_key, participation_option in detail.items():
                                    participation_list.append(FirmActivityDetail(participation=participation_key, participation_option=participation_option))
                            parsed_activities.append(FirmActivitiesAndPermissions(activity_name=activity_name, participation=participation_list))
                        return parsed_activities
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a dictionary")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_requirements(self, frn: int) -> Optional[List[FirmRequirement]]:
        """
        Retrieve the requirements associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm requirements endpoint to fetch
        detailed information about the firm's requirements. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmRequirement` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmRequirement]]: A list of `FirmRequirement` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Requirements"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                requirements_data = response.json()
                self.client_logger.info(f"Requirements retrieved successfully for FRN: {frn}")
                if requirements_data['Data'] is None:
                    self.client_logger.warning(f"Requirements not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {requirements_data['Message']}")
                    return None
                else:
                    if 'Data' in requirements_data and isinstance(requirements_data['Data'], list) and len(requirements_data['Data']) > 0:
                        return [FirmRequirement(**requirement) for requirement in requirements_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_investment_types(self, frn: int, reference: str) -> Optional[List]:
        """
        Retrieve the investment types associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm investment types endpoint to fetch
        detailed information about the firm's investment types. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmInvestmentType` Pydantic model to parse the API response.

        Args:
            frn (int): The Firm Reference Number.
            reference (str): The reference identifier for the investment types.

        Returns:
            Optional[List[FirmInvestmentType]]: A list of `FirmInvestmentType` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Requirements/{reference}/InvestmentTypes"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                investment_types_data = response.json()
                self.client_logger.info(f"Investment types retrieved successfully for FRN: {frn}")
                if investment_types_data['Data'] is None:
                    self.client_logger.warning(f"Investment types not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {investment_types_data['Message']}")
                    return None
                else:
                    if 'Data' in investment_types_data and isinstance(investment_types_data['Data'], list) and len(investment_types_data['Data']) > 0:
                        return [FirmInvestmentType(**investment_type) for investment_type in investment_types_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None

    def get_firm_individuals(self, frn: int) -> Optional[List[IndividualData]]:
        """
        Retrieve the individuals associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm individuals endpoint to fetch
        detailed information about the firm's individuals. It depends on:
        - The `requests` library for making HTTP requests.
        - The `IndividualData` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[IndividualData]]: A list of `IndividualData` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Individuals"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                individuals_data = response.json()
                self.client_logger.info(f"Individuals retrieved successfully for FRN: {frn}")
                if individuals_data['Data'] is None:
                    self.client_logger.warning(f"Individuals not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {individuals_data['Message']}")
                    return None
                else:
                    if 'Data' in individuals_data:
                        return [individual['IRN'] for individual in individuals_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback
    
    def get_individual_data(self, irn: str) -> Optional[List[IndividualData]]:
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Individuals/{irn}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                individual_data = response.json()
                self.client_logger.info(f"Individual data retrieved successfully for IRN: {irn}")
                if individual_data['Data'] is None:
                    self.client_logger.warning(f"Individual data not found for IRN: {irn}")
                    self.client_logger.warning(f"API MESSAGE: {individual_data['Message']}")
                    return None
                else:
                    if 'Data' in individual_data and isinstance(individual_data['Data'], list):
                        return [IndividualData(**name) for name in individual_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a list")
            else:   
                response.raise_for_status()
            return None  # Return None as a fallback
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for IRN {irn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for IRN {irn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for IRN {irn}: {e}")
            return None

    def get_firm_regulators(self, frn: int) -> Optional[List[FirmRegulator]]:
        """
        Retrieve the regulators associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm regulators endpoint to fetch
        detailed information about the firm's regulators. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmRegulator` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmRegulator]]: A list of `FirmRegulator` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Regulators"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                regulators_data = response.json()
                self.client_logger.info(f"Regulators retrieved successfully for FRN: {frn}")
                if regulators_data['Data'] is None:
                    self.client_logger.warning(f"Regulators not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {regulators_data['Message']}")
                    return None
                else:
                    if 'Data' in regulators_data and isinstance(regulators_data['Data'], list) and len(regulators_data['Data']) > 0:
                        return [FirmRegulator(**regulator) for regulator in regulators_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_waiver(self, frn: int) -> Optional[List[FirmWaiver]]:
        """
        Retrieve the waivers associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm waivers endpoint to fetch
        detailed information about the firm's waivers. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmWaiver` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmWaiver]]: A list of `FirmWaiver` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Waivers"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                waivers_data = response.json()
                self.client_logger.info(f"Waivers retrieved successfully for FRN: {frn}")
                if waivers_data['Data'] is None:
                    self.client_logger.warning(f"Waivers not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {waivers_data['Message']}")
                    return None
                else:
                    if 'Data' in waivers_data and isinstance(waivers_data['Data'], list) and len(waivers_data['Data']) > 0:
                        return [FirmWaiver(**waiver) for waiver in waivers_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
                    
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_exclusions(self, frn: int) -> Optional[List[FirmExclusion]]:
        """
        Retrieve the exclusions associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm exclusions endpoint to fetch
        detailed information about the firm's exclusions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmExclusion` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmExclusion]]: A list of `FirmExclusion` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Exclusions"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                exclusions_data = response.json()
                self.client_logger.info(f"Exclusions retrieved successfully for FRN: {frn}")
                if exclusions_data['Data'] is None:
                    self.client_logger.warning(f"Exclusions not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {exclusions_data['Message']}")
                    return None
                else:
                    if 'Data' in exclusions_data and isinstance(exclusions_data['Data'], list) and len(exclusions_data['Data']) > 0:
                        return [FirmExclusion(**exclusion) for exclusion in exclusions_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_disciplinary_history(self, frn: int) -> Optional[List[FirmDisciplinaryHistory]]:
        """
        Retrieve the disciplinary history for a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's disciplinary history endpoint to fetch
        detailed information about a firm's disciplinary actions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmDisciplinaryHistory` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmDisciplinaryHistory]]: A list of `FirmDisciplinaryHistory` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/DisciplinaryHistory"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                disciplinary_data = response.json()
                self.client_logger.info(f"Disciplinary history retrieved successfully for FRN: {frn}")
                if disciplinary_data['Data'] is None:
                    self.client_logger.warning(f"Disciplinary history not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {disciplinary_data['Message']}")
                    return None
                else:
                    if 'Data' in disciplinary_data and isinstance(disciplinary_data['Data'], list):
                        return [FirmDisciplinaryHistory(**item) for item in disciplinary_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a list")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_appointed_representatives(self, frn: int) -> Optional[FirmAppointedRepresentative]:
        """
        Retrieve the appointed representatives for a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's appointed representatives endpoint to fetch
        detailed information about a firm's appointed representatives. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmAppointedRepresentative` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[FirmAppointedRepresentative]: A `FirmAppointedRepresentative` object if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/AR"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                appointed_representatives_data = response.json()
                self.client_logger.info(f"Appointed representatives retrieved successfully for FRN: {frn}")
                if appointed_representatives_data['Data'] is None:
                    self.client_logger.warning(f"Appointed representatives not found for FRN: {frn}")
                    self.client_logger.warning(f"API MESSAGE: {appointed_representatives_data['Message']}")
                    return None
                else:   
                    if 'Data' in appointed_representatives_data and isinstance(appointed_representatives_data['Data'], dict):
                        return FirmAppointedRepresentative(**appointed_representatives_data['Data'])
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a dictionary")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_individual_control_function(self, irn: str) -> Optional[IndividualControlFunction]:
        """
        Retrieve the control functions associated with a specific individual by their Individual Reference Number (IRN).

        This function sends a GET request to the FCA API's individual control functions endpoint to fetch
        detailed information about an individual's control functions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `IndividualControlFunctionTable` Pydantic model to parse the API response.

        Args:
            irn (str): The Individual Reference Number.

        Returns:
            Optional[List[IndividualControlFunctionTable]]: A list of `IndividualControlFunctionTable` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Individuals/{irn}/CF"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                control_functions_data = response.json()
                self.client_logger.info(f"Control functions retrieved successfully for IRN: {irn}")
                if control_functions_data['Data'] is None:
                    self.client_logger.warning(f"Control functions not found for IRN: {irn}")
                    self.client_logger.warning(f"API MESSAGE: {control_functions_data['Message']}")
                    return None
                else:
                    if 'Data' in control_functions_data and isinstance(control_functions_data['Data'], list):
                        data = control_functions_data['Data'][0]
                        current = {key: IndividualControlFunctionDetail(**value) for key, value in data.get('Current', {}).items()} if data.get('Current') else {}
                        previous = {key: IndividualControlFunctionDetail(**value) for key, value in data.get('Previous', {}).items()} if data.get('Previous') else {}
                        return IndividualControlFunction(Current=current, Previous=previous)
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a list")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for IRN {irn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for IRN {irn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for IRN {irn}: {e}")
            return None
        return None
    
    def get_individual_disciplinary_history(self, irn: str) -> Optional[List[IndividualDisciplinaryHistory]]:
        """
        Retrieve the disciplinary history for a specific individual by their Individual Reference Number (IRN).

        This function sends a GET request to the FCA API's individual disciplinary history endpoint to fetch
        detailed information about an individual's disciplinary actions. It depends on:
        - The `requests` library for making HTTP requests.
        - The `IndividualDisciplinaryHistory` Pydantic model to parse the API response.

        Args:
            irn (str): The Individual Reference Number.

        Returns:
            Optional[List[IndividualDisciplinaryHistory]]: A list of `IndividualDisciplinaryHistory` objects if the request is successful, otherwise None.
        """
        self._rate_limit()
        try:
            url = f"{self.BASE_URL}/Individuals/{irn}/DisciplinaryHistory"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                disciplinary_data = response.json()
                self.client_logger.info(f"Disciplinary history retrieved successfully for IRN: {irn}")
                if disciplinary_data['Data'] is None:
                    self.client_logger.warning(f"Disciplinary history not found for IRN: {irn}")
                    self.client_logger.warning(f"API MESSAGE: {disciplinary_data['Message']}")
                    return None
                else:
                    if 'Data' in disciplinary_data and isinstance(disciplinary_data['Data'], list):
                        return [IndividualDisciplinaryHistory(**item) for item in disciplinary_data['Data']]
                    else:
                        raise ValueError("Invalid response format: 'Data' field is missing or not a list")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.client_logger.error(f"Request failed for IRN {irn}: {e}")
            return None
        except ValueError as e:
            self.client_logger.error(f"Value error for IRN {irn}: {e}")
            return None
        except Exception as e:
            self.client_logger.error(f"An unexpected error occurred for IRN {irn}: {e}")
            return None
        return None
