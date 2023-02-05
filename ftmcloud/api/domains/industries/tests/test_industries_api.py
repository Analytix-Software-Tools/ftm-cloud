# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.http_validation_error import HTTPValidationError  # noqa: F401
from openapi_server.models.http_error import HttpError  # noqa: F401
from openapi_server.models.industry import Industry  # noqa: F401
from openapi_server.models.patch_document import PatchDocument  # noqa: F401
from openapi_server.models.response import Response  # noqa: F401
from openapi_server.models.response_industry import ResponseIndustry  # noqa: F401


def test_add_industry(client: TestClient):
    """Test case for add_industry

    Add Industry
    """
    industry = {"name":"Test Organization","description":"Organization","pid":"Test pid","created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/industries/",
        headers=headers,
        json=industry,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_industry(client: TestClient):
    """Test case for delete_industry

    Delete Industry
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/industries/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_industries(client: TestClient):
    """Test case for get_industries

    Get Industries
    """
    params = [("q", 'q_example'),     ("limit", 56),     ("offset", 56),     ("sort", 'sort_example'),     ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/industries/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_industry(client: TestClient):
    """Test case for get_industry

    Get Industry
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/industries/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_industry(client: TestClient):
    """Test case for patch_industry

    Patch Industry
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/industries/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

