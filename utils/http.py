import requests
import sys

class RequestsHttpClient():

    @staticmethod
    def request(method, url, **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            print(f"HTTP request successful: {method} {url} {kwargs}")
            print(response.text)
            return response.json()
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            print("Retrying...")
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                print(f"HTTP request successful: {method} {url} {kwargs}")
                print(response.text)
                return response.json()
            except requests.RequestException as e:
                print(f"HTTP request failed: {e}")
                print("Retrying...")
                try:
                    response = requests.request(method, url, **kwargs)
                    response.raise_for_status()
                    print(f"HTTP request successful: {method} {url} {kwargs}")
                    print(response.text)
                    return response.json()
                except requests.RequestException as e:
                    raise ValueError(f"HTTP request failed: {e}")
