# coding: utf-8

from fastapi.testclient import TestClient


def test_search_products(client: TestClient):
    """Test case for search_products

    Search Products
    """
    product_search_query = {"search_text": "test", "requirements": [
        {"attribute_pid": "Attribute Pid", "value": {"value": 4}, "is_required": "true"},
        {"attribute_pid": "Attribute Pid", "value": {"value": 4}, "is_required": "true"}],
         "product_type_pid": "0d1c10aa-26d6-4efc-b4e6-39b564e0c79f"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/search/products",
        headers=headers,
        json=product_search_query,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
