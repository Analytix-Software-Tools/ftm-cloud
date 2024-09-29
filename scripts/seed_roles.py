import pymongo
import requests

from ftmcloud.core.config.config import Settings

openapi_url2 = "http://localhost:8080/openapi.json"
openapi_url = "https://ftmcloud-dev.azurewebsites.net/openapi.json"


def fetch_openapi_json(url):
    """Fetch the OpenAPI JSON from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenAPI JSON: {e}")
        return None


def parse_openapi_endpoints(openapi_data):
    """Parse the OpenAPI data to extract URLs and methods."""
    endpoints = []
    if 'paths' in openapi_data:
        for path, methods in openapi_data['paths'].items():
            for method in methods.keys():
                # Convert method to uppercase and store in the required format
                new_path = path.replace('/api/v0', '')
                new_path = new_path[1:]
                if new_path[-1] == "/":
                    new_path = new_path[:-1]
                endpoint = f"{method.upper()}:{new_path.split('/')[0]}"
                endpoints.append(endpoint)
    return endpoints


def seed_user_roles_on_admin():
    config = Settings()
    db = pymongo.MongoClient(
        host=config.MONGO_URI
    )
    new_permissions = []
    openapi_data = fetch_openapi_json(openapi_url)

    if openapi_data:
        # Parse the endpoints
        endpoints = parse_openapi_endpoints(openapi_data)
        for _endpoint in endpoints:
            new_permissions.append(_endpoint)
    db['analytix']['privileges'].update_one(
        filter={"name": "developer"},
        update={"$set": {"permissions": new_permissions}}
    )


if __name__ == '__main__':
    seed_user_roles_on_admin()
