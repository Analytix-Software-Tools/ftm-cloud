# coding: utf-8

from fastapi.testclient import TestClient


def test_add_category(client: TestClient):
    """Test case for add_category

    Add Category
    """
    category = {"name":"Test Category","description":"Category","pid":"Test pid","parent_category_pid":"parentServiceGroup","created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/categories/",
        headers=headers,
        json=category,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_category(client: TestClient):
    """Test case for delete_category

    Delete Category
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/categories/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_categories(client: TestClient):
    """Test case for get_categories

    Get Categories
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/categories/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_category(client: TestClient):
    """Test case for get_category

    Get Category
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/categories/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_category(client: TestClient):
    """Test case for patch_category

    Patch Category
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/categories/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

