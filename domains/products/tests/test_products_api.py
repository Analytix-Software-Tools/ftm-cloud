# coding: utf-8

from fastapi.testclient import TestClient


def test_add_product(client: TestClient):
    """Test case for add_product

    Add Product
    """
    product = {"name":"Test Product","description":"Product","img_url":"imgUrl","pid":"Test pid","product_type_pid":"productTypePid","organization_pid":"organizationPid","attribute_values":[],"created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/products/",
        headers=headers,
        json=product,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_product(client: TestClient):
    """Test case for delete_product

    Delete Product
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/products/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_product(client: TestClient):
    """Test case for get_product

    Get Product
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/products/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_products(client: TestClient):
    """Test case for get_products

    Get Products
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/products/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_product(client: TestClient):
    """Test case for patch_product

    Patch Product
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/products/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

