import os

import pytest

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status


def remove_all_user_manuals():
    user_manual_dir = "UserManuals"
    try:
        all_files_in_user_manual_dir = default_storage.listdir(user_manual_dir)
        for user_manual_filename in all_files_in_user_manual_dir[1]:
            default_storage.delete(os.path.join(user_manual_dir, user_manual_filename))
    except FileNotFoundError:
        pass


@pytest.fixture(autouse=True)
def removing_all_user_manuals():
    remove_all_user_manuals()
    yield
    remove_all_user_manuals()


@pytest.mark.django_db
def test_get_user_manual(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                         api_client_anon, mock_files):
    # Add a sample user manual
    user_manual_expected_path = os.path.join("UserManuals", "user_manual.pdf")
    _, pdf_bytes = mock_files
    default_storage.save(user_manual_expected_path, SimpleUploadedFile("test.pdf", pdf_bytes))

    client, _ = api_client_admin

    url = reverse("user_manual")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    user_manual_url_split = response.data["user_manual"].rsplit("/", maxsplit=2)
    user_manual_actual_path = os.path.join(user_manual_url_split[-2], user_manual_url_split[-1])

    assert user_manual_expected_path == user_manual_actual_path

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert user_manual_expected_path == user_manual_actual_path

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert user_manual_expected_path == user_manual_actual_path

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert user_manual_expected_path == user_manual_actual_path

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert user_manual_expected_path == user_manual_actual_path

    # If the user manual doesn't exist, we should expect HTTP 404 SC
    default_storage.delete(user_manual_expected_path)
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_put_user_manual(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                          api_client_anon, mock_files):
    _, pdf_bytes = mock_files

    # Only admins can add user manuals
    client, _ = api_client_admin

    url = reverse("user_manual")
    put_data = {
        "user_manual": SimpleUploadedFile("test.pdf", pdf_bytes),
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    user_manual_dir = "UserManuals"
    user_manual_filename = "user_manual.pdf"
    user_manual_expected_path = os.path.join(user_manual_dir, user_manual_filename)
    user_manual_url_split = default_storage.url(user_manual_expected_path).rsplit("/", maxsplit=2)
    user_manual_actual_path = os.path.join(user_manual_url_split[-2], user_manual_url_split[-1])

    assert user_manual_expected_path == user_manual_actual_path

    # If we add any file again, the old one should be deleted and a new one added.
    # We'll be able to see that behavior because normally Django would add a new file with a unique suffix.
    all_files_in_user_manual_dir = default_storage.listdir("UserManuals")
    assert 1 == len(all_files_in_user_manual_dir[1])
    assert user_manual_filename == all_files_in_user_manual_dir[1][0]

    put_data = {
        "user_manual": SimpleUploadedFile("test.pdf", pdf_bytes),
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    all_files_in_user_manual_dir = default_storage.listdir("UserManuals")
    assert 1 == len(all_files_in_user_manual_dir[1])
    assert user_manual_filename == all_files_in_user_manual_dir[1][0]

    client, _ = api_client_lab_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
