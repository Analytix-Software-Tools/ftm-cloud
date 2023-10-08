# coding: utf-8

from fastapi.testclient import TestClient


def test_delete_user(client: TestClient):
    """Test case for delete_user

    Delete User
    """

    headers = {
    }
    
    response = client.request(
        "DELETE",
        "/api/v0/users/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_user(client: TestClient):
    """Test case for get_user

    Get User
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/api/v0/users/{pid}".format(pid='pid_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_users(client: TestClient):
    """Test case for get_users

    Get Users
    """
    params = [("limit", 56), ("include_totals", True)]
    headers = {
    }
    response = client.request(
        "GET",
        "/api/v0/users/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_login_user(client: TestClient):
    """Test case for login_user

    Login User
    """
    user_sign_in = {"email":"s7@user.com","password":"test"}

    headers = {
    }

    response = client.request(
        "POST",
        "/api/v0/users/login",
        headers=headers,
        json=user_sign_in,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_patch_user(client: TestClient):
    """Test case for patch_user

    Patch User
    """
    patch_document = [{"op":"add","path":"/name","value":"New name value"}]

    headers = {
    }
    response = client.request(
        "PATCH",
        "/api/v0/users/{pid}".format(pid='pid_example'),
        headers=headers,
        json=patch_document,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_signup_user(client: TestClient):
    """Test case for signup_user

    Signup User
    """
    user = {"first_name":"First","last_name":"Last","email":"user@user.com","gallery_pids":["6245c82b1b91870b51573438","6245c82b1b91870b51573439"],"privilege_pid":"6245c82b1b91870b51573559","is_deleted":"false","organization_pid":"organization","pid":"userPid","created_at":"2022-03-17T00:54:43.924+00:00"}

    headers = {
    }
    response = client.request(
        "POST",
        "/api/v0/users/",
        headers=headers,
        json=user,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_users_profile(client: TestClient):
    """Test case for users_profile

    Users Profile
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/api/v0/users/profile",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

