import datetime
import json

import pytest

from dateutil.relativedelta import relativedelta

from django.urls import reverse

from rest_framework import status

from reagents import models
from reagents.tests.drftests.conftest import mock_datetime_date_today


@pytest.mark.django_db
def test_get_reagents_with_pending_approval(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                            api_client_lab_worker, api_client_anon, reagent_types, producers,
                                            concentrations, units, purities_qualities, storage_conditions, reagents):
    client, _ = api_client_admin
    type1, _, _ = reagent_types
    producer1, _ = producers
    concentration1, _ = concentrations
    unit1, _ = units
    purity_quality1, _ = purities_qualities
    storage_condition1, _ = storage_conditions
    _, reagent2 = reagents

    url = reverse("notifications-get-reagent-fields-with-pending-validation")

    # This endpoint is dedicated to admins because only they can approve reagents and their related fields
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": 1,
            "pk": type1.id,
            "table_name": "ReagentType",
            "value": type1.type,
        },
        {
            "id": 2,
            "pk": producer1.id,
            "table_name": "Producer",
            "value": f"[{producer1.abbreviation}] [{producer1.brand_name}] {producer1.producer_name}",
        },
        {
            "id": 3,
            "pk": concentration1.id,
            "table_name": "Concentration",
            "value": concentration1.concentration,
        },
        {
            "id": 4,
            "pk": unit1.id,
            "table_name": "Unit",
            "value": unit1.unit,
        },
        {
            "id": 5,
            "pk": purity_quality1.id,
            "table_name": "PurityQuality",
            "value": purity_quality1.purity_quality,
        },
        {
            "id": 6,
            "pk": storage_condition1.id,
            "table_name": "StorageCondition",
            "value": storage_condition1.storage_condition,
        },
        {
            "id": 7,
            "pk": reagent2.id,
            "table_name": "Reagent",
            "value": reagent2.name,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    reagent2.is_validated_by_admin = True
    reagent2.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": 1,
            "pk": type1.id,
            "table_name": "ReagentType",
            "value": type1.type,
        },
        {
            "id": 2,
            "pk": producer1.id,
            "table_name": "Producer",
            "value": f"[{producer1.abbreviation}] [{producer1.brand_name}] {producer1.producer_name}",
        },
        {
            "id": 3,
            "pk": concentration1.id,
            "table_name": "Concentration",
            "value": concentration1.concentration,
        },
        {
            "id": 4,
            "pk": unit1.id,
            "table_name": "Unit",
            "value": unit1.unit,
        },
        {
            "id": 5,
            "pk": purity_quality1.id,
            "table_name": "PurityQuality",
            "value": purity_quality1.purity_quality,
        },
        {
            "id": 6,
            "pk": storage_condition1.id,
            "table_name": "StorageCondition",
            "value": storage_condition1.storage_condition,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    reagent2.is_validated_by_admin = False
    reagent2.save()

    client, _ = api_client_lab_manager

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_reagents_with_close_expiration_date(api_client_lab_worker, personal_reagents):
    # The `month` and `year` query params default to the current month and year respectively,
    # which means not passing them will always list the two personal reagents from the test fixture
    # as they are created with `datetime.date.today()` for `expiration_date`.
    client, _ = api_client_lab_worker
    personal_reagent1, personal_reagent2, _, _ = personal_reagents

    url = reverse("notifications-get-reagents-with-close-expiration-date")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": personal_reagent1.expiration_date.isoformat(),
        },
        {
            "id": personal_reagent2.id,
            "reagent_name": personal_reagent2.reagent.name,
            "expiration_date": personal_reagent2.expiration_date.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Archived personal reagents don't appear in the list
    personal_reagent2.is_archived = True
    personal_reagent2.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": personal_reagent1.expiration_date.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent2.is_archived = False
    personal_reagent2.save()

    personal_reagent1.expiration_date = mock_datetime_date_today + datetime.timedelta(days=70)
    personal_reagent1.save()
    personal_reagent2.expiration_date = mock_datetime_date_today + datetime.timedelta(days=80)
    personal_reagent2.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": personal_reagent1.expiration_date.isoformat(),
        },
        {
            "id": personal_reagent2.id,
            "reagent_name": personal_reagent2.reagent.name,
            "expiration_date": personal_reagent2.expiration_date.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    some_next_month_and_year_date1 = mock_datetime_date_today + relativedelta(years=+3, months=+4)
    some_next_month_and_year_date2 = mock_datetime_date_today + relativedelta(years=+3, months=+7)

    personal_reagent1.expiration_date = some_next_month_and_year_date1
    personal_reagent2.expiration_date = some_next_month_and_year_date2
    personal_reagent1.save()
    personal_reagent2.save()

    # `month` and `year` query params
    url = (f"{reverse('notifications-get-reagents-with-close-expiration-date')}"
           f"?month={some_next_month_and_year_date1.month}&year={some_next_month_and_year_date1.year}")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": some_next_month_and_year_date1.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('notifications-get-reagents-with-close-expiration-date')}"
           f"?year={some_next_month_and_year_date1.year}")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": personal_reagent1.expiration_date.isoformat(),
        },
        {
            "id": personal_reagent2.id,
            "reagent_name": personal_reagent2.reagent.name,
            "expiration_date": personal_reagent2.expiration_date.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    some_next_month_and_year_date1 = mock_datetime_date_today + relativedelta(years=+3, months=+7)

    personal_reagent1.expiration_date = some_next_month_and_year_date1
    personal_reagent1.save()

    url = (f"{reverse('notifications-get-reagents-with-close-expiration-date')}"
           f"?month={some_next_month_and_year_date1.month}")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
            "expiration_date": personal_reagent1.expiration_date.isoformat(),
        },
        {
            "id": personal_reagent2.id,
            "reagent_name": personal_reagent2.reagent.name,
            "expiration_date": personal_reagent2.expiration_date.isoformat(),
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # The allowed range for `month` is [1, 12]
    url = f"{reverse('notifications-get-reagents-with-close-expiration-date')}?month=0"
    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    url = f"{reverse('notifications-get-reagents-with-close-expiration-date')}?month=13"
    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # `year` must be at least 1899
    url = f"{reverse('notifications-get-reagents-with-close-expiration-date')}?month=1799"
    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check `no_pagination`
    url = f"{reverse('notifications-get-reagents-with-close-expiration-date')}?no_pagination=true"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual


@pytest.mark.django_db
def test_get_reagents_with_not_generated_usage_records(api_client_lab_worker, personal_reagents):
    client, lab_worker = api_client_lab_worker
    url = reverse("notifications-get-reagents-with-not-generated-usage-records")

    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    # These reagents are not required to to have their usage record generated, so they're not going to show on the list
    personal_reagent3.main_owner = lab_worker
    personal_reagent3.save()
    personal_reagent4.main_owner = lab_worker
    personal_reagent4.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
        },
        {
            "id": personal_reagent2.id,
            "reagent_name": personal_reagent2.reagent.name,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent2.is_usage_record_generated = True
    personal_reagent2.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent_name": personal_reagent1.reagent.name,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.is_usage_record_generated = True
    personal_reagent1.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = []
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Once we mark their reagent as required to have its usage record generated, they're going to appear on the list
    personal_reagent3_reagent = personal_reagent3.reagent
    personal_reagent3_reagent.is_usage_record_required = True
    personal_reagent3_reagent.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent3.id,
            "reagent_name": personal_reagent3.reagent.name,
        },
        {
            "id": personal_reagent4.id,
            "reagent_name": personal_reagent4.reagent.name,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual


@pytest.mark.django_db
def test_get_few_critical_reagents(api_client_lab_worker, personal_reagents):
    client, lab_worker = api_client_lab_worker
    url = reverse("notifications-get-few-critical-reagents")

    personal_reagent1, personal_reagent2, personal_reagent3, _ = personal_reagents

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "reagent_id": personal_reagent1.reagent.id,
            "reagent_name": personal_reagent1.reagent.name,
            "count": 1,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent2.is_critical = True
    personal_reagent2.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "reagent_id": personal_reagent1.reagent.id,
            "reagent_name": personal_reagent1.reagent.name,
            "count": 2,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent3.main_owner = lab_worker
    personal_reagent3.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "reagent_id": personal_reagent1.reagent.id,
            "reagent_name": personal_reagent1.reagent.name,
            "count": 2,
        },
        {
            "reagent_id": personal_reagent3.reagent.id,
            "reagent_name": personal_reagent3.reagent.name,
            "count": 1,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.pk = None
    personal_reagent1._state.adding = True  # pylint: disable=protected-access
    personal_reagent1.save()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "reagent_id": personal_reagent3.reagent.id,
            "reagent_name": personal_reagent3.reagent.name,
            "count": 1,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual


@pytest.mark.django_db
def test_get_reagent_requests(api_client_lab_worker, api_client_admin, api_client_lab_manager, personal_reagents):
    # This tests the whole flow:
    # 1. Create a request (with checking for errors: requesting own reagent and a reagent which was already requested)
    # 2. Check if the responder sees it
    # 3. Try to
    #     a) reject it and see if the ownership isn't transfered
    #     b) accept it and see if the ownership is changed

    client, admin = api_client_admin
    url = reverse("reagentrequest-list")

    personal_reagent1, personal_reagent2, personal_reagent3, _ = personal_reagents

    # The 3rd personal reagent belongs to the admin
    response = client.post(url, {
        "personal_reagent": personal_reagent3.id,
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client, lab_manager = api_client_lab_manager

    lab_manager_requester_comment = ""
    response = client.post(url, {
        "personal_reagent": personal_reagent2.id,
        "requester_comment": lab_manager_requester_comment,
    })

    assert response.status_code == status.HTTP_201_CREATED

    lab_manager_reagent_request = models.ReagentRequest.objects.filter(
        personal_reagent=personal_reagent2, status=models.ReagentRequest.AWAITING_APPROVAL
    ).first()

    client, admin = api_client_admin

    # Requested by the lab manager
    response = client.post(url, {
        "personal_reagent": personal_reagent2.id,
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    admin_requester_comment = "Potrzebny do badań."
    response = client.post(url, {
        "personal_reagent": personal_reagent1.id,
        "requester_comment": admin_requester_comment,
    })

    assert response.status_code == status.HTTP_201_CREATED

    admin_reagent_request = models.ReagentRequest.objects.filter(
        personal_reagent=personal_reagent1, status=models.ReagentRequest.AWAITING_APPROVAL
    ).first()

    client, lab_worker = api_client_lab_worker
    url = reverse("notifications-get-reagent-requests")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": lab_manager_reagent_request.id,
            "requester_comment": lab_manager_requester_comment,
            "requester_name": lab_manager.username,
            "reagent_name": personal_reagent2.reagent.name,
        },
        {
            "id": admin_reagent_request.id,
            "requester_comment": admin_requester_comment,
            "requester_name": admin.username,
            "reagent_name": personal_reagent1.reagent.name,
        },
    ]

    actual = json.loads(json.dumps(response.data["results"]))
    # No access to `change_status_date` becasue the serializer uses `timezone.now` in a HiddenField
    actual[0].pop("change_status_date")
    actual[1].pop("change_status_date")

    assert expected == actual

    # Check that the status can be changed only by the owner (expect for admin)
    client, lab_manager = api_client_lab_manager

    url = reverse("reagentrequest-change-reagent-request-status", args=[lab_manager_reagent_request.id])
    patch_data = {
        "status": "RE",
        "responder_comment": "Dodaj komentarz, dlaczego chcesz ten odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, lab_worker = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert personal_reagent2.main_owner == lab_worker

    url = reverse("reagentrequest-change-reagent-request-status", args=[admin_reagent_request.id])
    response = client.patch(url, {
        "status": "AP",
    })

    assert response.status_code == status.HTTP_200_OK

    personal_reagent1 = models.PersonalReagent.objects.get(pk=personal_reagent1.id)
    assert personal_reagent1.main_owner == admin
