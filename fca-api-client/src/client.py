from typing import Optional, List, Dict, Any
import requests
from fca_models import FirmData, FirmNames, FirmNameDetail, FirmAddress, FirmControlledFunction
from fca_models import FirmControlledFunctionDetail, IndividualData, FirmRequirement, FirmRegulator
from fca_models import FirmWaiver, FirmExclusion, FirmDisciplinaryHistory, FirmAppointedRepresentative
from fca_models import FirmActivitiesAndPermissions, FirmActivityDetail, FirmInvestmentType
from auth import get_auth_headers  # Import the simplified function
from utils import rate_limiter
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class FCAApiClient:
    BASE_URL = "https://register.fca.org.uk/services/V0.1"
    
    def __init__(self):
        self.headers = get_auth_headers()  # Use the simplified function
        self.rate_limit = rate_limiter(300)  # 50 requests per 10 seconds = 300 requests per minute

    @rate_limiter(300)
    def search_firms(self, query: str) -> List[Dict[str, Any]]:
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
        try:
            url = f"{self.BASE_URL}/firms/search"
            response = requests.get(url, headers=self.headers, params={"query": query})
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
            return []  # Return an empty list as a fallback
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}"
            headers = self.headers
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                firm_data = response.json()
                logger.info(f"Firm data retrieved successfully for FRN: {frn}")
                if 'Data' in firm_data and isinstance(firm_data['Data'], list) and len(firm_data['Data']) > 0:
                    return FirmData(**firm_data['Data'][0])
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Names"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                firm_names_data = response.json()
                logger.info(f"Firm names retrieved successfully for FRN: {frn}")
                if 'Data' in firm_names_data and isinstance(firm_names_data['Data'], list) and len(firm_names_data['Data']) > 0:
                    return [FirmNames(**name) for name in firm_names_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Address"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                firm_addresses_data = response.json()
                logger.info(f"Firm addresses retrieved successfully for FRN: {frn}")
                if 'Data' in firm_addresses_data and isinstance(firm_addresses_data['Data'], list) and len(firm_addresses_data['Data']) > 0: 
                    return [FirmAddress(**address) for address in firm_addresses_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/CF"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                controlled_functions_data = response.json()
                logger.info(f"Controlled functions retrieved successfully for FRN: {frn}")
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
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Permissions"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                activities_permissions_data = response.json()
                logger.info(f"Activities and permissions retrieved successfully for FRN: {frn}")
                if 'Data' in activities_permissions_data and isinstance(activities_permissions_data['Data'], dict):
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
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Requirements"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                requirements_data = response.json()
                logger.info(f"Requirements retrieved successfully for FRN: {frn}")
                if 'Data' in requirements_data and isinstance(requirements_data['Data'], list) and len(requirements_data['Data']) > 0:
                    return [FirmRequirement(**requirement) for requirement in requirements_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

    def get_firm_investment_types(self, frn: int, reference: str) -> Optional[List[FirmInvestmentType]]:
        """
        Retrieve the investment types associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm investment types endpoint to fetch
        detailed information about the firm's investment types. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmInvestmentType` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmInvestmentType]]: A list of `FirmInvestmentType` objects if the request is successful, otherwise None.
        """
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Requirements/{reference}/InvestmentType"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                investment_types_data = response.json()
                logger.info(f"Investment types retrieved successfully for FRN: {frn}")
                if 'Data' in investment_types_data and isinstance(investment_types_data['Data'], list) and len(investment_types_data['Data']) > 0:
                    return [FirmInvestmentType(**investment_type) for investment_type in investment_types_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None

    def get_firm_individuals(self, frn: int) -> Optional[List[IndividualData]]:
        """
        Retrieve the individuals associated with a specific firm by its Firm Reference Number (FRN).

        This function sends a GET request to the FCA API's firm individuals endpoint to fetch
        detailed information about the firm's individuals. It depends on:
        - The `requests` library for making HTTP requests.
        - The `FirmIndividualData` Pydantic model to parse the API response.

        Args:
            frn (str): The Firm Reference Number.

        Returns:
            Optional[List[FirmIndividualData]]: A list of `FirmIndividualData` objects if the request is successful, otherwise None.
        """
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Individuals"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                individuals_data = response.json()
                logger.info(f"Individuals retrieved successfully for FRN: {frn}")
                if 'Data' in individuals_data and isinstance(individuals_data['Data'], list) and len(individuals_data['Data']) > 0:
                    return [IndividualData(**individual) for individual in individuals_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback

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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Regulators"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                regulators_data = response.json()
                logger.info(f"Regulators retrieved successfully for FRN: {frn}")
                if 'Data' in regulators_data and isinstance(regulators_data['Data'], list) and len(regulators_data['Data']) > 0:
                    return [FirmRegulator(**regulator) for regulator in regulators_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Waivers"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                waivers_data = response.json()
                logger.info(f"Waivers retrieved successfully for FRN: {frn}")
                if 'Data' in waivers_data and isinstance(waivers_data['Data'], list) and len(waivers_data['Data']) > 0:
                    return [FirmWaiver(**waiver) for waiver in waivers_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/Exclusions"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                exclusions_data = response.json()
                logger.info(f"Exclusions retrieved successfully for FRN: {frn}")
                if 'Data' in exclusions_data and isinstance(exclusions_data['Data'], list) and len(exclusions_data['Data']) > 0:
                    return [FirmExclusion(**exclusion) for exclusion in exclusions_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing, not a list, or empty")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/DisciplinaryHistory"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                disciplinary_data = response.json()
                logger.info(f"Disciplinary history retrieved successfully for FRN: {frn}")
                if 'Data' in disciplinary_data and isinstance(disciplinary_data['Data'], list):
                    return [FirmDisciplinaryHistory(**item) for item in disciplinary_data['Data']]
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing or not a list")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
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
        try:
            url = f"{self.BASE_URL}/Firm/{frn}/AR"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                appointed_representatives_data = response.json()
                logger.info(f"Appointed representatives retrieved successfully for FRN: {frn}")
                if 'Data' in appointed_representatives_data and isinstance(appointed_representatives_data['Data'], dict):
                    return FirmAppointedRepresentative(**appointed_representatives_data['Data'])
                else:
                    raise ValueError("Invalid response format: 'Data' field is missing or not a dictionary")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for FRN {frn}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value error for FRN {frn}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred for FRN {frn}: {e}")
            return None
        return None  # Return None as a fallback





