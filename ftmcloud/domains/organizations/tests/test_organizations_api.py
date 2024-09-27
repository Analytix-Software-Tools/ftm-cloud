# coding: utf-8

from fastapi.testclient import TestClient


def test_add_organization(client: TestClient):
    """Test case for add_organization

    Add Organization
    """
    organization = {"name":"Test Organization","description":"Organization","pid":"Test pid","created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/organizations/",
        headers=headers,
        json=organization,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_organization(client: TestClient):
    """Test case for delete_organization

    Delete Organization
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/organizations/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_organization(client: TestClient):
    """Test case for get_organization

    Get Organization
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/organizations/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_organizations(client: TestClient):
    """Test case for get_organizations

    Get Organizations
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/organizations/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_organization(client: TestClient):
    """Test case for patch_organization

    Patch Organization
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/organizations/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

