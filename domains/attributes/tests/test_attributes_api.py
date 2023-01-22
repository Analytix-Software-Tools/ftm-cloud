# coding: utf-8

from fastapi.testclient import TestClient


def test_add_attribute(client: TestClient):
    """Test case for add_attribute

    Add Attribute
    """
    attribute = {"name":"Test Attribute","description":"Attribute","pid":"Test pid","created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/attributes/",
        headers=headers,
        json=attribute,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_attribute(client: TestClient):
    """Test case for delete_attribute

    Delete Attribute
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/attributes/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_attribute(client: TestClient):
    """Test case for get_attribute

    Get Attribute
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/attributes/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_attributes(client: TestClient):
    """Test case for get_attributes

    Get Attributes
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/attributes/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_attribute(client: TestClient):
    """Test case for patch_attribute

    Patch Attribute
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/attributes/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

