# coding: utf-8

from fastapi.testclient import TestClient


def test_get_privilege(client: TestClient):
    """Test case for get_privilege

    Get Privilege
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/privileges/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_privileges(client: TestClient):
    """Test case for get_privileges

    Get Privileges
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/privileges/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

