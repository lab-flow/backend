import json

import pytest

from django.urls import reverse

from rest_framework import status

from reagents.models import User

from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, mock_datetime_date_today, model_to_dict


@pytest.mark.django_db
def test_list_users(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                    api_client_anon):
    _, lab_manager = api_client_lab_manager
    _ , project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    client, admin = api_client_admin
    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
    ]

    # Dropping `last_login` because no user has really logged in (that is through the API)
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # Adding a sample user (saving username and password for later login through the API to check `last_login`)
    user_username = "JK"
    user_password = "4TLZL4RH"
    user = User.objects.create_user(
        username=user_username,
        email="jk@jk.pl",
        password=user_password,
        first_name="Jan",
        last_name="Kowalski",
        lab_roles=[User.LAB_MANAGER],
    )

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('user-list')}?ordering=id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    url = f"{reverse('user-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # `username`
    url = f"{reverse('user-list')}?ordering=username"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    url = f"{reverse('user-list')}?ordering=-username"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # `first_name`
    url = f"{reverse('user-list')}?ordering=first_name"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    url = f"{reverse('user-list')}?ordering=-first_name"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # `last_name`
    url = f"{reverse('user-list')}?ordering=last_name"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    url = f"{reverse('user-list')}?ordering=-last_name"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # `email`
    url = f"{reverse('user-list')}?ordering=email"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    url = f"{reverse('user-list')}?ordering=-email"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    # Searching
    # `username`
    url = f"{reverse('user-list')}?search=IŁ"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    assert actual[0].pop("last_login") is None

    assert expected == actual

    # `first_name`
    url = f"{reverse('user-list')}?search=Jan"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    assert actual[0].pop("last_login") is None

    assert expected == actual

    # `last_name`
    url = f"{reverse('user-list')}?search=Łukas"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    assert actual[0].pop("last_login") is None

    assert expected == actual

    # `email`
    url = f"{reverse('user-list')}?search=.pl"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    client, lab_manager = api_client_lab_manager
    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual:
        assert actual_user.pop("last_login") is None

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client = api_client_anon
    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check is `last_login` is updated when we log in through the API
    response = client.post(reverse("token_obtain_pair"), {"username": user_username, "password": user_password})

    assert response.status_code == status.HTTP_200_OK

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": admin.id,
            "username": "IŁ",
            "email": "il@il.pl",
            "first_name": "Ignacy",
            "last_name": "Łukasiewicz",
            "is_staff": True,
            "lab_roles": [],
        },
        {
            "id": lab_manager.id,
            "username": "MSC",
            "email": "msc@msc.pl",
            "first_name": "Maria",
            "last_name": "Skłodowska-Curie",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
        {
            "id": project_manager.id,
            "username": "KO",
            "email": "ko@ko.pl",
            "first_name": "Karol",
            "last_name": "Olszewski",
            "is_staff": False,
            "lab_roles": [User.PROJECT_MANAGER],
        },
        {
            "id": lab_worker.id,
            "username": "ZW",
            "email": "zw@zw.pl",
            "first_name": "Zygmunt",
            "last_name": "Wróblewski",
            "is_staff": False,
            "lab_roles": [User.LAB_WORKER],
        },
        {
            "id": user.id,
            "username": "JK",
            "email": "jk@jk.pl",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_staff": False,
            "lab_roles": [User.LAB_MANAGER],
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    for actual_user in actual[:-1]:
        assert actual_user.pop("last_login") is None

    assert_timezone_now_gte_datetime(actual[-1].pop("last_login"))

    assert expected == actual


@pytest.mark.django_db
def test_create_user(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                     api_client_anon):
    User.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    url = reverse("user-list")

    # Basic user
    post_data = {
        "username": "MS",
        "email": "ms@ms.pl",
        "password": "NMIV9S35",
        "first_name": "Michał",
        "last_name": "Sędziwój",
        "lab_roles": [User.LAB_MANAGER],
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_user.id,
        "is_staff": False,
        "last_login": None,
    }

    # Many roles
    post_data = {
        "username": "KF",
        "email": "kf@kf.pl",
        "password": "GZLL2NVY",
        "first_name": "Kazimierz",
        "last_name": "Funk",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)

    history_data2 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_user.id,
        "is_staff": False,
        "last_login": None,
    }

    # Check history
    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('user-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('user-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        int(history_row.pop("id"))

    assert expected == actual

    # `username`
    response = client.get(f"{reverse('user-get-historical-records')}?ordering=username")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('user-get-historical-records')}?ordering=-username")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `first_name`
    response = client.get(f"{reverse('user-get-historical-records')}?ordering=first_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('user-get-historical-records')}?ordering=-first_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `last_name`
    response = client.get(f"{reverse('user-get-historical-records')}?ordering=last_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('user-get-historical-records')}?ordering=-last_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `email`
    response = client.get(f"{reverse('user-get-historical-records')}?ordering=email")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('user-get-historical-records')}?ordering=-email")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `username`
    response = client.get(f"{reverse('user-get-historical-records')}?search=k")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `first_name`
    response = client.get(f"{reverse('user-get-historical-records')}?search=mic")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `last_name`
    response = client.get(f"{reverse('user-get-historical-records')}?search=nk")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `email`
    response = client.get(f"{reverse('user-get-historical-records')}?search=.pl")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Missing username
    response = client.post(
        url,
        {
            "email": "msb@msb.pl",
            "password": "P0855Y3W",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing email
    response = client.post(
        url,
        {
            "username": "MSB",
            "password": "P0855Y3W",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing password
    response = client.post(
        url,
        {
            "username": "MSB",
            "email": "msb@msb.pl",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing first name (ok for everyone)
    post_data = {
        "username": "MSB",
        "email": "msb@msb.pl",
        "password": "P0855Y3W",
        "last_name": "Sędziwój",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)
    assert not db_user.first_name

    # Missing last name (ok for everyone)
    post_data = {
        "username": "MSBB",
        "email": "msbb@msbb.pl",
        "password": "4R3Q1Z6J",
        "first_name": "Michał",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)
    assert not db_user.last_name

    # Missing lab roles (ok only for admins which can't be created through the API)
    post_data = {
        "username": "MSBC",
        "email": "msbc@msbc.pl",
        "password": "7FI9XTW3",
        "first_name": "Michał",
        "last_name": "Sędziwój",
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique username
    response = client.post(
        url,
        {
            "username": "MSB",
            "email": "msc@msc.pl",
            "password": "C916FB02",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique email
    response = client.post(
        url,
        {
            "username": "MSC",
            "email": "msb@msb.pl",
            "password": "1SNRXO1H",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Trying to set `is_staff`
    post_data = {
        "username": "MSD",
        "email": "msd@msd.pl",
        "password": "A176DHOU",
        "first_name": "Michał",
        "last_name": "Sędziwój",
        "lab_roles": [User.LAB_WORKER],
        "is_staff": True,
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("is_staff") is None

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")
    post_data.pop("is_staff")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)
    assert not db_user.is_staff

    # Trying to set `last_login`
    post_data = {
        "username": "MSE",
        "email": "mse@mse.pl",
        "password": "GU8PZ8SI",
        "first_name": "Michał",
        "last_name": "Sędziwój",
        "lab_roles": [User.LAB_WORKER],
        "last_login": mock_datetime_date_today,
    }
    response = client.post(
        url,
        post_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.get(pk=response.data["id"])
    raw_password = post_data.pop("password")
    post_data.pop("last_login")

    assert post_data.items() <= model_to_dict(db_user).items()
    assert db_user.check_password(raw_password)
    assert db_user.last_login is None

    # Username too short (<2 characters)
    response = client.post(
        url,
        {
            "username": "M",
            "email": "m@m.pl",
            "password": "JZQP8A18",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username too long (>4 characters)
    response = client.post(
        url,
        {
            "username": "MSAAA",
            "email": "msaaa@msaaa.pl",
            "password": "EMQCA6VQ",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with lower case letters
    response = client.post(
        url,
        {
            "username": "MSAu",
            "email": "msau@msau.pl",
            "password": "9E1UK92A",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with characters outside of the Polish alphabet
    response = client.post(
        url,
        {
            "username": "MSAÜ",
            "email": "msau@msau.pl",
            "password": "R9SQEOHL",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    # Password too similar to user's attributes
    response = client.post(
        url,
        {
            "username": "MSAU",
            "email": "msau@msau.pl",
            "password": "sedziwoj",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too short (minimum 8 letters)
    response = client.post(
        url,
        {
            "username": "MSAU",
            "email": "msau@msau.pl",
            "password": "KAJXSJ8",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too common
    response = client.post(
        url,
        {
            "username": "MSAU",
            "email": "msau@msau.pl",
            "password": "password",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password entirely numeric
    response = client.post(
        url,
        {
            "username": "MSAU",
            "email": "msau@msau.pl",
            "password": "46290123",
            "first_name": "Michał",
            "last_name": "Sędziwój",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client, _ = api_client_lab_manager
    url = reverse("user-list")
    response = client.post(
        url,
        {
            "username": "SK",
            "email": "sk@sk.pl",
            "password": "DNHALPRJ",
            "first_name": "Stanisław",
            "last_name": "Kostanecki",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager
    url = reverse("user-list")
    response = client.post(
        url,
        {
            "username": "SK",
            "email": "sk@sk.pl",
            "password": "DNHALPRJ",
            "first_name": "Stanisław",
            "last_name": "Kostanecki",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker
    url = reverse("user-list")
    response = client.post(
        url,
        {
            "username": "SK",
            "email": "sk@sk.pl",
            "password": "DNHALPRJ",
            "first_name": "Stanisław",
            "last_name": "Kostanecki",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    url = reverse("user-list")
    response = client.post(
        url,
        {
            "username": "SK",
            "email": "sk@sk.pl",
            "password": "DNHALPRJ",
            "first_name": "Stanisław",
            "last_name": "Kostanecki",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_user_and_get_current_user_info(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                                 api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("user-detail", args=[admin.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Obviously an admin can retrieve their own info
    expected = {
        "id": admin.id,
        "username": "IŁ",
        "email": "il@il.pl",
        "first_name": "Ignacy",
        "last_name": "Łukasiewicz",
        "is_staff": True,
        "lab_roles": [],
    }
    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    # Both actions should return the same data for an admin.
    url = reverse("user-get-current-user-info")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    # An admin should also be able to retrieve any other person's data
    user_username = "JK"
    user_password = "3GIRT6GM"
    user = User.objects.create_user(
        username=user_username,
        email="jk@jk.pl",
        password=user_password,
        first_name="Jan",
        last_name="Kowalski",
        lab_roles=[User.LAB_MANAGER],
    )

    url = reverse("user-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": "JK",
        "email": "jk@jk.pl",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "is_staff": False,
        "lab_roles": [User.LAB_MANAGER],
    }
    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    # When we log in through the API, `last_login` should change
    response = client.post(reverse("token_obtain_pair"), {"username": user_username, "password": user_password})

    assert response.status_code == status.HTTP_200_OK

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": "JK",
        "email": "jk@jk.pl",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "is_staff": False,
        "lab_roles": [User.LAB_MANAGER],
    }
    actual = json.loads(json.dumps(response.data))
    assert_timezone_now_gte_datetime(actual.pop("last_login"))

    assert expected == actual

    client, lab_manager = api_client_lab_manager
    url = reverse("user-detail", args=[lab_manager.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": lab_manager.id,
        "username": "MSC",
        "email": "msc@msc.pl",
        "first_name": "Maria",
        "last_name": "Skłodowska-Curie",
        "is_staff": False,
        "lab_roles": [User.LAB_MANAGER],
    }
    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    url = reverse("user-get-current-user-info")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    url = reverse("user-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": "JK",
        "email": "jk@jk.pl",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "is_staff": False,
        "lab_roles": [User.LAB_MANAGER],
    }
    actual = json.loads(json.dumps(response.data))
    assert_timezone_now_gte_datetime(actual.pop("last_login"))

    assert expected == actual

    client, project_manager = api_client_project_manager
    url = reverse("user-detail", args=[project_manager.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": project_manager.id,
        "username": "KO",
        "email": "ko@ko.pl",
        "first_name": "Karol",
        "last_name": "Olszewski",
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    url = reverse("user-get-current-user-info")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": project_manager.id,
        "username": "KO",
        "email": "ko@ko.pl",
        "first_name": "Karol",
        "last_name": "Olszewski",
        "is_staff": False,
        "lab_roles": [User.PROJECT_MANAGER],
    }
    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    url = reverse("user-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": "JK",
        "email": "jk@jk.pl",
        "first_name": "Jan",
        "last_name": "Kowalski",
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, lab_worker = api_client_lab_worker
    url = reverse("user-detail", args=[lab_worker.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": lab_worker.id,
        "username": "ZW",
        "email": "zw@zw.pl",
        "first_name": "Zygmunt",
        "last_name": "Wróblewski",
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    url = reverse("user-get-current-user-info")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": lab_worker.id,
        "username": "ZW",
        "email": "zw@zw.pl",
        "first_name": "Zygmunt",
        "last_name": "Wróblewski",
        "is_staff": False,
        "lab_roles": [User.LAB_WORKER],
    }
    actual = json.loads(json.dumps(response.data))
    assert actual.pop("last_login") is None

    assert expected == actual

    url = reverse("user-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": "JK",
        "email": "jk@jk.pl",
        "first_name": "Jan",
        "last_name": "Kowalski",
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    url = reverse("user-detail", args=[1])
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse("user-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_user(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                     api_client_anon, projects_procedures):
    User.history.all().delete()  # pylint: disable=no-member

    project_procedure1, _ = projects_procedures

    # Basic user
    user_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.PROJECT_MANAGER],
    }
    user = User.objects.create_user(**user_data)

    user_data.pop("password")

    history_data1 = user_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": user.id,
        "is_staff": False,
        "last_login": None,
    }

    client, admin = api_client_admin
    url = reverse("user-detail", args=[admin.id])
    put_data = {
        "username": "IŁ",
        "email": "il@il.pl",
        "password": "MKZPQL9J",
        "first_name": "Ignacy",
        "last_name": "Łukasiewicz",
        "lab_roles": [User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )
    assert response.status_code == status.HTTP_200_OK

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    history_data2 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_user.id,
        "is_staff": True,
        "last_login": None,
    }

    put_data["id"] = admin.id

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    # Check history

    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = response.data["results"]
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Many roles
    url = reverse("user-detail", args=[user.id])
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    # Missing username
    put_data = {
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing email
    put_data = {
        "username": "JŚ",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing password
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Missing first name (ok for everyone)
    url = reverse("user-detail", args=[user.id])
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id
    put_data["first_name"] = "Jędrzej"

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

     # Missing last name (ok for everyone)
    url = reverse("user-detail", args=[user.id])
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id
    put_data["last_name"] = "Śniadecki"

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    # Missing lab roles (ok only for admins which can't be created through the API)
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique username
    put_data = {
        "username": admin.username,
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique email
    put_data = {
        "username": "JŚ",
        "email": admin.email,
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Trying to set `is_staff`
    url = reverse("user-detail", args=[user.id])
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        "is_staff": True,
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    put_data.pop("is_staff")
    assert not db_user_dict.pop("is_staff")

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    # Trying to set `last_login`
    url = reverse("user-detail", args=[user.id])
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        "last_login": mock_datetime_date_today,
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    put_data.pop("last_login")
    assert db_user_dict.pop("last_login") is None

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    # Username too short (<2 characters)
    put_data = {
        "username": "J",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username too long (>4 characters)
    put_data = {
        "username": "JŚAAA",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with lower case letters
    put_data = {
        "username": "JŚo",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with characters outside of the Polish alphabet
    put_data = {
        "username": "JŚÖ",
        "email": "js@js.pl",
        "password": "TDL9QXO5",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too similar to user's attributes
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "sniadecki",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too short (minimum 8 letters)
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "TDL9QXO",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too common
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "password",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password entirely numeric
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "46290123",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Assign the user to some project/procedure as their manager and try to remove their project manager role
    project_procedure1.manager = user
    project_procedure1.save()
    put_data = {
        "username": "JŚ",
        "email": "js@js.pl",
        "password": "C93UAWLR",
        "first_name": "Jędrzej",
        "last_name": "Śniadecki",
        "lab_roles": [User.LAB_MANAGER],
    }
    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Once we change the manager, we're good to go
    project_procedure1.manager = admin
    project_procedure1.save()

    response = client.put(
        url,
        put_data,
    )

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = user.id

    db_user = User.objects.get(pk=response.data["id"])
    db_user_dict = model_to_dict(db_user)

    raw_password = put_data.pop("password")
    db_user_dict.pop("password")

    assert put_data.items() <= db_user_dict.items()
    assert db_user.check_password(raw_password)

    client, lab_manager = api_client_lab_manager
    url = reverse("user-detail", args=[lab_manager.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, project_manager = api_client_project_manager
    url = reverse("user-detail", args=[project_manager.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker
    url = reverse("user-detail", args=[lab_worker.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    url = reverse("user-detail", args=[1])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse("user-detail", args=[user.id])
    response = client.put(
        url,
        {
            "username": "XYZ",
            "email": "xyz@xyz.pl",
            "password": "xyzxyzxy",
            "first_name": "Xyz",
            "last_name": "Zyx",
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_partial_update_user(api_client_admin, api_client_lab_manager, api_client_project_manager,
                             api_client_lab_worker, api_client_anon, projects_procedures):
    User.history.all().delete()  # pylint: disable=no-member

    project_procedure1, _ = projects_procedures

    client, admin = api_client_admin
    url = reverse("user-detail", args=[admin.id])

    # Should be able to update their own info
    response = client.patch(
        url,
        {
            "username": "IŁA",
            "password": "T6BMOT68",
            "lab_roles": [User.PROJECT_MANAGER],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_admin = User.objects.get(pk=admin.id)
    assert "IŁA" == db_admin.username
    assert db_admin.check_password("T6BMOT68")
    assert [User.PROJECT_MANAGER] == db_admin.lab_roles

    # Check history
    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": admin.id,
        "username": "IŁA",
        "email": "il@il.pl",
        "first_name": "Ignacy",
        "last_name": "Łukasiewicz",
        "lab_roles": [User.PROJECT_MANAGER],
        "is_staff": True,
        "last_login": None,
    }]

    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = response.data["results"]
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    # Create a sample user
    url = reverse("user-list")

    # Basic user
    user = User.objects.create_user(
        username="EB",
        email="eb@eb.pl",
        password="WEOMUE7R",
        first_name="Edwart",
        last_name="Bekier",
        lab_roles=[User.PROJECT_MANAGER],
    )

    url = reverse("user-detail", args=[user.id])

    # Update their info as well
    # Many roles
    response = client.patch(
        url,
        {
            "username": "EBA",
            "password": "5AXYC8DK",
            "lab_roles": [User.LAB_MANAGER, User.PROJECT_MANAGER],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_user = User.objects.get(pk=user.id)
    assert "EBA" == db_user.username
    assert db_user.check_password("5AXYC8DK")
    assert db_user.lab_roles == [User.LAB_MANAGER, User.PROJECT_MANAGER]

    # Empty lab roles (ok only for admins)
    admin.lab_roles = [User.PROJECT_MANAGER]
    admin.save()

    url = reverse("user-detail", args=[admin.id])
    response = client.patch(
        url,
        {
           "lab_roles": [],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_admin = User.objects.get(pk=admin.id)
    assert db_admin.lab_roles == []

    url = reverse("user-detail", args=[user.id])
    response = client.patch(
        url,
        {
            "lab_roles": [],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique username
    response = client.patch(
        url,
        {
            "username": admin.username,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Nonunique email
    response = client.patch(
        url,
        {
            "email": admin.email,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

     # Trying to set `is_staff`
    response = client.patch(
        url,
        {
            "is_staff": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_user = User.objects.get(pk=user.id)
    assert not db_user.is_staff

     # Trying to set `last_login`
    response = client.patch(
        url,
        {
            "last_login": mock_datetime_date_today,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_user = User.objects.get(pk=user.id)
    assert db_user.last_login is None

    # Username too short (<2 characters)
    response = client.patch(
        url,
        {
            "username": "E",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

   # Username too long (>4 characters)
    response = client.patch(
        url,
        {
            "username": "EEEBA",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with lower case letters
    response = client.patch(
        url,
        {
            "username": "eBA",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Username with characters outside of the Polish alphabet
    response = client.patch(
        url,
        {
            "username": "EBÄ",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too similar to user's attributes
    response = client.patch(
        url,
        {
            "password": "EdwartBe",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too short (minimum 8 letters)
    response = client.patch(
        url,
        {
            "password": "5AXYC8D",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password too common
    response = client.patch(
        url,
        {
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Password entirely numeric
    response = client.patch(
        url,
        {
            "password": "46290123",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Assign the user to some project/procedure as their manager and try to remove their project manager role
    project_procedure1.manager = user
    project_procedure1.save()

    response = client.patch(
        url,
        {
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Once we change the manager, we're good to go
    project_procedure1.manager = admin
    project_procedure1.save()

    response = client.patch(
        url,
        {
            "lab_roles": [User.LAB_WORKER],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    db_user = User.objects.get(pk=user.id)
    assert [User.LAB_WORKER] == db_user.lab_roles

    client, lab_manager = api_client_lab_manager
    url = reverse("user-detail", args=[lab_manager.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, project_manager = api_client_project_manager
    url = reverse("user-detail", args=[project_manager.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker
    url = reverse("user-detail", args=[lab_worker.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    url = reverse("user-detail", args=[1])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse("user-detail", args=[user.id])
    response = client.patch(
        url,
        {
            "username": "XYZ",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_destroy_user(api_client_admin, api_client_lab_manager, api_client_project_manager,
                      api_client_lab_worker, api_client_anon):
    User.history.all().delete()  # pylint: disable=no-member

    # Basic user
    user_data = {
        "username": "KJ",
        "email": "kj@kj.pl",
        "password": "7EB4L4IB",
        "first_name": "Kazimierz",
        "last_name": "Jabłczyński",
        "lab_roles":[User.LAB_MANAGER],
    }
    user = User.objects.create_user(**user_data)

    client, admin = api_client_admin
    url = reverse("user-detail", args=[user.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(pk=user.id).exists()

    # Check history
    user_data.pop("password")
    expected = [
        user_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": user.id,
        "is_staff": False,
        "last_login": None,
        },
        user_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": user.id,
        "is_staff": False,
        "last_login": None,
        },
    ]

    response = client.get(reverse("user-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # An admin can also remove themselves.
    url = reverse("user-detail", args=[admin.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(pk=admin.id).exists()

    client, lab_manager = api_client_lab_manager
    url = reverse("user-detail", args=[lab_manager.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, project_manager = api_client_project_manager
    url = reverse("user-detail", args=[project_manager.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker
    url = reverse("user-detail", args=[lab_worker.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("user-detail", args=[user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    url = reverse("user-detail", args=[1])
    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse("user-detail", args=[user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
