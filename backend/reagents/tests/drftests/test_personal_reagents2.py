"""This file tests PersonalReagent and ProjectProcedure."""

import datetime
import json

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import FileResponse
from django.urls import reverse
from django.utils.text import get_valid_filename

from rest_framework import status

from reagents import generators
from reagents.models import Laboratory, PersonalReagent, ProjectProcedure, Reagent
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict, mock_datetime_date_today


@pytest.mark.django_db
def test_retrieve_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                    api_client_lab_worker, api_client_anon, projects_procedures, laboratories,
                                    personal_reagents):
    _, project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    # Projects/procedures
    project_procedure1, _ = projects_procedures

    client, _ = api_client_admin
    url = reverse("projectprocedure-detail", args=[project_procedure1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": project_procedure1.id,
        "name": "PB01 - psy i koty",
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [
            {
                "id": project_manager.id,
                "repr": project_manager.username,
            },
            {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
        ],
        "is_validated_by_admin": True,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Laboratories
    laboratory1, _ = laboratories

    client, _ = api_client_admin
    url = reverse("laboratory-detail", args=[laboratory1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": laboratory1.id,
        "laboratory": "LGM",
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Personal reagents
    # Depending on the role this view is different for admins/lab managers and project managers/lab workers.
    personal_reagent1, _, _, _ = personal_reagents

    client, _ = api_client_admin
    url = reverse("personal_reagents-detail", args=[personal_reagent1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    personal_reagent1_clp_classifications = [
        {
            "id": clp_classification.id,
            "repr": clp_classification.clp_classification,
        }
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ]
    expected = {
        "id": personal_reagent1.id,
        "reagent": {
            "id": personal_reagent1.reagent.id,
            "repr": personal_reagent1.reagent.name,
        },
        "producer": {
            "id": personal_reagent1.reagent.producer.id,
            "repr": personal_reagent1.reagent.producer.abbreviation,
        },
        "catalog_no": personal_reagent1.reagent.catalog_no,
        "main_owner": {
            "id": lab_worker.id,
            "repr": lab_worker.username,
        },
        "project_procedure": {
            "id": project_procedure1.id,
            "repr": project_procedure1.name,
        },
        "project_procedure_manager_id": project_procedure1.manager.id,
        "clp_classifications": personal_reagent1_clp_classifications,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)).isoformat(),
        "laboratory": {
            "id": laboratory1.id,
            "repr": laboratory1.laboratory,
        },
        "room": "315",
        "detailed_location": "Lodówka D17",
        "is_critical": True,
        "lot_no": "2000/02/03",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)).isoformat(),
        "user_comment": "Bardzo ważny odczynnik.",
        "is_usage_record_required": True,
        "is_usage_record_generated": False,
        "disposal_utilization_date": None,
        "is_archived": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                  api_client_lab_worker, api_client_anon, reagents, projects_procedures,
                                  laboratories, personal_reagents):
    # pylint: disable=no-member
    ProjectProcedure.history.all().delete()
    Laboratory.history.all().delete()
    PersonalReagent.history.all().delete()
    # pylint: enable=no-member

    _, lab_manager = api_client_lab_manager
    _, project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    project_procedure1, _ = projects_procedures

    # Projects/procedures
    client, admin = api_client_admin
    url = reverse("projectprocedure-detail", args=[project_procedure1.id])

    put_data = {
        "name": "PB01 - psy i koty",
        "manager": project_manager.id,
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    put_data = {
        "name": "PB01 - psy i koty",
        "manager": project_manager.id,
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    project_procedure1_id = response.data["id"]
    put_data["is_validated_by_admin"] = True
    db_project_procedure = ProjectProcedure.objects.get(pk=project_procedure1_id)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_project_procedure.id,
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [
            {
                "id": project_manager.id,
                "repr": project_manager.username,
            },
            {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
        ],
    }
    history_data2 = history_data1.copy()
    history_data2["workers"] = [
            {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            {
                "id": project_manager.id,
                "repr": project_manager.username,
            },
            {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
    ]

    put_data["id"] = project_procedure1_id
    assert put_data == model_to_dict(db_project_procedure)

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    put_data = {
        "name": "PB07 - gołębie",
        "manager": project_manager.id,
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    put_data = {
        "name": "PB07 - gołębie",
        "manager": project_manager.id,
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    project_procedure1_id = response.data["id"]
    put_data["id"] = project_procedure1_id
    put_data["is_validated_by_admin"] = True
    db_project_procedure = ProjectProcedure.objects.get(pk=project_procedure1_id)

    assert put_data == model_to_dict(db_project_procedure)

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, admin = api_client_admin

    # The manager must have the project manager role
    put_data = {
        "name": "PB07 - gołębie",
        "manager": admin.id,
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # The manager must belong to the workers as well
    put_data = {
        "name": "PB07 - gołębie",
        "manager": project_manager.id,
        "workers": [lab_manager.id, lab_worker.id],
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Laboratories
    laboratory1, laboratory2 = laboratories

    client, admin = api_client_admin
    url = reverse("laboratory-detail", args=[laboratory1.id])

    put_data = {
        "laboratory": "LN",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    laboratory1_id = response.data["id"]
    db_laboratory = Laboratory.objects.get(pk=laboratory1_id)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_laboratory.id,
    }

    put_data["id"] = laboratory1_id
    assert put_data == model_to_dict(db_laboratory)

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    put_data = {
        "laboratory": "LO",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, admin = api_client_admin

    reagent1, _ = reagents
    personal_reagent1, _, _, _ = personal_reagents

    client, _ = api_client_admin
    url = reverse("personal_reagents-detail", args=[personal_reagent1.id])

    # Personal reagents
    put_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "main_owner": lab_manager.id,
        "lot_no": "2000/02/03",
        "receipt_purchase_date": mock_datetime_date_today,
        "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)),
        "laboratory": laboratory1.id,
        "room": "315",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    personal_reagent1_id = response.data["id"]
    put_data["project_procedure"] = personal_reagent1.project_procedure.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_personal_reagent.id,
        "reagent": {
            "id": reagent1.id,
            "repr": reagent1.name,
        },
        "project_procedure": {
            "id": db_project_procedure.id,
            "repr": db_project_procedure.name,
        },
        "laboratory": {
            "id": db_laboratory.id,
            "repr": db_laboratory.laboratory,
        },
        "main_owner": {
            "id": lab_manager.id,
            "repr": lab_manager.username,
        },
        "receipt_purchase_date": put_data["receipt_purchase_date"].isoformat(),
        "opening_date": put_data["opening_date"].isoformat(),
        "expiration_date": put_data["expiration_date"].isoformat(),
    }

    put_data["id"] = personal_reagent1_id
    assert put_data == model_to_dict(db_personal_reagent)

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, lab_manager = api_client_lab_manager

    put_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "lot_no": "2024/01/22",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)),
        "laboratory": laboratory1.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = personal_reagent1.project_procedure.id
    put_data["main_owner"] = lab_manager.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    # Changing the ownership is only available through PATCH regardless if we send the whole request or only partial
    put_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "main_owner": lab_worker.id,
        "lot_no": "2024/01/22",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)),
        "laboratory": laboratory1.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    assert lab_manager.id == PersonalReagent.objects.get(pk=response.data["id"]).main_owner.id

    put_data = {
        "main_owner": admin.id,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # They can't modify it if they're not the main owner either
    personal_reagent1.main_owner = lab_worker
    personal_reagent1.save()

    put_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "main_owner": lab_worker.id,
        "lot_no": "2024/01/22",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Project/procedure managers can PUT on any personal reagent within their projects/procedures
    client, _ = api_client_project_manager

    put_data = {
        "reagent": reagent1.id,
        "project_procedure": None,
        "is_critical": False,
        "main_owner": project_manager.id,
        "lot_no": "2024/01/22",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=333)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = None
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    # Once it's not part of the procedure they can still modify it if it's their personal reagent, but they can't
    # edit the main_owner field
    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "main_owner": lab_worker.id,
        "lot_no": "2024/01/22",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3333)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = None
    put_data["main_owner"] = project_manager.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    # Once we remove the ownership, they can't modify it at all
    personal_reagent1.project_procedure = None
    personal_reagent1.main_owner = lab_worker
    personal_reagent1.save()

    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "main_owner": lab_worker.id,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3333)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=2222)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = None
    put_data["main_owner"] = lab_worker.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    # They can't change the owner either
    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "main_owner": project_manager.id,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=2222)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = None
    put_data["main_owner"] = lab_worker.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = None
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["is_archived"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    # Archiving a personal reagent automatically changes `disposal_utilization_date` (it can't be changed manually)
    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=2222)),
        "disposal_utilization_date": (mock_datetime_date_today + datetime.timedelta(days=2)),
        "laboratory": laboratory2.id,
        "room": "316",
        "is_archived": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    put_data["id"] = personal_reagent1_id
    put_data["project_procedure"] = None
    put_data["main_owner"] = lab_worker.id
    put_data["opening_date"] = personal_reagent1.opening_date
    put_data["disposal_utilization_date"] = mock_datetime_date_today
    put_data["detailed_location"] = personal_reagent1.detailed_location
    put_data["is_usage_record_generated"] = False
    put_data["user_comment"] = personal_reagent1.user_comment
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent1_id)

    assert put_data == model_to_dict(db_personal_reagent)

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # When the main owner wants to add a personal reagent to a project/procedure, they must belong to it.
    client, admin = api_client_admin

    put_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure1.id,
        "is_critical": False,
        "main_owner": admin.id,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=2222)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Opening date cannot be before the receipt/purchase date
    client, admin = api_client_admin

    put_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "main_owner": admin.id,
        "lot_no": "2024/01/23",
        "receipt_purchase_date": mock_datetime_date_today,
        "opening_date": (mock_datetime_date_today - datetime.timedelta(days=2)),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=2222)),
        "laboratory": laboratory2.id,
        "room": "316",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_partial_update_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                          api_client_lab_worker, api_client_anon, projects_procedures, laboratories,
                                          personal_reagents):
    # pylint: disable=no-member
    ProjectProcedure.history.all().delete()
    Laboratory.history.all().delete()
    PersonalReagent.history.all().delete()
    # pylint: enable=no-member

    _, admin = api_client_admin
    _, lab_manager = api_client_lab_manager
    _, project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    _, project_procedure2 = projects_procedures

    # Projects/procedures
    # Admins and lab managers have the same permissions
    client, _ = api_client_admin
    url = reverse("projectprocedure-detail", args=[project_procedure2.id])

    patch_data = {
        "name": "Dziki",
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_project_procedure = ProjectProcedure.objects.get(pk=response.data["id"])
    assert patch_data["name"] == db_project_procedure.name
    assert patch_data["is_validated_by_admin"] == db_project_procedure.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_project_procedure.id,
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [
            {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            {
                "id": project_manager.id,
                "repr": project_manager.username,
            },
            {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
        ],
    }

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "name": "PB15 - wiewiórki",
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_project_procedure = ProjectProcedure.objects.get(pk=response.data["id"])
    assert patch_data["name"] == db_project_procedure.name
    assert patch_data["is_validated_by_admin"] == db_project_procedure.is_validated_by_admin

    # Project/procedure managers can't modify projects/procedures regardless if they are their assigned managers
    client, _ = api_client_project_manager

    patch_data = {
        "workers": [lab_manager.id, project_manager.id, lab_worker.id],
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    project_procedure2.manager = admin
    project_procedure2.save()

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    patch_data = {
        "workers": [lab_worker.id],
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, _ = api_client_admin

    # The manager must have the project manager role
    patch_data = {
        "manager": admin.id,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # The manager must belong to the workers as well
    patch_data = {
        "name": "PB06 - lisy",
        "manager": project_manager.id,
        "workers": [lab_worker.id],
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Laboratories
    _, laboratory2 = laboratories

    client, _ = api_client_admin
    url = reverse("laboratory-detail", args=[laboratory2.id])

    patch_data = {
        "laboratory": "LP",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_laboratory = Laboratory.objects.get(pk=response.data["id"])

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_laboratory.id,
    }

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "laboratory": "LR",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Personal reagents
    personal_reagent1, _, _, _ = personal_reagents

    # Admins can change anybody's personal reagent
    client, _ = api_client_admin
    url = reverse("personal_reagents-detail", args=[personal_reagent1.id])

    patch_data = {
        "user_comment": "Mało ważny odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["user_comment"] == PersonalReagent.objects.get(pk=response.data["id"]).user_comment

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": personal_reagent1.id,
        "reagent": {
            "id": personal_reagent1.reagent.id,
            "repr": personal_reagent1.reagent.name,
        },
        "project_procedure": {
            "id": personal_reagent1.project_procedure.id,
            "repr": personal_reagent1.project_procedure.name,
        },
        "is_critical": True,
        "main_owner": {
            "id": personal_reagent1.main_owner.id,
            "repr": personal_reagent1.main_owner.username,
        },
        "lot_no": "2000/02/03",
        "receipt_purchase_date": personal_reagent1.receipt_purchase_date.isoformat(),
        "opening_date": personal_reagent1.opening_date.isoformat(),
        "expiration_date": personal_reagent1.expiration_date.isoformat(),
        "disposal_utilization_date": None,
        "laboratory": {
            "id": personal_reagent1.laboratory.id,
            "repr": personal_reagent1.laboratory.laboratory,
        },
        "room": "315",
        "detailed_location": "Lodówka D17",
        "is_usage_record_generated": False,
        "is_archived": False,
    }

    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Archiving a personal reagent automatically changes `disposal_utilization_date` (it can't be changed manually)
    patch_data = {
        "disposal_utilization_date": mock_datetime_date_today - datetime.timedelta(days=4),
        "is_archived": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_personal_reagent = PersonalReagent.objects.get(pk=response.data["id"])

    assert mock_datetime_date_today == db_personal_reagent.disposal_utilization_date
    assert db_personal_reagent.is_archived

    # Lab managers can change the `main_owner` and `is_archived` fields of any personal reagent
    client, _ = api_client_lab_manager

    patch_data = {
        "user_comment": "Bardzo mało ważny odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["user_comment"] != PersonalReagent.objects.get(pk=response.data["id"]).user_comment

    patch_data = {
        "is_archived": True,
        "user_comment": "Bardzo mało ważny odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_personal_reagent = PersonalReagent.objects.get(pk=response.data["id"])
    assert patch_data["is_archived"]
    assert patch_data["user_comment"] != db_personal_reagent.user_comment

    # They can't change it to a person who isn't a project/procedure manager though
    patch_data = {
        "main_owner": lab_manager.id,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    patch_data = {
        "main_owner": project_manager.id,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["main_owner"] == PersonalReagent.objects.get(pk=response.data["id"]).main_owner.id

    # Project/procedure managers can update any personal reagent that's assigned to their project/procedure.
    # As long as it belongs to a project/procedure, the main owner can be changed as well.
    client, _ = api_client_project_manager
    patch_data = {
        "main_owner": lab_worker.id,
        "user_comment": "Super ważny odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["main_owner"] == PersonalReagent.objects.get(pk=response.data["id"]).main_owner.id
    assert patch_data["user_comment"] == PersonalReagent.objects.get(pk=response.data["id"]).user_comment

    # When it's not part of the project/procedure, the same rules apply as for the lab worker,
    # i.e. everything can be changed but the main owner.

    personal_reagent1.project_procedure = None
    personal_reagent1.main_owner = project_manager
    personal_reagent1.save()

    patch_data = {
        "main_owner": lab_worker.id,
        "user_comment": "Bardzo ważny odczynnik.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["main_owner"] != PersonalReagent.objects.get(pk=response.data["id"]).main_owner.id
    assert patch_data["user_comment"] == PersonalReagent.objects.get(pk=response.data["id"]).user_comment

    # Once we change the main owner, no permissions apply
    personal_reagent1.project_procedure = None
    personal_reagent1.main_owner = lab_worker
    personal_reagent1.save()

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    patch_data = {
        "room": "310",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    assert patch_data["room"] == PersonalReagent.objects.get(pk=response.data["id"]).room

    personal_reagent1.main_owner = project_manager
    personal_reagent1.save()

    patch_data = {
        "room": "311",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent1.main_owner = lab_worker
    personal_reagent1.save()

    client = api_client_anon
    patch_data = {
        "room": "312",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                  api_client_lab_worker, api_client_anon, projects_procedures, laboratories,
                                  personal_reagents):
    # pylint: disable=no-member
    ProjectProcedure.history.all().delete()
    Laboratory.history.all().delete()
    PersonalReagent.history.all().delete()
    # pylint: enable=no-member

    # The `project_procedure` and `laboratory` fields in PersonalReagent is protected, so it cannot be deleted
    # before the personal reagent is deleted.

    # Projects/procedures
    projects_procedure1, _ = projects_procedures

    client, _ = api_client_admin
    project_procedeure_id = projects_procedure1.id
    url = reverse("projectprocedure-detail", args=[project_procedeure_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Laboratories
    laboratory1, _ = laboratories

    client, _ = api_client_admin
    laboratory_id = laboratory1.id
    url = reverse("laboratory-detail", args=[laboratory_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Personal reagents
    # We'll copy the instance before each DELETE to demonstrate the removal with different permissions
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    personal_reagent_id = personal_reagent1.id
    personal_reagent1.pk = None
    personal_reagent1._state.adding = True  # pylint: disable=protected-access
    personal_reagent1.save()

    # Admins can remove anybody's personal reagent
    client, admin = api_client_admin
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PersonalReagent.objects.filter(pk=personal_reagent_id).exists()

    history_data1 = {
        "history_user": None,
        "history_change_reason": None,
        "history_type": "+",
        "pk": personal_reagent1.id,
        "reagent": {
            "id": personal_reagent1.reagent.id,
            "repr": personal_reagent1.reagent.name,
        },
        "project_procedure": {
            "id": personal_reagent1.project_procedure.id,
            "repr": personal_reagent1.project_procedure.name,
        },
        "is_critical": True,
        "main_owner": {
            "id": personal_reagent1.main_owner.id,
            "repr": personal_reagent1.main_owner.username,
        },
        "lot_no": "2000/02/03",
        "receipt_purchase_date": personal_reagent1.receipt_purchase_date.isoformat(),
        "opening_date": personal_reagent1.opening_date.isoformat(),
        "expiration_date": personal_reagent1.expiration_date.isoformat(),
        "disposal_utilization_date": None,
        "laboratory": {
            "id": personal_reagent1.laboratory.id,
            "repr": personal_reagent1.laboratory.laboratory,
        },
        "room": "315",
        "detailed_location": "Lodówka D17",
        "user_comment": "Bardzo ważny odczynnik.",
        "is_usage_record_generated": False,
        "is_archived": False,
    }
    history_data2 = history_data1.copy()
    history_data2["history_user"] = admin.id
    history_data2["history_type"] = "-"
    history_data2["pk"] = personal_reagent_id

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Lab managers only their own
    personal_reagent_id = personal_reagent1.id

    client, _ = api_client_lab_manager
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent_id = personal_reagent4.id
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PersonalReagent.objects.filter(pk=personal_reagent_id).exists()

    # Same for project/procedure managers
    # They can't remove anybody's personal reagent, even if it belongs to a project/procedure
    personal_reagent_id = personal_reagent1.id

    client, project_manager = api_client_project_manager
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent1.main_owner = project_manager
    personal_reagent1.save()

    url = reverse("personal_reagents-detail", args=[personal_reagent_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PersonalReagent.objects.filter(pk=personal_reagent_id).exists()

    # Same for lab workers
    personal_reagent_id = personal_reagent3.id

    client, lab_worker = api_client_lab_worker
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent3.main_owner = lab_worker
    personal_reagent3.save()

    url = reverse("personal_reagents-detail", args=[personal_reagent_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PersonalReagent.objects.filter(pk=personal_reagent_id).exists()

    personal_reagent_id = personal_reagent2.id

    client = api_client_anon
    url = reverse("personal_reagents-detail", args=[personal_reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Now we can remove projects/procedures
    projects_procedure1, projects_procedure2 = projects_procedures

    client, _ = api_client_admin
    project_procedeure_id = projects_procedure1.id
    url = reverse("projectprocedure-detail", args=[project_procedeure_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ProjectProcedure.objects.filter(pk=project_procedeure_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": project_procedeure_id,
        "name": "PB01 - psy i koty",
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [],
        "is_validated_by_admin": True,
    }

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager
    project_procedeure_id = projects_procedure2.id
    url = reverse("projectprocedure-detail", args=[project_procedeure_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ProjectProcedure.objects.filter(pk=project_procedeure_id).exists()

    client, _ = api_client_project_manager
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Now we can remove laboratories
    laboratory1, laboratory2 = laboratories

    client, _ = api_client_admin
    laboratory_id = laboratory1.id
    url = reverse("laboratory-detail", args=[laboratory_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Laboratory.objects.filter(pk=laboratory_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": laboratory_id,
        "laboratory": "LGM",
    }

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("laboratory-detail", args=[laboratory2.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_personal_view(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                           api_client_anon, reagents, projects_procedures, laboratories, personal_reagents):
    reagent1, reagent2 = reagents
    project_procedure1, _ = projects_procedures
    laboratory1, laboratory2 = laboratories
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    personal_reagent1_hazard_statements = [
        {
            "id": hazard_statement.id,
            "repr": hazard_statement.code,
        }
        for hazard_statement in personal_reagent1.reagent.hazard_statements.order_by(
            "clp_classification__clp_classification",
            "code",
        )
    ]
    personal_reagent1_precautionary_statements = [
        {
            "id": precautionary_statement.id,
            "repr": precautionary_statement.code,
        }
        for precautionary_statement in personal_reagent1.reagent.precautionary_statements.order_by("code")
    ]
    personal_reagent1_clp_classifications = [
        {
            "id": clp_classification.id,
            "repr": clp_classification.clp_classification,
        }
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ]
    personal_reagent2_hazard_statements = [
        {
            "id": hazard_statement.id,
            "repr": hazard_statement.code,
        }
        for hazard_statement in personal_reagent2.reagent.hazard_statements.order_by(
            "clp_classification__clp_classification",
            "code",
        )
    ]
    personal_reagent2_precautionary_statements = [
        {
            "id": precautionary_statement.id,
            "repr": precautionary_statement.code,
        }
        for precautionary_statement in personal_reagent2.reagent.precautionary_statements.order_by("code")
    ]
    personal_reagent2_clp_classifications = [
        {
            "id": clp_classification.id,
            "repr": clp_classification.clp_classification,
        }
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent2.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ]
    personal_reagent3_hazard_statements = [
        {
            "id": hazard_statement.id,
            "repr": hazard_statement.code,
        }
        for hazard_statement in personal_reagent3.reagent.hazard_statements.order_by(
            "clp_classification__clp_classification",
            "code",
        )
    ]
    personal_reagent3_precautionary_statements = [
        {
            "id": precautionary_statement.id,
            "repr": precautionary_statement.code,
        }
        for precautionary_statement in personal_reagent3.reagent.precautionary_statements.order_by("code")
    ]
    personal_reagent3_clp_classifications = [
        {
            "id": clp_classification.id,
            "repr": clp_classification.clp_classification,
        }
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent3.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ]
    personal_reagent4_hazard_statements = [
        {
            "id": hazard_statement.id,
            "repr": hazard_statement.code,
        }
        for hazard_statement in personal_reagent4.reagent.hazard_statements.order_by(
            "clp_classification__clp_classification",
            "code",
        )
    ]
    personal_reagent4_precautionary_statements = [
        {
            "id": precautionary_statement.id,
            "repr": precautionary_statement.code,
        }
        for precautionary_statement in personal_reagent4.reagent.precautionary_statements.order_by("code")
    ]
    personal_reagent4_clp_classifications = [
        {
            "id": clp_classification.id,
            "repr": clp_classification.clp_classification,
        }
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent4.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ]

    client, _ = api_client_admin
    url = reverse("personal_reagents-get-personal-view")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent3.id,
            "reagent": {
                "id": personal_reagent3.reagent.id,
                "repr": personal_reagent3.reagent.name,
            },
            "producer": {
                "id": personal_reagent3.reagent.producer.id,
                "repr": personal_reagent3.reagent.producer.abbreviation,
            },
            "concentration": None,
            "purity_quality": None,
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "project_procedure": None,
            "hazard_statements": personal_reagent3_hazard_statements,
            "precautionary_statements": personal_reagent3_precautionary_statements,
            "clp_classifications": personal_reagent3_clp_classifications,
            "signal_word": "WRN",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=20)).isoformat(),
            "laboratory": {
                "id": laboratory2.id,
                "repr": laboratory2.laboratory,
            },
            "room": "314",
            "detailed_location": "Lodówka C3",
            "is_critical": True,
            "lot_no": "4000/01/30",
            "receipt_purchase_date": (mock_datetime_date_today - datetime.timedelta(days=15)).isoformat(),
            "opening_date": None,
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent4.id,
            "reagent": {
                "id": personal_reagent4.reagent.id,
                "repr": personal_reagent4.reagent.name,
            },
            "producer": {
                "id": personal_reagent4.reagent.producer.id,
                "repr": personal_reagent4.reagent.producer.abbreviation,
            },
            "concentration": None,
            "purity_quality": None,
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "hazard_statements": personal_reagent4_hazard_statements,
            "precautionary_statements": personal_reagent4_precautionary_statements,
            "clp_classifications": personal_reagent4_clp_classifications,
            "signal_word": "WRN",
            "expiration_date": (mock_datetime_date_today - datetime.timedelta(days=45)).isoformat(),
            "laboratory": {
                "id": laboratory1.id,
                "repr": laboratory1.laboratory,
            },
            "room": "315",
            "detailed_location": "Lodówka D17",
            "is_critical": False,
            "lot_no": "1000/01/01",
            "receipt_purchase_date": (mock_datetime_date_today - datetime.timedelta(days=60)).isoformat(),
            "opening_date": None,
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = []
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent": {
                "id": personal_reagent1.reagent.id,
                "repr": personal_reagent1.reagent.name,
            },
            "producer": {
                "id": personal_reagent1.reagent.producer.id,
                "repr": personal_reagent1.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent1.reagent.concentration.id,
                "repr": personal_reagent1.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent1.reagent.purity_quality.id,
                "repr": personal_reagent1.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent1.reagent.catalog_no,
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "hazard_statements": personal_reagent1_hazard_statements,
            "precautionary_statements": personal_reagent1_precautionary_statements,
            "clp_classifications": personal_reagent1_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)).isoformat(),
            "laboratory": {
                "id": laboratory1.id,
                "repr": laboratory1.laboratory,
            },
            "room": "315",
            "detailed_location": "Lodówka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)).isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
        {
            "id": personal_reagent2.id,
            "reagent": {
                "id": personal_reagent2.reagent.id,
                "repr": personal_reagent2.reagent.name,
            },
            "producer": {
                "id": personal_reagent2.reagent.producer.id,
                "repr": personal_reagent2.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent2.reagent.concentration.id,
                "repr": personal_reagent2.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent2.reagent.purity_quality.id,
                "repr": personal_reagent2.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "project_procedure": None,
            "hazard_statements": personal_reagent2_hazard_statements,
            "precautionary_statements": personal_reagent2_precautionary_statements,
            "clp_classifications": personal_reagent2_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=6)).isoformat(),
            "laboratory": {
                "id": laboratory2.id,
                "repr": laboratory2.laboratory,
            },
            "room": "314",
            "detailed_location": "Lodówka A0",
            "is_critical": False,
            "lot_no": "1000/01/01",
            "receipt_purchase_date": (mock_datetime_date_today - datetime.timedelta(days=30)).isoformat(),
            "opening_date": None,
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_critical`
    url = f"{reverse('personal_reagents-get-personal-view')}?is_critical=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent": {
                "id": personal_reagent1.reagent.id,
                "repr": personal_reagent1.reagent.name,
            },
            "producer": {
                "id": personal_reagent1.reagent.producer.id,
                "repr": personal_reagent1.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent1.reagent.concentration.id,
                "repr": personal_reagent1.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent1.reagent.purity_quality.id,
                "repr": personal_reagent1.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent1.reagent.catalog_no,
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "hazard_statements": personal_reagent1_hazard_statements,
            "precautionary_statements": personal_reagent1_precautionary_statements,
            "clp_classifications": personal_reagent1_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)).isoformat(),
            "laboratory": {
                "id": laboratory1.id,
                "repr": laboratory1.laboratory,
            },
            "room": "315",
            "detailed_location": "Lodówka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)).isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `room`
    url = f"{reverse('personal_reagents-get-personal-view')}?ordering=room"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent2.id,
            "reagent": {
                "id": personal_reagent2.reagent.id,
                "repr": personal_reagent2.reagent.name,
            },
            "producer": {
                "id": personal_reagent2.reagent.producer.id,
                "repr": personal_reagent2.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent2.reagent.concentration.id,
                "repr": personal_reagent2.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent2.reagent.purity_quality.id,
                "repr": personal_reagent2.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "project_procedure": None,
            "hazard_statements": personal_reagent2_hazard_statements,
            "precautionary_statements": personal_reagent2_precautionary_statements,
            "clp_classifications": personal_reagent2_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=6)).isoformat(),
            "laboratory": {
                "id": laboratory2.id,
                "repr": laboratory2.laboratory,
            },
            "room": "314",
            "detailed_location": "Lodówka A0",
            "is_critical": False,
            "lot_no": "1000/01/01",
            "receipt_purchase_date": (mock_datetime_date_today - datetime.timedelta(days=30)).isoformat(),
            "opening_date": None,
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
        {
            "id": personal_reagent1.id,
            "reagent": {
                "id": personal_reagent1.reagent.id,
                "repr": personal_reagent1.reagent.name,
            },
            "producer": {
                "id": personal_reagent1.reagent.producer.id,
                "repr": personal_reagent1.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent1.reagent.concentration.id,
                "repr": personal_reagent1.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent1.reagent.purity_quality.id,
                "repr": personal_reagent1.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent1.reagent.catalog_no,
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "hazard_statements": personal_reagent1_hazard_statements,
            "precautionary_statements": personal_reagent1_precautionary_statements,
            "clp_classifications": personal_reagent1_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)).isoformat(),
            "laboratory": {
                "id": laboratory1.id,
                "repr": laboratory1.laboratory,
            },
            "room": "315",
            "detailed_location": "Lodówka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)).isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual
    url = f"{reverse('personal_reagents-get-personal-view')}?ordering=-room"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `reagent__name`
    personal_reagent2.reagent = reagent2
    personal_reagent2.save()

    url = f"{reverse('personal_reagents-get-personal-view')}?search=alkohol"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": personal_reagent1.id,
            "reagent": {
                "id": personal_reagent1.reagent.id,
                "repr": personal_reagent1.reagent.name,
            },
            "producer": {
                "id": personal_reagent1.reagent.producer.id,
                "repr": personal_reagent1.reagent.producer.abbreviation,
            },
            "concentration": {
                "id": personal_reagent1.reagent.concentration.id,
                "repr": personal_reagent1.reagent.concentration.concentration,
            },
            "purity_quality": {
                "id": personal_reagent1.reagent.purity_quality.id,
                "repr": personal_reagent1.reagent.purity_quality.purity_quality,
            },
            "catalog_no": personal_reagent1.reagent.catalog_no,
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "hazard_statements": personal_reagent1_hazard_statements,
            "precautionary_statements": personal_reagent1_precautionary_statements,
            "clp_classifications": personal_reagent1_clp_classifications,
            "signal_word": "DGR",
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=3)).isoformat(),
            "laboratory": {
                "id": laboratory1.id,
                "repr": laboratory1.laboratory,
            },
            "room": "315",
            "detailed_location": "Lodówka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "opening_date": (mock_datetime_date_today + datetime.timedelta(days=1)).isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent2.reagent = reagent1
    personal_reagent2.save()

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_usage_record_data(personal_reagents):
    personal_reagent1, _, _, _ = personal_reagents

    reagent1 = personal_reagent1.reagent
    personal_reagent1_storage_conditions = ", ".join([
        storage_condition
        for storage_condition in map(lambda x: x.storage_condition, personal_reagent1.reagent.storage_conditions.all())
    ])
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    expected = [
        ["Nazwa odczynnika", reagent1.name],
        ["Producent", reagent1.producer.abbreviation],
        ["Nr katalogowy", reagent1.catalog_no],
        ["Jednostka miary", f"{reagent1.volume} {reagent1.unit}"],
        ["Lot/Batch/Nr serii", personal_reagent1.lot_no],
        ["Data przysłania", personal_reagent1.receipt_purchase_date],
        ["Data ważności", personal_reagent1.expiration_date],
        ["Warunki przechowywania", personal_reagent1_storage_conditions],
        ["Kupujący", personal_reagent1.main_owner],
        ["Pracownia/Pokój", personal_reagent1.room],
        ["Lokalizacja", personal_reagent1.detailed_location],
        ["Klasyfikacja zagrożenia", personal_reagent1_clp_classifications],
        ["Data otwarcia i sprawdzenia", ""],
        ["Osoba sprawdzająca (podpis)", ""],
        ["Uwagi / porcjonowanie", ""],
    ]
    actual = generators.generate_usage_record_data(personal_reagent1)

    assert expected == actual


@pytest.mark.django_db
def test_generate_usage_record(api_client_admin, api_client_lab_manager, api_client_project_manager,
                               api_client_lab_worker, api_client_anon, laboratories, personal_reagents):
    # pylint: disable=no-member
    PersonalReagent.history.all().delete()
    # pylint: enable=no-member

    _, laboratory2 = laboratories
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    # Admins can generate usage records for any personal reagent
    client, admin = api_client_admin
    personal_reagent = personal_reagent2
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    assert PersonalReagent.objects.get(pk=personal_reagent_id).is_usage_record_generated

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": personal_reagent.id,
        "reagent": {
            "id": personal_reagent.reagent.id,
            "repr": personal_reagent.reagent.name,
        },
        "project_procedure": None,
        "is_critical": False,
        "main_owner": {
            "id": personal_reagent.main_owner.id,
            "repr": personal_reagent.main_owner.username,
        },
        "lot_no": "1000/01/01",
        "receipt_purchase_date": personal_reagent.receipt_purchase_date.isoformat(),
        "opening_date": None,
        "expiration_date": personal_reagent.expiration_date.isoformat(),
        "disposal_utilization_date": None,
        "laboratory": {
            "id": laboratory2.id,
            "repr": laboratory2.laboratory,
        },
        "room": "314",
        "detailed_location": "Lodówka A0",
        "user_comment": "",
        "is_usage_record_generated": True,
        "is_archived": False,
    }

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # The rest only for their own (except for those in projects/procedures)
    client, _ = api_client_lab_manager
    personal_reagent = personal_reagent3
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent = personal_reagent4
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    assert PersonalReagent.objects.get(pk=personal_reagent_id).is_usage_record_generated

    client, project_manager = api_client_project_manager
    personal_reagent = personal_reagent3
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent = personal_reagent3
    personal_reagent.main_owner = project_manager
    personal_reagent.save()

    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    assert PersonalReagent.objects.get(pk=personal_reagent_id).is_usage_record_generated

    # This is possible because personal_reagent1 belongs to a project/procedure in which this user is a manager
    personal_reagent = personal_reagent1
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    assert PersonalReagent.objects.get(pk=personal_reagent_id).is_usage_record_generated

    client, _ = api_client_lab_worker
    personal_reagent = personal_reagent3
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    personal_reagent = personal_reagent1
    personal_reagent.is_usage_record_generated = False
    personal_reagent.save()
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    assert PersonalReagent.objects.get(pk=personal_reagent_id).is_usage_record_generated

    client = api_client_anon
    personal_reagent_id = personal_reagent.id
    url = reverse("personal_reagents-generate-usage-record", args=[personal_reagent_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_sanepid_pip_report_data(personal_reagents):
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    reagent1 = personal_reagent1.reagent
    reagent2 = personal_reagent2.reagent
    reagent3 = personal_reagent3.reagent
    reagent4 = personal_reagent4.reagent
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent2_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent2.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent3_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent3.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent4_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent4.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    expected = [
        [
            "Lp.",
            "Nazwa odczynnika",
            "Producent (marka)",
            "Laboratorium",
            "Pracownia/pokój",
            "Główny użytkownik",
            "Data przyjęcia/zakupu",
            "Klasyfikacja CLP",
            "Nr instrukcji bezpieczeństwa",
        ],
        [
            1,
            reagent1.name,
            reagent1.producer.abbreviation,
            personal_reagent1.laboratory.laboratory,
            personal_reagent1.room,
            personal_reagent1.main_owner,
            personal_reagent1.receipt_purchase_date,
            personal_reagent1_clp_classifications,
            reagent1.safety_instruction.name,
        ],
        [
            2,
            reagent2.name,
            reagent2.producer.abbreviation,
            personal_reagent2.laboratory.laboratory,
            personal_reagent2.room,
            personal_reagent2.main_owner,
            personal_reagent2.receipt_purchase_date,
            personal_reagent2_clp_classifications,
            reagent2.safety_instruction.name,
        ],
        [
            3,
            reagent3.name,
            reagent3.producer.abbreviation,
            personal_reagent3.laboratory.laboratory,
            personal_reagent3.room,
            personal_reagent3.main_owner,
            personal_reagent3.receipt_purchase_date,
            personal_reagent3_clp_classifications,
            reagent3.safety_instruction.name,
        ],
        [
            4,
            reagent4.name,
            reagent4.producer.abbreviation,
            personal_reagent4.laboratory.laboratory,
            personal_reagent4.room,
            personal_reagent4.main_owner,
            personal_reagent4.receipt_purchase_date,
            personal_reagent4_clp_classifications,
            reagent4.safety_instruction.name,
        ],
    ]
    actual = generators.generate_sanepid_pip_report_data(PersonalReagent.objects.all())

    assert expected == actual


@pytest.mark.django_db
def test_generate_sanepid_pip_report(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                     api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("personal_reagents-generate-sanepid-pip-report")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_sanepid_pip_{admin.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_manager = api_client_lab_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_sanepid_pip_{lab_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, _ = api_client_project_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_lab_manager_report_data(personal_reagents):
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    reagent1 = personal_reagent1.reagent
    reagent2 = personal_reagent2.reagent
    reagent3 = personal_reagent3.reagent
    reagent4 = personal_reagent4.reagent
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent2_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent2.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent3_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent3.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent4_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent4.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    expected = [
        [
            "Lp.",
            "Nazwa odczynnika",
            "Producent (marka)",
            "Laboratorium",
            "Pracownia/pokój",
            "Główny użytkownik",
            "Data przyjęcia/zakupu",
            "Data ważności",
            "Klasyfikacja CLP",
            "Nr instrukcji bezpieczeństwa",
            "Rodzaj odczynnika",
        ],
        [
            1,
            reagent1.name,
            reagent1.producer.abbreviation,
            personal_reagent1.laboratory.laboratory,
            personal_reagent1.room,
            personal_reagent1.main_owner,
            personal_reagent1.receipt_purchase_date,
            personal_reagent1.expiration_date,
            personal_reagent1_clp_classifications,
            reagent1.safety_instruction.name,
            reagent1.type,
        ],
        [
            2,
            reagent2.name,
            reagent2.producer.abbreviation,
            personal_reagent2.laboratory.laboratory,
            personal_reagent2.room,
            personal_reagent2.main_owner,
            personal_reagent2.receipt_purchase_date,
            personal_reagent2.expiration_date,
            personal_reagent2_clp_classifications,
            reagent2.safety_instruction.name,
            reagent2.type,
        ],
        [
            3,
            reagent3.name,
            reagent3.producer.abbreviation,
            personal_reagent3.laboratory.laboratory,
            personal_reagent3.room,
            personal_reagent3.main_owner,
            personal_reagent3.receipt_purchase_date,
            personal_reagent3.expiration_date,
            personal_reagent3_clp_classifications,
            reagent3.safety_instruction.name,
            reagent3.type,
        ],
        [
            4,
            reagent4.name,
            reagent4.producer.abbreviation,
            personal_reagent4.laboratory.laboratory,
            personal_reagent4.room,
            personal_reagent4.main_owner,
            personal_reagent4.receipt_purchase_date,
            personal_reagent4.expiration_date,
            personal_reagent4_clp_classifications,
            reagent4.safety_instruction.name,
            reagent4.type,
        ],
    ]
    actual = generators.generate_lab_manager_report_data(PersonalReagent.objects.all())

    assert expected == actual


@pytest.mark.django_db
def test_generate_lab_manager_report(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                     api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("personal_reagents-generate-lab-manager-report")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_kierownika_laboratorium_{admin.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_manager = api_client_lab_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_kierownika_laboratorium_{lab_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, _ = api_client_project_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_projects_procedures_report_data(personal_reagents):
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    reagent1 = personal_reagent1.reagent
    reagent2 = personal_reagent2.reagent
    reagent3 = personal_reagent3.reagent
    reagent4 = personal_reagent4.reagent
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent2_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent2.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent3_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent3.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent4_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent4.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    expected = [
        [
            "Lp.",
            "Projekt / procedura",
            "Nazwa odczynnika",
            "Producent (marka)",
            "Laboratorium",
            "Pracownia/pokój",
            "Lokalizacja szczegółowa",
            "Główny użytkownik",
            "Data przyjęcia/zakupu",
            "Data ważności",
            "Klasyfikacja CLP",
        ],
        [
            1,
            personal_reagent1.project_procedure,
            reagent1.name,
            reagent1.producer.abbreviation,
            personal_reagent1.laboratory.laboratory,
            personal_reagent1.room,
            personal_reagent1.detailed_location,
            personal_reagent1.main_owner,
            personal_reagent1.receipt_purchase_date,
            personal_reagent1.expiration_date,
            personal_reagent1_clp_classifications,
        ],
        [
            2,
            personal_reagent2.project_procedure,
            reagent2.name,
            reagent2.producer.abbreviation,
            personal_reagent2.laboratory.laboratory,
            personal_reagent2.room,
            personal_reagent2.detailed_location,
            personal_reagent2.main_owner,
            personal_reagent2.receipt_purchase_date,
            personal_reagent2.expiration_date,
            personal_reagent2_clp_classifications,
        ],
        [
            3,
            personal_reagent3.project_procedure,
            reagent3.name,
            reagent3.producer.abbreviation,
            personal_reagent3.laboratory.laboratory,
            personal_reagent3.room,
            personal_reagent3.detailed_location,
            personal_reagent3.main_owner,
            personal_reagent3.receipt_purchase_date,
            personal_reagent3.expiration_date,
            personal_reagent3_clp_classifications,
        ],
        [
            4,
            personal_reagent4.project_procedure,
            reagent4.name,
            reagent4.producer.abbreviation,
            personal_reagent4.laboratory.laboratory,
            personal_reagent4.room,
            personal_reagent4.detailed_location,
            personal_reagent4.main_owner,
            personal_reagent4.receipt_purchase_date,
            personal_reagent4.expiration_date,
            personal_reagent4_clp_classifications,
        ],
    ]
    actual = generators.generate_projects_procedures_report_data(PersonalReagent.objects.all())

    assert expected == actual


@pytest.mark.django_db
def test_generate_projects_procedures_report(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                             api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("personal_reagents-generate-projects-procedures-report")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_kierownika_projektu_procedury_{admin.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_manager = api_client_lab_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_kierownika_projektu_procedury_{lab_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, project_manager = api_client_project_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_kierownika_projektu_procedury_{project_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, _ = api_client_lab_worker

    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_all_personal_reagents_report_data(personal_reagents):
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    reagent1 = personal_reagent1.reagent
    reagent2 = personal_reagent2.reagent
    reagent3 = personal_reagent3.reagent
    reagent4 = personal_reagent4.reagent
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent1.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent2_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent2.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent3_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent3.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    personal_reagent4_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(
            lambda x: x.clp_classification,
            personal_reagent4.reagent.hazard_statements.distinct(
                "clp_classification__clp_classification"
            ).order_by(
                "clp_classification__clp_classification"
            )
        )
    ])
    expected = [
        [
            "Lp.",
            "Nazwa\n"
            "odczynnika",
            "Producent\n"
            "(marka)",
            "Nr katologowy",
            "LOT",
            "Główny\n"
            "użytkownik",
            "Projekt/\n"
            "procedura",
            "Odczynnik\n"
            "kluczowy",
            "Klasyfikacja CLP",
            "Data przyjęcia/\n"
            "zakupu",
            "Data otwarcia",
            "Data ważności",
            "Data zużycia/\n"
            "utylizacji",
            "Laboratorium",
            "Pracownia/pokój",
            "Lokalizacja\n"
            "szczegółowa",
            "Wymagana\n"
            "karta\n"
            "rozchodu",
            "Wygenerowana\n"
            "karta\n"
            "rozchodu",
            "Uwagi użytkownika",
        ],
        [
            1,
            reagent1.name,
            reagent1.producer.abbreviation,
            reagent1.catalog_no,
            personal_reagent1.lot_no,
            personal_reagent1.main_owner,
            personal_reagent1.project_procedure,
            "Tak",
            personal_reagent1_clp_classifications,
            personal_reagent1.receipt_purchase_date,
            personal_reagent1.opening_date,
            personal_reagent1.expiration_date,
            personal_reagent1.disposal_utilization_date,
            personal_reagent1.laboratory.laboratory,
            personal_reagent1.room,
            personal_reagent1.detailed_location,
            "Tak",
            "Nie",
            personal_reagent1.user_comment,
        ],
        [
            2,
            reagent2.name,
            reagent2.producer.abbreviation,
            reagent2.catalog_no,
            personal_reagent2.lot_no,
            personal_reagent2.main_owner,
            personal_reagent2.project_procedure,
            "Nie",
            personal_reagent2_clp_classifications,
            personal_reagent2.receipt_purchase_date,
            personal_reagent2.opening_date,
            personal_reagent2.expiration_date,
            personal_reagent2.disposal_utilization_date,
            personal_reagent2.laboratory.laboratory,
            personal_reagent2.room,
            personal_reagent2.detailed_location,
            "Tak",
            "Nie",
            personal_reagent2.user_comment,
        ],
        [
            3,
            reagent3.name,
            reagent3.producer.abbreviation,
            reagent3.catalog_no,
            personal_reagent3.lot_no,
            personal_reagent3.main_owner,
            personal_reagent3.project_procedure,
            "Tak",
            personal_reagent3_clp_classifications,
            personal_reagent3.receipt_purchase_date,
            personal_reagent3.opening_date,
            personal_reagent3.expiration_date,
            personal_reagent3.disposal_utilization_date,
            personal_reagent3.laboratory.laboratory,
            personal_reagent3.room,
            personal_reagent3.detailed_location,
            "Nie",
            "Nie dotyczy",
            personal_reagent3.user_comment,
        ],
        [
            4,
            reagent4.name,
            reagent4.producer.abbreviation,
            reagent4.catalog_no,
            personal_reagent4.lot_no,
            personal_reagent4.main_owner,
            personal_reagent4.project_procedure,
            "Nie",
            personal_reagent4_clp_classifications,
            personal_reagent4.receipt_purchase_date,
            personal_reagent4.opening_date,
            personal_reagent4.expiration_date,
            personal_reagent4.disposal_utilization_date,
            personal_reagent4.laboratory.laboratory,
            personal_reagent4.room,
            personal_reagent4.detailed_location,
            "Nie",
            "Nie dotyczy",
            personal_reagent4.user_comment,
        ],
    ]
    actual = generators.generate_all_personal_reagents_report_data(PersonalReagent.objects.all())

    assert expected == actual


@pytest.mark.django_db
def test_generate_all_personal_reagents_report(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                               api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("personal_reagents-generate-all-personal-reagents-report")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_wszystkie_odczynniki_osobiste_{admin.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_manager = api_client_lab_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_wszystkie_odczynniki_osobiste_{lab_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, project_manager = api_client_project_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_wszystkie_odczynniki_osobiste_{project_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_worker = api_client_lab_worker

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_wszystkie_odczynniki_osobiste_{lab_worker.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_personal_view_report_data(personal_reagents):
    personal_reagent1, personal_reagent2, personal_reagent3, _ = personal_reagents

    # To check "Nie dotyczy" in some personal reagent
    personal_reagent3.main_owner = personal_reagent1.main_owner
    personal_reagent3.save()

    reagent1 = personal_reagent1.reagent
    reagent2 = personal_reagent2.reagent
    reagent3 = personal_reagent3.reagent

    personal_reagent1_hazard_statements = reagent1.hazard_statements.order_by(
        "clp_classification__clp_classification",
        "code",
    )
    personal_reagent2_hazard_statements = reagent2.hazard_statements.order_by(
        "clp_classification__clp_classification",
        "code",
    )
    personal_reagent3_hazard_statements = reagent3.hazard_statements.order_by(
        "clp_classification__clp_classification",
        "code",
    )

    personal_reagent1_h_codes = ",\n".join(list(map(lambda x: x.code, personal_reagent1_hazard_statements)))
    personal_reagent1_p_codes = ",\n".join(list(map(
        lambda x: x.code,
        reagent1.precautionary_statements.order_by("code")
    )))
    personal_reagent1_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(lambda x: x.clp_classification, personal_reagent1_hazard_statements)
    ])
    personal_reagent2_h_codes = ",\n".join(list(map(lambda x: x.code, personal_reagent2_hazard_statements)))
    personal_reagent2_p_codes = ",\n".join(list(map(
        lambda x: x.code,
        reagent2.precautionary_statements.order_by("code")
    )))
    personal_reagent2_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(lambda x: x.clp_classification, personal_reagent2_hazard_statements)
    ])
    personal_reagent3_h_codes = ",\n".join(list(map(lambda x: x.code, personal_reagent3_hazard_statements)))
    personal_reagent3_p_codes = ",\n".join(list(map(
        lambda x: x.code,
        reagent3.precautionary_statements.order_by("code")
    )))
    personal_reagent3_clp_classifications = ", ".join([
        clp_classification.clp_classification
        for clp_classification in map(lambda x: x.clp_classification, personal_reagent3_hazard_statements)
    ])
    expected = [
        [
            "Lp.",
            "Nazwa\n"
            "odczynnika",
            "Producent\n"
            "(marka)",
            "Stężenie",
            "Czystość",
            "Nr katologowy",
            "LOT",
            "Projekt/\n"
            "procedura",
            "Odczynnik\n"
            "kluczowy",
            "Kody H",
            "Kody P",
            "Klasyfikacja\n"
            "CLP",
            "Ostrzeżenie",
            "Data przyjęcia/\n"
            "zakupu",
            "Data otwarcia",
            "Data ważności",
            "Data zużycia/\n"
            "utylizacji",
            "Laboratorium",
            "Pracownia/\n"
            "pokój",
            "Lokalizacja\n"
            "szczegółowa",
            "Wymagana\n"
            "karta\n"
            "rozchodu",
            "Wygenerowana\n"
            "karta\n"
            "rozchodu",
            "Uwagi\n"
            "użytkownika",
        ],
        [
            1,
            reagent1.name,
            reagent1.producer.abbreviation,
            reagent1.concentration,
            reagent1.purity_quality,
            reagent1.catalog_no,
            personal_reagent1.lot_no,
            personal_reagent1.project_procedure,
            "Tak",
            personal_reagent1_h_codes,
            personal_reagent1_p_codes,
            personal_reagent1_clp_classifications,
            "DGR",
            personal_reagent1.receipt_purchase_date,
            personal_reagent1.opening_date,
            personal_reagent1.expiration_date,
            personal_reagent1.disposal_utilization_date,
            personal_reagent1.laboratory.laboratory,
            personal_reagent1.room,
            personal_reagent1.detailed_location,
            "Tak",
            "Nie",
            personal_reagent1.user_comment,
        ],
        [
            2,
            reagent2.name,
            reagent2.producer.abbreviation,
            reagent2.concentration,
            reagent2.purity_quality,
            reagent2.catalog_no,
            personal_reagent2.lot_no,
            personal_reagent2.project_procedure,
            "Nie",
            personal_reagent2_h_codes,
            personal_reagent2_p_codes,
            personal_reagent2_clp_classifications,
            "DGR",
            personal_reagent2.receipt_purchase_date,
            personal_reagent2.opening_date,
            personal_reagent2.expiration_date,
            personal_reagent2.disposal_utilization_date,
            personal_reagent2.laboratory.laboratory,
            personal_reagent2.room,
            personal_reagent2.detailed_location,
            "Tak",
            "Nie",
            personal_reagent2.user_comment,
        ],
        [
            3,
            reagent3.name,
            reagent3.producer.abbreviation,
            reagent3.concentration,
            reagent3.purity_quality,
            reagent3.catalog_no,
            personal_reagent3.lot_no,
            personal_reagent3.project_procedure,
            "Tak",
            personal_reagent3_h_codes,
            personal_reagent3_p_codes,
            personal_reagent3_clp_classifications,
            "WRN",
            personal_reagent3.receipt_purchase_date,
            personal_reagent3.opening_date,
            personal_reagent3.expiration_date,
            personal_reagent3.disposal_utilization_date,
            personal_reagent3.laboratory.laboratory,
            personal_reagent3.room,
            personal_reagent3.detailed_location,
            "Nie",
            "Nie dotyczy",
            personal_reagent3.user_comment,
        ],
    ]
    actual = generators.generate_personal_view_report_data(
        PersonalReagent.objects.filter(main_owner=personal_reagent1.main_owner).order_by("id")
    )

    assert expected == actual


@pytest.mark.django_db
def test_generate_personal_view_report(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                       api_client_lab_worker, api_client_anon):
    client, admin = api_client_admin
    url = reverse("personal_reagents-generate-personal-view-report")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_moje_odczynniki_osobiste_{admin.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_manager = api_client_lab_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_moje_odczynniki_osobiste_{lab_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, project_manager = api_client_project_manager

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_moje_odczynniki_osobiste_{project_manager.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client, lab_worker = api_client_lab_worker

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response, FileResponse)
    assert response.as_attachment
    expected_filename = f"raport_moje_odczynniki_osobiste_{lab_worker.username}.pdf"
    assert get_valid_filename(expected_filename) == response.filename

    client = api_client_anon

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_generate_statistics(api_client_admin, api_client_lab_manager, api_client_project_manager,
                             api_client_lab_worker, api_client_anon, reagent_types, producers, safety_data_sheets,
                             safety_instructions, units, storage_conditions, reagents, projects_procedures,
                             laboratories):
    # Using personal reagents from the main test fixture wouldn't be enough to test this action thoroughly.
    # That's why we're going to create a lot more mock personal reagents for this method specifically.
    # We'll also reverse the usual order of users making requests based on their roles because admins get most of the
    # overall statistics.

    reagent_type1, _, _ = reagent_types
    producer1, _ = producers
    safety_instruction1, _ = safety_instructions
    safety_data_sheet1, _ = safety_data_sheets
    unit1, _ = units
    storage_condition1, _ = storage_conditions
    reagent1, reagent2 = reagents
    project_procedure1, project_procedure2 = projects_procedures
    laboratory1, laboratory2 = laboratories

    client = api_client_anon
    url = reverse("personal_reagents-generate-statistics")

    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, lab_worker = api_client_lab_worker
    url = reverse("personal_reagents-list")

    lab_worker_personal_reagent1 = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure1.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    lab_worker_personal_reagent2 = {
        "reagent": reagent2.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    lab_worker_personal_reagents = [lab_worker_personal_reagent1] * 3 + [lab_worker_personal_reagent2] * 5
    response = client.post(url, lab_worker_personal_reagents)

    assert response.status_code == status.HTTP_201_CREATED

    posted_personal_reagents = response.data

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": lab_worker.username,
                },
                "data": [
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 5,
                    },
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [],
    }
    actual = response.data

    assert expected == actual

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[0]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2020, 1, 1)
    personal_reagent.save()

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": lab_worker.username,
                },
                "data": [
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 5,
                    },
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[1]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2020, 2, 25)
    personal_reagent.save()

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[2]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2021, 6, 27)
    personal_reagent.save()

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[3]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2020, 12, 27)
    personal_reagent.save()

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": lab_worker.username,
                },
                "data": [
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 5,
                    },
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 1,
                    },
                ],
            },
            {
                "agg_fields": {
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    lab_worker_personal_reagents = expected["worker_personal_reagents"][0]
    lab_worker_disposed_utilized_personal_reagents = []
    for agg in expected["worker_disposed_utilized_personal_reagents"]:
        agg["agg_fields"] = {
            "username": lab_worker.username,
            "year": agg["agg_fields"]["year"],
        }
        lab_worker_disposed_utilized_personal_reagents.append(agg)

    client, project_manager = api_client_project_manager

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [],
        "worker_disposed_utilized_personal_reagents": [],
        "project_procedure_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
        ],
        "project_procedure_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    url = reverse("personal_reagents-list")

    project_manager_personal_reagent1 = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure1.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    project_manager_personal_reagent2 = {
        "reagent": reagent2.id,
        "project_procedure": project_procedure2.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    project_manager_personal_reagents = ([project_manager_personal_reagent1] * 6
                                         + [project_manager_personal_reagent2] * 7)
    response = client.post(url, project_manager_personal_reagents)

    assert response.status_code == status.HTTP_201_CREATED

    posted_personal_reagents = response.data

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[0]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2021, 12, 30)
    personal_reagent.save()

    personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[1]["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2021, 12, 30)
    personal_reagent.save()

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": project_manager.username,
                },
                "data": [
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 7,
                    },
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 6,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                ],
            },
        ],
        "project_procedure_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 9,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                },
                "data": [
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 7,
                    },
                ],
            },
        ],
        "project_procedure_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    url = reverse("personal_reagents-list")

    project_manager_personal_reagent1 = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure2.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    project_manager_personal_reagents = [project_manager_personal_reagent1] * 13
    response = client.post(url, project_manager_personal_reagents)

    assert response.status_code == status.HTTP_201_CREATED

    posted_personal_reagents = response.data

    for i in range(5):
        personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[i]["id"])
        personal_reagent.disposal_utilization_date = datetime.date(2020, 12, 31)
        personal_reagent.save()

    for i in range(5, 12):
        personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[i]["id"])
        personal_reagent.disposal_utilization_date = datetime.date(2021, 12, 31)
        personal_reagent.save()

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": project_manager.username,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 19,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 7,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 9,
                    },
                ],
            },
            {
                "agg_fields": {
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 5,
                    },
                ],
            },
        ],
        "project_procedure_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 13,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 7,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 9,
                    },
                ],
            },
        ],
        "project_procedure_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 7,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 5,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    project_manager_personal_reagents = expected["worker_personal_reagents"][0]
    project_manager_disposed_utilized_personal_reagents = []
    for agg in expected["worker_disposed_utilized_personal_reagents"]:
        agg["agg_fields"] = {
            "username": project_manager.username,
            "year": agg["agg_fields"]["year"],
        }
        project_manager_disposed_utilized_personal_reagents.append(agg)

    client, lab_manager = api_client_lab_manager

    url = reverse("personal_reagents-list")

    project_manager_personal_reagent1 = {
        "reagent": reagent1.id,
        "is_critical": True,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
        "laboratory": laboratory1.id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
    }
    response = client.post(url, project_manager_personal_reagent1)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent = PersonalReagent.objects.get(pk=response.data["id"])
    personal_reagent.disposal_utilization_date = datetime.date(2020, 12, 31)
    personal_reagent.save()

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "worker_personal_reagents": [
            {
                "agg_fields": {
                    "username": lab_manager.username,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
        "worker_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
        "project_procedure_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 13,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 7,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 9,
                    },
                ],
            },
        ],
        "project_procedure_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 7,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure2.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 5,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 3,
                    },
                ],
            },
            {
                "agg_fields": {
                    "project_procedure_name": project_procedure1.name,
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 2,
                    },
                ],
            },
        ],
        "laboratory_personal_reagents": [
            {
                "agg_fields": {
                    "laboratory": "LGM",
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 23,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 12,
                    },
                ],
            },
        ],
        "laboratory_disposed_utilized_personal_reagents": [
            {
                "agg_fields": {
                    "laboratory": "LGM",
                    "year": 2021,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 10,
                    },
                ],
            },
            {
                "agg_fields": {
                    "laboratory": "LGM",
                    "year": 2020,
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 8,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 1,
                    },
                ],
            },
        ],
        "top10_laboratory_personal_reagents": [
            {
                "agg_fields": {
                    "laboratory": "LGM",
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 23,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 12,
                    },
                ],
            },
        ],
        "top20_laboratory_personal_reagents": [
            {
                "agg_fields": {
                    "laboratory": "LGM",
                },
                "data": [
                    {
                        "reagent_name": reagent1.name,
                        "catalog_no": reagent1.catalog_no,
                        "count": 23,
                    },
                    {
                        "reagent_name": reagent2.name,
                        "catalog_no": reagent2.catalog_no,
                        "count": 12,
                    },
                ],
            },
        ],
    }
    actual = response.data

    assert expected == actual

    url = reverse("personal_reagents-list")

    worker_personal_reagents = [
        {
            "agg_fields": {
                "username": lab_manager.username,
            },
            "data": [],
        },
    ]
    worker_disposed_utilized_personal_reagents = [
        {
            "agg_fields": {
                "year": 2019,
            },
            "data": [],
        },
    ]
    laboratory_personal_reagents = [
        {
            "agg_fields": {
                "laboratory": "LG",
            },
            "data": [],
        },
    ]
    laboratory_disposed_utilized_personal_reagents = [
        {
            "agg_fields": {
                "laboratory": "LG",
                "year": 2019,
            },
            "data": [],
        },
    ]
    top10_laboratory_personal_reagents = [
        {
            "agg_fields": {
                "laboratory": "LG",
            },
            "data": [],
        },
    ]
    top20_laboratory_personal_reagents = [
        {
            "agg_fields": {
                "laboratory": "LG",
            },
            "data": [],
        },
    ]
    for i in range(50, 29, -1):
        url = reverse("reagent-list")
        post_data = {
            "type": reagent_type1.id,
            "producer": producer1.id,
            "name": "Agaroza",
            "catalog_no": f"42{i}",
            "volume": 100,
            "unit": unit1.id,
            "storage_conditions": [storage_condition1.id],
            "safety_instruction": safety_instruction1.id,
            "safety_data_sheet": safety_data_sheet1.id,
            "is_usage_record_required": True,
        }
        response = client.post(url, post_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED

        reagent = Reagent.objects.get(pk=response.data["id"])

        lab_manager_personal_reagent1 = {
            "reagent": reagent.id,
            "is_critical": True,
            "lot_no": "123",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)).isoformat(),
            "laboratory": laboratory2.id,
            "room": "314",
            "detailed_location": "Zamrażarka D17",
        }
        lab_manager_personal_reagents = [lab_manager_personal_reagent1] * i

        url = reverse("personal_reagents-list")
        response = client.post(url, lab_manager_personal_reagents)

        posted_personal_reagents = response.data

        for j in range(i):
            personal_reagent = PersonalReagent.objects.get(pk=posted_personal_reagents[j]["id"])
            personal_reagent.disposal_utilization_date = datetime.date(2019, 12, 31)
            personal_reagent.save()

        worker_personal_reagents[0]["data"].append({
            "reagent_name": reagent.name,
            "catalog_no": reagent.catalog_no,
            "count": i,
        })
        worker_disposed_utilized_personal_reagents[0]["data"].append({
            "reagent_name": reagent.name,
            "catalog_no": reagent.catalog_no,
            "count": i,
        })
        laboratory_personal_reagents[0]["data"].append({
            "reagent_name": reagent.name,
            "catalog_no": reagent.catalog_no,
            "count": i,
        })
        laboratory_disposed_utilized_personal_reagents[0]["data"].append({
            "reagent_name": reagent.name,
            "catalog_no": reagent.catalog_no,
            "count": i,
        })
        if i > 40:
            top10_laboratory_personal_reagents[0]["data"].append({
                "reagent_name": reagent.name,
                "catalog_no": reagent.catalog_no,
                "count": i,
            })
        if i > 30:
            top20_laboratory_personal_reagents[0]["data"].append({
                "reagent_name": reagent.name,
                "catalog_no": reagent.catalog_no,
                "count": i,
            })

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected["worker_personal_reagents"][0]["data"] = (
        worker_personal_reagents[0]["data"] + expected["worker_personal_reagents"][0]["data"]
    )
    expected["worker_disposed_utilized_personal_reagents"] = (
        worker_disposed_utilized_personal_reagents + expected["worker_disposed_utilized_personal_reagents"]
    )
    expected["laboratory_personal_reagents"] = (
        laboratory_personal_reagents + expected["laboratory_personal_reagents"]
    )
    expected["laboratory_disposed_utilized_personal_reagents"] = (
        laboratory_disposed_utilized_personal_reagents + expected["laboratory_disposed_utilized_personal_reagents"]
    )
    expected["top10_laboratory_personal_reagents"] = (
        top10_laboratory_personal_reagents + expected["top10_laboratory_personal_reagents"]
    )
    expected["top20_laboratory_personal_reagents"] = (
        top20_laboratory_personal_reagents + expected["top20_laboratory_personal_reagents"]
    )
    actual = response.data

    assert expected == actual

    lab_manager_personal_reagents = expected["worker_personal_reagents"][0]
    lab_manager_disposed_utilized_personal_reagents = []
    for agg in expected["worker_disposed_utilized_personal_reagents"]:
        agg["agg_fields"] = {
            "username": lab_manager.username,
            "year": agg["agg_fields"]["year"],
        }
        lab_manager_disposed_utilized_personal_reagents.append(agg)

    client, _ = api_client_admin

    url = reverse("personal_reagents-generate-statistics")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected["worker_personal_reagents"] = []
    expected["worker_disposed_utilized_personal_reagents"] = []
    expected["global_personal_reagents"] = [
        lab_manager_personal_reagents,
        project_manager_personal_reagents,
        lab_worker_personal_reagents,
    ]

    expected["global_disposed_utilized_personal_reagents"] = (
        lab_manager_disposed_utilized_personal_reagents
        + project_manager_disposed_utilized_personal_reagents
        + lab_worker_disposed_utilized_personal_reagents
    )
    actual = response.data

    assert expected == actual
