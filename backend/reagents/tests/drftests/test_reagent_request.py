"""The entire flow is tested in test_notification.py in `test_get_reagent_requests`."""

import json

import pytest

from django.urls import reverse

from rest_framework import status

from reagents.models import PersonalReagent, ReagentRequest
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict


@pytest.mark.django_db
def test_list_and_get_current_user_reagent_requests(api_client_admin, api_client_lab_manager,
                                                    api_client_project_manager, api_client_lab_worker, api_client_anon,
                                                    personal_reagents):
    _, lab_worker = api_client_lab_worker
    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, _ = personal_reagents
    # Basic reagent requests
    reagent_request1_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)
    reagent_request2_data = {
        "requester": lab_worker,
        "personal_reagent": personal_reagent3,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request2 = ReagentRequest.objects.create(**reagent_request2_data)

    url = reverse("reagentrequest-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
        {
            "id": reagent_request2.id,
            "requester": reagent_request2_data["requester"].id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # Filtering
    # `status`
    reagent_request2.status = ReagentRequest.APPROVED
    reagent_request2.save()
    url = f"{reverse('reagentrequest-list')}?status={ReagentRequest.AWAITING_APPROVAL}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-list')}?status={ReagentRequest.APPROVED}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request2.id,
            "requester": reagent_request2_data["requester"].id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.APPROVED,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request2.status = ReagentRequest.REJECTED
    reagent_request2.save()
    url = f"{reverse('reagentrequest-list')}?status={ReagentRequest.REJECTED}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected[0]["status"] = ReagentRequest.REJECTED

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request2.status = ReagentRequest.AWAITING_APPROVAL
    reagent_request2.save()

    # Ordering
    # `id`
    url = f"{reverse('reagentrequest-list')}?ordering=id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
        {
            "id": reagent_request2.id,
            "requester": reagent_request2_data["requester"].id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # `change_status_date`
    url = f"{reverse('reagentrequest-list')}?ordering=change_status_date"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
        {
            "id": reagent_request2.id,
            "requester": reagent_request2_data["requester"].id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-list')}?ordering=-change_status_date"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # Searching
    # `requester__username`
    url = f"{reverse('reagentrequest-list')}?search=IŁ"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # `personal_reagent__reagent__name`
    url = f"{reverse('reagentrequest-list')}?search=alkohol"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "requester": reagent_request1_data["requester"].id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = reverse("reagentrequest-get-current-user-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]
    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))
    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # For quicker filterset checks
    reagent_request2.requester = admin
    reagent_request2.save()

    # Filtering
    # `status`
    reagent_request2.status = ReagentRequest.APPROVED
    reagent_request2.save()
    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?status={ReagentRequest.AWAITING_APPROVAL}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?status={ReagentRequest.APPROVED}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request2.id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.APPROVED,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request2.status = ReagentRequest.REJECTED
    reagent_request2.save()
    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?status={ReagentRequest.REJECTED}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected[0]["status"] = ReagentRequest.REJECTED

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request2.status = ReagentRequest.AWAITING_APPROVAL
    reagent_request2.save()

    # Ordering
    # `id`
    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?ordering=id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
        {
            "id": reagent_request2.id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # `change_status_date`
    # In theory these two cases could fail because the dates will be equal. To prevent that, we sort by `id` as well.
    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?ordering=change_status_date,id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
        {
            "id": reagent_request2.id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?ordering=-change_status_date,-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # Searching
    # `personal_reagent__reagent__name`
    url = f"{reverse('reagentrequest-get-current-user-reagent-requests')}?search=alkohol"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]

    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request2.requester = lab_worker
    reagent_request2.save()

    # With a POST method creating a second request for the same personal reagent would be blocked.
    reagent_request1.delete()

    client, lab_manager = api_client_lab_manager
    reagent_request1_data["requester"] = lab_manager
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)

    url = reverse("reagentrequest-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("reagentrequest-get-current-user-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]
    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))
    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    reagent_request1.delete()

    client, project_manager = api_client_project_manager
    reagent_request1_data["requester"] = project_manager
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)

    url = reverse("reagentrequest-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("reagentrequest-get-current-user-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request1.id,
            "personal_reagent": reagent_request1_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request1_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request1.personal_reagent.reagent.name,
        },
    ]
    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))
    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # The lab worker has already added a request in the beginning of this TC,
    # so we're not going to add a new one and we're not going to delete reagent_request1 this time for anon testing.

    client, lab_worker = api_client_lab_worker
    reagent_request1_data["requester"] = lab_worker

    url = reverse("reagentrequest-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    url = reverse("reagentrequest-get-current-user-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_request2.id,
            "personal_reagent": reagent_request2_data["personal_reagent"].id,
            "status": ReagentRequest.AWAITING_APPROVAL,
            "requester_comment": reagent_request2_data["requester_comment"],
            "responder_comment": "",
            "reagent_name": reagent_request2.personal_reagent.reagent.name,
        },
    ]
    response_data_reagent_requests = response.data["results"]
    for rr in response_data_reagent_requests:
        assert_timezone_now_gte_datetime(rr.pop("change_status_date"))
    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    client = api_client_anon
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)

    url = reverse("reagentrequest-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse("reagentrequest-get-current-user-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    reagent_request1.delete()


@pytest.mark.django_db
def test_create_reagent_request(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                api_client_lab_worker, api_client_anon, personal_reagents):
    ReagentRequest.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, personal_reagent4 = personal_reagents
    url = reverse("reagentrequest-list")

    post_data = {
        "personal_reagent": personal_reagent1.id,
        "requester_comment": "Potrzebuję do badań.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request1 = ReagentRequest.objects.get(pk=response.data["id"])

    assert post_data.items() <= model_to_dict(db_reagent_request1).items()
    assert admin == db_reagent_request1.requester
    assert_timezone_now_gte_datetime(db_reagent_request1.change_status_date)

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_reagent_request1.id,
        "requester": admin.id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "responder_comment": "",
    }

    post_data = {
        "personal_reagent": personal_reagent4.id,
        "requester_comment": "Niezbędny do projektu.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request2 = ReagentRequest.objects.get(pk=response.data["id"])

    assert post_data.items() <= model_to_dict(db_reagent_request2).items()
    assert admin == db_reagent_request2.requester
    assert_timezone_now_gte_datetime(db_reagent_request2.change_status_date)

    history_data2 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_reagent_request2.id,
        "requester": admin.id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "responder_comment": "",
    }

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(
        f"{reverse('reagentrequest-get-historical-records')}?ordering=id"
    )

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    response = client.get(
        f"{reverse('reagentrequest-get-historical-records')}?ordering=-id"
    )

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Ordering
    # `change_status_date`
    response = client.get(
        f"{reverse('reagentrequest-get-historical-records')}?ordering=change_status_date,id"
    )

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    response = client.get(
        f"{reverse('reagentrequest-get-historical-records')}?ordering=-change_status_date,-id"
    )

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Searching
    # `personal_reagent__reagent__name`
    response = client.get(
        f"{reverse('reagentrequest-get-historical-records')}?search=dna"
    )

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    db_reagent_request1.delete()

    client, lab_manager = api_client_lab_manager

    post_data = {
        "personal_reagent": personal_reagent1.id,
        "requester_comment": "Potrzebuję do badań.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    assert post_data.items() <= model_to_dict(db_reagent_request).items()
    assert lab_manager == db_reagent_request.requester
    assert_timezone_now_gte_datetime(db_reagent_request.change_status_date)

    db_reagent_request.delete()

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, project_manager = api_client_project_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    assert post_data.items() <= model_to_dict(db_reagent_request).items()
    assert project_manager == db_reagent_request.requester
    assert_timezone_now_gte_datetime(db_reagent_request.change_status_date)

    db_reagent_request.delete()

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker

    post_data = {
        "personal_reagent": personal_reagent3.id,
        "requester_comment": "Potrzebuję do badań.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    assert post_data.items() <= model_to_dict(db_reagent_request).items()
    assert lab_worker == db_reagent_request.requester
    assert_timezone_now_gte_datetime(db_reagent_request.change_status_date)

    db_reagent_request.delete()

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "personal_reagent": personal_reagent1.id,
        "requester_comment": "Potrzebuję do badań.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to request a personal reagent that belongs to the requester
    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Try to request a personal reagent that is already being requested
    client, _ = api_client_project_manager

    post_data = {
        "personal_reagent": personal_reagent3.id,
        "requester_comment": "Potrzebuję do badań.",
    }
    response = client.post(url, post_data)

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Change the status to approved or rejected and check again
    db_reagent_request.status = ReagentRequest.APPROVED
    db_reagent_request.save()

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    db_reagent_request.delete()
    ReagentRequest.objects.get(pk=response.data["id"]).delete()


@pytest.mark.django_db
def test_retrieve_reagent_request(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                  api_client_lab_worker, api_client_anon, personal_reagents):
    _, lab_worker = api_client_lab_worker
    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, _ = personal_reagents
    # Basic reagent requests
    reagent_request1_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)
    reagent_request2_data = {
        "requester": lab_worker,
        "personal_reagent": personal_reagent3,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request2 = ReagentRequest.objects.create(**reagent_request2_data)

    # Admins can retrieve any reagent request
    url = reverse("reagentrequest-detail", args=[reagent_request1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_request1.id,
        "requester": reagent_request1_data["requester"].id,
        "personal_reagent": reagent_request1_data["personal_reagent"].id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "requester_comment": reagent_request1_data["requester_comment"],
        "responder_comment": "",
        "reagent_name": reagent_request1.personal_reagent.reagent.name,
    }

    response_data_reagent_requests = response.data
    assert_timezone_now_gte_datetime(response_data_reagent_requests.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    url = reverse("reagentrequest-detail", args=[reagent_request2.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_request2.id,
        "requester": reagent_request2_data["requester"].id,
        "personal_reagent": reagent_request2_data["personal_reagent"].id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "requester_comment": reagent_request2_data["requester_comment"],
        "responder_comment": "",
        "reagent_name": reagent_request2.personal_reagent.reagent.name,
    }

    response_data_reagent_requests = response.data
    assert_timezone_now_gte_datetime(response_data_reagent_requests.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    # Users with a lab role can only retrieve their requests
    client, lab_manager = api_client_lab_manager

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request1.delete()
    reagent_request1_data["requester"] = lab_manager
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)

    url = reverse("reagentrequest-detail", args=[reagent_request1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_request1.id,
        "requester": reagent_request1_data["requester"].id,
        "personal_reagent": reagent_request1_data["personal_reagent"].id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "requester_comment": reagent_request1_data["requester_comment"],
        "responder_comment": "",
        "reagent_name": reagent_request1.personal_reagent.reagent.name,
    }

    response_data_reagent_requests = response.data
    assert_timezone_now_gte_datetime(response_data_reagent_requests.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    client, project_manager = api_client_project_manager

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request1.delete()
    reagent_request1_data["requester"] = project_manager
    reagent_request1 = ReagentRequest.objects.create(**reagent_request1_data)

    url = reverse("reagentrequest-detail", args=[reagent_request1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_request1.id,
        "requester": reagent_request1_data["requester"].id,
        "personal_reagent": reagent_request1_data["personal_reagent"].id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "requester_comment": reagent_request1_data["requester_comment"],
        "responder_comment": "",
        "reagent_name": reagent_request1.personal_reagent.reagent.name,
    }

    response_data_reagent_requests = response.data
    assert_timezone_now_gte_datetime(response_data_reagent_requests.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    client, lab_worker = api_client_lab_worker

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # We still have the second reagent request
    url = reverse("reagentrequest-detail", args=[reagent_request2.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_request2.id,
        "requester": reagent_request2_data["requester"].id,
        "personal_reagent": reagent_request2_data["personal_reagent"].id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "requester_comment": reagent_request2_data["requester_comment"],
        "responder_comment": "",
        "reagent_name": reagent_request2.personal_reagent.reagent.name,
    }

    response_data_reagent_requests = response.data
    assert_timezone_now_gte_datetime(response_data_reagent_requests.pop("change_status_date"))

    actual = json.loads(json.dumps(response_data_reagent_requests))

    assert expected == actual

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    reagent_request1.delete()
    reagent_request2.delete()


@pytest.mark.django_db
def test_update_reagent_request(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                api_client_lab_worker, api_client_anon, personal_reagents):
    ReagentRequest.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, _ = personal_reagents
    # Basic reagent requests
    reagent_request_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])
    put_data = {
        "requester_comment": "Potrzebuję pilnie do badań.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    reagent_request_data["requester"] = reagent_request_data["requester"].id
    reagent_request_data["personal_reagent"] = reagent_request_data["personal_reagent"].id
    reagent_request_data["status"] = ReagentRequest.AWAITING_APPROVAL
    reagent_request_data["responder_comment"] = ""
    history_data1 = reagent_request_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": reagent_request.id,
    }

    reagent_request_data["requester_comment"] = put_data["requester_comment"]
    history_data2 = reagent_request_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": reagent_request.id,
    }

    reagent_request_data["id"] = reagent_request.id

    db_reagent_request_dict = model_to_dict(ReagentRequest.objects.get(pk=response.data["id"]))
    assert_timezone_now_gte_datetime(db_reagent_request_dict.pop("change_status_date"))

    assert reagent_request_data == db_reagent_request_dict

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Only admins can change other workers' requests
    client, lab_manager = api_client_lab_manager

    response = client.put(url, reagent_request_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data = {
        "requester": lab_manager,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])
    put_data = {
        "requester_comment": "Potrzebuję bardzo pilnie do badań.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    reagent_request_data["id"] = reagent_request.id
    reagent_request_data["requester"] = reagent_request_data["requester"].id
    reagent_request_data["personal_reagent"] = reagent_request_data["personal_reagent"].id
    reagent_request_data["status"] = ReagentRequest.AWAITING_APPROVAL
    reagent_request_data["requester_comment"] = put_data["requester_comment"]
    reagent_request_data["responder_comment"] = ""

    db_reagent_request_dict = model_to_dict(ReagentRequest.objects.get(pk=response.data["id"]))
    assert_timezone_now_gte_datetime(db_reagent_request_dict.pop("change_status_date"))

    assert reagent_request_data == db_reagent_request_dict

    client, project_manager = api_client_project_manager

    response = client.put(url, reagent_request_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data = {
        "requester": project_manager,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])
    put_data = {
        "requester_comment": "Potrzebuję bardzo bardzo pilnie do badań.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    reagent_request_data["id"] = reagent_request.id
    reagent_request_data["requester"] = reagent_request_data["requester"].id
    reagent_request_data["personal_reagent"] = reagent_request_data["personal_reagent"].id
    reagent_request_data["status"] = ReagentRequest.AWAITING_APPROVAL
    reagent_request_data["requester_comment"] = put_data["requester_comment"]
    reagent_request_data["responder_comment"] = ""

    db_reagent_request_dict = model_to_dict(ReagentRequest.objects.get(pk=response.data["id"]))
    assert_timezone_now_gte_datetime(db_reagent_request_dict.pop("change_status_date"))

    assert reagent_request_data == db_reagent_request_dict

    client, lab_worker = api_client_lab_worker

    response = client.put(url, reagent_request_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data = {
        "requester": lab_worker,
        "personal_reagent": personal_reagent3,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])
    put_data = {
        "requester_comment": "Potrzebuję bardzo bardzo (!!!) pilnie do badań.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    reagent_request_data["id"] = reagent_request.id
    reagent_request_data["requester"] = reagent_request_data["requester"].id
    reagent_request_data["personal_reagent"] = reagent_request_data["personal_reagent"].id
    reagent_request_data["status"] = ReagentRequest.AWAITING_APPROVAL
    reagent_request_data["requester_comment"] = put_data["requester_comment"]
    reagent_request_data["responder_comment"] = ""

    db_reagent_request_dict = model_to_dict(ReagentRequest.objects.get(pk=response.data["id"]))
    assert_timezone_now_gte_datetime(db_reagent_request_dict.pop("change_status_date"))

    assert reagent_request_data == db_reagent_request_dict

    client = api_client_anon

    response = client.put(url, reagent_request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    reagent_request.delete()


@pytest.mark.django_db
def test_partial_update_reagent_request(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                        api_client_lab_worker, api_client_anon, personal_reagents):
    ReagentRequest.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, _ = personal_reagents
    # Basic reagent requests
    reagent_request_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    history_data1 = reagent_request_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": reagent_request.id,
        "requester": admin.id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "responder_comment": "",
    }
    history_data1["personal_reagent"] = reagent_request_data["personal_reagent"].id

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    patch_data = {
        "requester_comment": "Bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert ReagentRequest.objects.get(pk=response.data["id"]).requester_comment == patch_data["requester_comment"]

    history_data2 = history_data1.copy()
    history_data2["history_user"] = admin.id
    history_data2["history_type"] = "~"
    history_data2["requester_comment"] = patch_data["requester_comment"]

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Partial updates can only be done by the requesters (expect for admins)
    client, lab_manager = api_client_lab_manager
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data["requester"] = lab_manager
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    patch_data = {
        "requester_comment": "Bardzo bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert ReagentRequest.objects.get(pk=response.data["id"]).requester_comment == patch_data["requester_comment"]

    client, project_manager = api_client_project_manager
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data["requester"] = project_manager
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    patch_data = {
        "requester_comment": "Bardzo bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert ReagentRequest.objects.get(pk=response.data["id"]).requester_comment == patch_data["requester_comment"]

    client, lab_worker = api_client_lab_worker
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    reagent_request.delete()

    reagent_request_data["requester"] = lab_worker
    reagent_request_data["personal_reagent"] = personal_reagent3
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    patch_data = {
        "requester_comment": "Bardzo bardzo bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert ReagentRequest.objects.get(pk=response.data["id"]).requester_comment == patch_data["requester_comment"]

    client, lab_manager = api_client_lab_manager
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # The admin can partial update, though
    client, admin = api_client_admin

    patch_data = {
        "requester_comment": "Bardzo bardzo bardzo bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert ReagentRequest.objects.get(pk=response.data["id"]).requester_comment == patch_data["requester_comment"]

    client = api_client_anon

    patch_data = {
        "requester_comment": "Bardzo bardzo bardzo bardzo bardzo go potrzebuję do badań.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    reagent_request.delete()


@pytest.mark.django_db
def test_destroy_reagent_request(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                 api_client_lab_worker, api_client_anon, personal_reagents):
    ReagentRequest.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    personal_reagent1, _, personal_reagent3, _ = personal_reagents
    # Basic reagent requests
    reagent_request_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    history_data1 = reagent_request_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": reagent_request.id,
        "requester": admin.id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "responder_comment": "",
    }
    history_data1["personal_reagent"] = reagent_request_data["personal_reagent"].id

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentRequest.objects.filter(pk=reagent_request.id).exists()

    history_data2 = history_data1.copy()
    history_data2["history_user"] = admin.id
    history_data2["history_type"] = "-"

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    # Admins can remove anybody's reagent requests
    client, lab_manager = api_client_lab_manager

    reagent_request_data["requester"] = lab_manager
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    client, admin = api_client_admin
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentRequest.objects.filter(pk=reagent_request.id).exists()

    client, lab_manager = api_client_lab_manager

    reagent_request_data["requester"] = lab_manager
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentRequest.objects.filter(pk=reagent_request.id).exists()

    client, project_manager = api_client_project_manager

    reagent_request_data["requester"] = project_manager
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentRequest.objects.filter(pk=reagent_request.id).exists()

    client, lab_worker = api_client_lab_worker

    reagent_request_data = {
        "requester": lab_worker,
        "personal_reagent": personal_reagent3,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)

    url = reverse("reagentrequest-detail", args=[reagent_request.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentRequest.objects.filter(pk=reagent_request.id).exists()

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_change_reagent_request_status(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                       api_client_lab_worker, api_client_anon, personal_reagents):
    ReagentRequest.history.all().delete()  # pylint: disable=no-member
    PersonalReagent.history.all().delete()  # pylint: disable=no-member

    client, admin = api_client_admin
    personal_reagent1, personal_reagent2, _, _ = personal_reagents
    # Basic reagent requests
    reagent_request_data = {
        "requester": admin,
        "personal_reagent": personal_reagent1,
        "requester_comment": "Potrzebuję do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)
    initial_change_status_date = reagent_request.change_status_date

    history_data1 = reagent_request_data | {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": reagent_request.id,
        "requester": admin.id,
        "status": ReagentRequest.AWAITING_APPROVAL,
        "responder_comment": "",
    }
    history_data1["personal_reagent"] = reagent_request_data["personal_reagent"].id

    url = reverse("reagentrequest-change-reagent-request-status", args=[reagent_request.id])

    # Only the personal reagent's owner (and an admin) can change the status
    client, _ = api_client_lab_manager

    patch_data = {
        "status": ReagentRequest.APPROVED,
        "responder_comment": "Akurat jest mi niepotrzebny.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    assert db_reagent_request.status == patch_data["status"]
    assert db_reagent_request.responder_comment == patch_data["responder_comment"]
    assert db_reagent_request.change_status_date >= initial_change_status_date

    client, _ = api_client_admin

    history_data2 = history_data1.copy()
    history_data2["history_user"] = lab_worker.id
    history_data2["history_type"] = "~"
    history_data2["status"] = ReagentRequest.APPROVED
    history_data2["responder_comment"] = patch_data["responder_comment"]

    # Check history
    response = client.get(reverse("reagentrequest-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))
        assert_timezone_now_gte_datetime(history_row.pop("change_status_date"))

    assert expected == actual

    personal_reagent = db_reagent_request.personal_reagent

    history_data3 = {
        "history_user": lab_worker.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": personal_reagent.id,
        "reagent": {
            "id": personal_reagent.reagent.id,
            "repr": personal_reagent.reagent.name,
        },
        "project_procedure": {
            "id": personal_reagent.project_procedure.id,
            "repr": personal_reagent.project_procedure.name,
        },
        "is_critical": True,
        "main_owner": {
            "id": personal_reagent.main_owner.id,
            "repr": personal_reagent.main_owner.username,
        },
        "lot_no": "2000/02/03",
        "receipt_purchase_date": personal_reagent.receipt_purchase_date.isoformat(),
        "expiration_date": personal_reagent.expiration_date.isoformat(),
        "disposal_utilization_date": None,
        "laboratory": "LGM",
        "room": "315",
        "detailed_location": "Lodówka D17",
        "user_comment": "Bardzo ważny odczynnik.",
        "is_usage_record_generated": False,
        "is_archived": False,
    }

    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, project_manager = api_client_project_manager
    reagent_request_data = {
        "requester": project_manager,
        "personal_reagent": personal_reagent2,
        "requester_comment": "Potrzebuję pilnie do badań.",
    }
    reagent_request = ReagentRequest.objects.create(**reagent_request_data)
    initial_change_status_date = reagent_request.change_status_date

    url = reverse("reagentrequest-change-reagent-request-status", args=[reagent_request.id])

    client, _ = api_client_lab_worker

    patch_data = {
        "status": ReagentRequest.REJECTED,
        "responder_comment": "Nie mogę ci go oddać, bo jest mi bardzo potrzebny.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_reagent_request = ReagentRequest.objects.get(pk=response.data["id"])

    assert db_reagent_request.status == patch_data["status"]
    assert db_reagent_request.responder_comment == patch_data["responder_comment"]
    assert db_reagent_request.change_status_date > initial_change_status_date

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
