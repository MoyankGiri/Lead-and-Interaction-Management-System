import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FastAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def login_user(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
            # logger.debug(f"login user {self.token}")

        return None

    def register_user(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "password": password}
        )
        return response.status_code == 200

    def _get_headers(self, token):
        """Return headers including the Authorization token if logged in."""
        headers = {}
        # logger.debug(f"get headers inside {self.token}")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def get_lead_by_id(self, lead_id, token):
        response = requests.get(
            f"{self.base_url}/leads/{lead_id}",
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            result = response.json()
            return result
        return []

    def get_all_leads(self, token):
        # logger.debug(f"get headers {self._get_headers()}")
        response = requests.get(
            f"{self.base_url}/leads",
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            return response.json()
        return []

    def create_lead(self, restaurant_name, address, status, call_frequency, last_call_date, token):
        if last_call_date is None:
            payload = {
                "restaurant_name": restaurant_name,
                "address": address,
                "status": status,
                "call_frequency": call_frequency,
                "last_call_date": last_call_date
            }
        else:
            payload = {
                "restaurant_name": restaurant_name,
                "address": address,
                "status": status,
                "call_frequency": call_frequency,
                "last_call_date": str(last_call_date)
            }
        logger.debug(f"api: {payload}")
        response = requests.post(
            f"{self.base_url}/leads",
            json=payload,
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        return response.status_code == 200
    
    def update_lead(self, lead_id, token, lead_data):
        response = requests.put(
            f"{self.base_url}/leads/{lead_id}",
            headers=self._get_headers(token),
            json=lead_data
        )
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_leads_requiring_calls_today(self, token):
        response = requests.get(
            f"{self.base_url}/leads/due_today",
            headers=self._get_headers(token)
        )
        logger.debug(f"api: {response.json()}")
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                return [result]  # Wrap the single dictionary in a list
            return result

        return []

    def get_pocs_by_lead(self, lead_id, token):
        response = requests.get(
            f"{self.base_url}/pocs/{lead_id}",
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                return [result]  # Wrap the single dictionary in a list
            return result
        return []

    def create_poc(self, lead_id, name, role, phone, email, token):
        payload = {
            "lead_id": lead_id,
            "name": name,
            "role": role,
            "phone": phone,
            "email": email
        }
        response = requests.post(
            f"{self.base_url}/pocs",
            json=payload,
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        return response.status_code == 200

    def get_interactions_by_lead(self, lead_id, token):
        response = requests.get(
            f"{self.base_url}/interactions/{lead_id}",
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                return [result]  # Wrap the single dictionary in a list
            return result
        return []

    def create_interaction(self, lead_id, interaction_date, details, order_placed, token):
        payload = {
            "lead_id": lead_id,
            "interaction_date": str(interaction_date),
            "details": details,
            "order_placed": order_placed
        }
        response = requests.post(
            f"{self.base_url}/interactions",
            json=payload,
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        return response.status_code == 200

    def get_performance_metrics(self, lead_id, token):
        response = requests.get(
            f"{self.base_url}/performance/{lead_id}",
            headers=self._get_headers(token)
        )
        if response.status_code == 401:
            return None
        if response.status_code == 200:
            result = response.json()
            return result
        return []
    def get_well_performing_accounts(self, token):
        response = requests.get(
            f"{self.base_url}/performance/well_performing",
            headers=self._get_headers(token)
        )
        if response.status_code == 200:
            return response.json()
        return []

    def get_underperforming_accounts(self, token):
        response = requests.get(
            f"{self.base_url}/performance/underperforming",
            headers=self._get_headers(token)
        )
        if response.status_code == 200:
            return response.json()
        return []