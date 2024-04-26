from utils.http import RequestsHttpClient

class PloomesAPI:
    def __init__(self):
        """
        Initializes PloomesAPI instance.

        Args:
            user_key (str): User key for authentication.
            http_client (HttpClient): HTTP client for making requests.
        """
        self.base_url = 'https://api2.ploomes.com'
        self.headers = {
            'Content-Type': 'application/json',
            'User-Key': ''
        }
        self.http_client = RequestsHttpClient()

    def update_contact(self, data, ploomes_id):
        """
        Updates a contact using the provided data.

        Args:
            data (dict): Contact data.
            ploomes_id (int): ID of the contact to update.

        Returns:
            dict: Response data.
        """
        url = f'{self.base_url}/Contacts({ploomes_id})'
        return self._make_request('PATCH', url, json=data)

    def create_contact(self, data):
        """
        Creates a new contact using the provided data.

        Args:
            data (dict): Contact data.

        Returns:
            dict: Response data.
        """
        url = f'{self.base_url}/Contacts'
        return self._make_request('POST', url, json=data)

    def get_city_id_by_name(self, city_name):
        """
        Retrieves the ID of a city by its name.

        Args:
            city_name (str): Name of the city to search for.

        Returns:
            str: ID of the city if found, None otherwise.
        """
        url = f'{self.base_url}/Cities'
        params = {'$filter': f"Name eq '{city_name}'"}
        data = self._make_request('GET', url, params=params)
        if data.get('value', None):
            return data['value'][0]['Id']
        else:
            print("City not found.")
            return None

    def _make_request(self, method, url, **kwargs):
        """
        Makes an HTTP request with the given method, url, and optional parameters.

        Args:
            method (str): HTTP method (GET, POST, PATCH, etc.).
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to the HTTP client.

        Returns:
            dict: Response data.
        """
        return self.http_client.request(method, url, headers=self.headers, **kwargs)
