# coding: utf-8

import pytest
from fastapi.testclient import TestClient

from app import app


def test_add_gallery(client: TestClient):
    """Test case for add_gallery

    Add Gallery
    """
    gallery = {"name": "Test gallery", "description": "test", "organizationPid": "0e1f82df-5872-4466-aa3f-446ec937e5fa", "userPids": []}
    invalid_gallery = {**gallery, 'name': "none", 'organizationPid': 'invalid'}

    headers = {
        "Authorization": "Bearer special-key",
    }
    with TestClient(app) as client:
        response = client.request(
            "POST",
            "/api/v0/galleries/",
            headers=headers,
            json=gallery,
        )

        invalid_gallery_response = client.request(
            "POST",
            "/api/v0/galleries",
            headers=headers,
            json=invalid_gallery
        )

        # uncomment below to assert the status code of the HTTP response
        assert response.status_code == 200
        assert invalid_gallery_response == 404


def test_delete_gallery(client: TestClient):
    """Test case for delete_gallery

    Delete Gallery
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/api/v0/galleries/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_galleries(client: TestClient):
    """Test case for get_galleries

    Get Galleries
    """
    params = [("limit", 2), ("offset", 56), ("include_totals", True)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    with TestClient(app) as client:
        response = client.request(
            "GET",
            "/api/v0/galleries/",
            headers=headers,
            params=params,
        )

        # uncomment below to assert the status code of the HTTP response
        assert response.status_code == 200


def test_get_gallery(client: TestClient):
    """Test case for get_gallery

    Get Gallery
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/api/v0/galleries/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 404


def test_patch_gallery(client: TestClient):
    """Test case for patch_gallery

    Patch Gallery
    """
    patch_document = [{"op": "add", "path": "/name", "value": "New name value"}]

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PATCH",
        "/api/v0/galleries/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
