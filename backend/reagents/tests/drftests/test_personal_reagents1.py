"""This file tests PersonalReagent and ProjectProcedure."""

import datetime
import json

import pytest

from django.urls import reverse

from rest_framework import status

from reagents.models import Laboratory, PersonalReagent, ProjectProcedure
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict, mock_datetime_date_today


@pytest.mark.django_db
def test_list_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                api_client_lab_worker, api_client_anon, projects_procedures, laboratories,
                                personal_reagents):
    _, project_manager = api_client_project_manager
    _, lab_manager = api_client_lab_manager
    _, lab_worker = api_client_lab_worker

    # Projects/procedures
    project_procedure1, project_procedure2 = projects_procedures

    client, _ = api_client_admin
    url = reverse("projectprocedure-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": project_procedure2.id,
            "name": "PB02 - owce",
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
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('projectprocedure-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('projectprocedure-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": project_procedure2.id,
            "name": "PB02 - owce",
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
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('projectprocedure-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": project_procedure2.id,
            "name": "PB02 - owce",
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
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('projectprocedure-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `name`
    url = f"{reverse('projectprocedure-list')}?ordering=name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": project_procedure2.id,
            "name": "PB02 - owce",
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
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('projectprocedure-list')}?ordering=-name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `name`
    url = f"{reverse('projectprocedure-list')}?search=psy"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Laboratories
    laboratory1, laboratory2 = laboratories

    client, _ = api_client_admin
    url = reverse("laboratory-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": laboratory1.id,
            "laboratory": "LGM",
        },
        {
            "id": laboratory2.id,
            "laboratory": "LG",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('laboratory-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": laboratory1.id,
            "laboratory": "LGM",
        },
        {
            "id": laboratory2.id,
            "laboratory": "LG",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('laboratory-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `laboratory`
    url = f"{reverse('laboratory-list')}?ordering=laboratory"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": laboratory2.id,
            "laboratory": "LG",
        },
        {
            "id": laboratory1.id,
            "laboratory": "LGM",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('laboratory-list')}?ordering=-laboratory"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `laboratory`
    url = f"{reverse('laboratory-list')}?search=LGM"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": laboratory1.id,
            "laboratory": "LGM",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Personal reagents
    personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4 = personal_reagents

    client, admin = api_client_admin
    url = reverse("personal_reagents-list")
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("personal_reagents-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # All filters are tested only here because of the number of lines it takes to test it.
    # Every action uses the same method for filtering anyway (`filter_queryset`),
    # so it'll suffice to check any of the below filters in the remaining actions.

    # Filtering
    # `is_critical`
    url = f"{reverse('personal_reagents-list')}?is_critical=True"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?is_critical=False"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `receipt_purchase_date`
    url = f"{reverse('personal_reagents-list')}?receipt_purchase_date={mock_datetime_date_today.isoformat()}"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?receipt_purchase_date_lt={(mock_datetime_date_today - datetime.timedelta(days=30)).isoformat()}"
    )
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?receipt_purchase_date_lte={(mock_datetime_date_today - datetime.timedelta(days=30)).isoformat()}"
    )
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?receipt_purchase_date_gt={(mock_datetime_date_today - datetime.timedelta(days=15)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?receipt_purchase_date_gte={(mock_datetime_date_today - datetime.timedelta(days=15)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `expiration_date`
    url = (f"{reverse('personal_reagents-list')}"
           f"?expiration_date={(mock_datetime_date_today + datetime.timedelta(days=3)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?expiration_date_lt={(mock_datetime_date_today + datetime.timedelta(days=3)).isoformat()}"
    )
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?expiration_date_lte={(mock_datetime_date_today + datetime.timedelta(days=3)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?expiration_date_gt={(mock_datetime_date_today + datetime.timedelta(days=6)).isoformat()}"
    )
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?expiration_date_gte={(mock_datetime_date_today + datetime.timedelta(days=6)).isoformat()}"
    )
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `disposal_utilization_date`
    url = (f"{reverse('personal_reagents-list')}"
           f"?disposal_utilization_date={(mock_datetime_date_today - datetime.timedelta(days=30)).isoformat()}"
    )
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = []
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.disposal_utilization_date = personal_reagent1.receipt_purchase_date
    personal_reagent1.save()
    personal_reagent2.disposal_utilization_date = personal_reagent2.receipt_purchase_date
    personal_reagent2.save()
    personal_reagent3.disposal_utilization_date = personal_reagent3.receipt_purchase_date
    personal_reagent3.save()

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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=30)).isoformat(),
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?disposal_utilization_date_lt={(mock_datetime_date_today - datetime.timedelta(days=30)).isoformat()}"
    )
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?disposal_utilization_date_lte={(mock_datetime_date_today - datetime.timedelta(days=30)).isoformat()}"
    )
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=30)).isoformat(),
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?disposal_utilization_date_gt={(mock_datetime_date_today - datetime.timedelta(days=15)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": mock_datetime_date_today.isoformat(),
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = (f"{reverse('personal_reagents-list')}"
           f"?disposal_utilization_date_gte={(mock_datetime_date_today - datetime.timedelta(days=15)).isoformat()}"
    )
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": mock_datetime_date_today.isoformat(),
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=15)).isoformat(),
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.disposal_utilization_date = None
    personal_reagent1.is_usage_record_generated = True
    personal_reagent1.save()
    personal_reagent2.disposal_utilization_date = None
    personal_reagent2.save()
    personal_reagent3.disposal_utilization_date = None
    personal_reagent3.save()

    # `is_usage_record_generated`
    url = f"{reverse('personal_reagents-list')}?is_usage_record_generated=True"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": True,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?is_usage_record_generated=False"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.is_usage_record_generated = False
    personal_reagent1.save()

    # `is_archived`
    url = f"{reverse('personal_reagents-list')}?is_archived=True"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?is_archived=False"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `laboratory`
    url = f"{reverse('personal_reagents-list')}?laboratory={laboratory2.id}"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `project_procedure`
    url = f"{reverse('personal_reagents-list')}?project_procedure={project_procedure1.id}"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `main_owner`
    url = f"{reverse('personal_reagents-list')}?main_owner={admin.id}"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `reagent`
    assert personal_reagent3.reagent.id == personal_reagent4.reagent.id
    url = f"{reverse('personal_reagents-list')}?reagent={personal_reagent3.reagent.id}"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `room`
    url = f"{reverse('personal_reagents-list')}?room=315"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `detailed_location`
    url = f"{reverse('personal_reagents-list')}?detailed_location=Lodówka A0"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Test multiple choice
    url = f"{reverse('personal_reagents-list')}?detailed_location=Lodówka A0&detailed_location=Lodówka C3"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `type`
    assert personal_reagent1.reagent.type.id == personal_reagent2.reagent.type.id
    url = f"{reverse('personal_reagents-list')}?type={personal_reagent1.reagent.type.id}"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `producer`
    assert personal_reagent3.reagent.producer.id == personal_reagent4.reagent.producer.id
    url = f"{reverse('personal_reagents-list')}?producer={personal_reagent3.reagent.producer.id}"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `clp_classification`
    assert personal_reagent1_clp_classifications == personal_reagent2_clp_classifications
    url = f"{reverse('personal_reagents-list')}?clp_classification={personal_reagent1_clp_classifications[0]['id']}"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))
    assert expected == actual

    # `cas_no`
    personal_reagent3_reagent = personal_reagent3.reagent
    personal_reagent3_reagent.cas_no = "12345"
    personal_reagent3_reagent.save()

    url = f"{reverse('personal_reagents-list')}?cas_no=12345"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent3_reagent.cas_no = ""
    personal_reagent3_reagent.save()

    # `is_usage_record_required`
    url = f"{reverse('personal_reagents-list')}?is_usage_record_required=True"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?is_usage_record_required=False"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `is_validated_by_admin`
    url = f"{reverse('personal_reagents-list')}?is_validated_by_admin=True"
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
            "catalog_no": personal_reagent2.reagent.catalog_no,
            "main_owner": {
                "id": lab_worker.id,
                "repr": lab_worker.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent2_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?is_validated_by_admin=False"
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
            "catalog_no": personal_reagent3.reagent.catalog_no,
            "main_owner": {
                "id": admin.id,
                "repr": admin.username,
            },
            "project_procedure": None,
            "project_procedure_manager_id": None,
            "clp_classifications": personal_reagent3_clp_classifications,
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
            "user_comment": "",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Removing personal reagents 2 and 3 because they use the same reagent and it'd make it harder to test.
    personal_reagent2.delete()
    personal_reagent3.delete()

    # Ordering
    # `id`
    url = f"{reverse('personal_reagents-list')}?ordering=id"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `reagent__name`
    url = f"{reverse('personal_reagents-list')}?ordering=reagent"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-reagent"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `reagent__producer__abbreviation`
    url = f"{reverse('personal_reagents-list')}?ordering=producer"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-producer"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `main_owner`
    url = f"{reverse('personal_reagents-list')}?ordering=main_owner"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-main_owner"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `reagent__catalog_no`
    url = f"{reverse('personal_reagents-list')}?ordering=catalog_no"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-catalog_no"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `lot_no`
    url = f"{reverse('personal_reagents-list')}?ordering=lot_no"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-lot_no"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `receipt_purchase_date`
    url = f"{reverse('personal_reagents-list')}?ordering=receipt_purchase_date"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-receipt_purchase_date"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `expiration_date`
    url = f"{reverse('personal_reagents-list')}?ordering=expiration_date"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-expiration_date"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `disposal_utilization_date`
    # In PostgreSQL: By default, null values sort as if larger than any non-null value.
    # Source: https://www.postgresql.org/docs/current/queries-order.html
    url = f"{reverse('personal_reagents-list')}?ordering=disposal_utilization_date"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-disposal_utilization_date"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `room`
    personal_reagent1.room = "200"
    personal_reagent1.save()

    url = f"{reverse('personal_reagents-list')}?ordering=room"
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
            "room": "200",
            "detailed_location": "Lodówka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-room"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.room = "315"
    personal_reagent1.save()

    # `detailed_location`
    personal_reagent1.detailed_location = "Zamrażarka D17"
    personal_reagent1.save()

    url = f"{reverse('personal_reagents-list')}?ordering=detailed_location"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
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
            "detailed_location": "Zamrażarka D17",
            "is_critical": True,
            "lot_no": "2000/02/03",
            "receipt_purchase_date": mock_datetime_date_today.isoformat(),
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('personal_reagents-list')}?ordering=-detailed_location"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    personal_reagent1.detailed_location = "Lodówka D17"
    personal_reagent1.save()

    # Searching
    # `reagent__name`
    url = f"{reverse('personal_reagents-list')}?search=alkohol"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `reagent__producer__abbreviation`
    url = f"{reverse('personal_reagents-list')}?search=therm"
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
            "catalog_no": personal_reagent4.reagent.catalog_no,
            "main_owner": {
                "id": lab_manager.id,
                "repr": lab_manager.username,
            },
            "project_procedure": {
                "id": project_procedure1.id,
                "repr": project_procedure1.name,
            },
            "project_procedure_manager_id": project_procedure1.manager.id,
            "clp_classifications": personal_reagent4_clp_classifications,
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
            "user_comment": "Mało ważny odczynnik.",
            "is_usage_record_required": False,
            "is_usage_record_generated": False,
            "disposal_utilization_date": (mock_datetime_date_today - datetime.timedelta(days=46)).isoformat(),
            "is_archived": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `main_owner__username`
    url = f"{reverse('personal_reagents-list')}?search=zw"
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
            "user_comment": "Bardzo ważny odczynnik.",
            "is_usage_record_required": True,
            "is_usage_record_generated": False,
            "disposal_utilization_date": None,
            "is_archived": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_personal_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                  api_client_lab_worker, api_client_anon, reagents):
    # pylint: disable=no-member
    ProjectProcedure.history.all().delete()
    Laboratory.history.all().delete()
    PersonalReagent.history.all().delete()
    # pylint: enable=no-member

    _, admin = api_client_admin
    _, lab_manager = api_client_lab_manager
    _, project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    reagent1, _ = reagents

    # Projects/procedures
    client, _ = api_client_admin
    url = reverse("projectprocedure-list")

    # Admins always POST with `is_validated_by_admin` set to True
    post_data = {
        "name": "PB03 - psy",
        "manager": project_manager.id,
        "workers": [project_manager.id, lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    project_procedure_id = response.data["id"]
    db_project_procedure = ProjectProcedure.objects.get(pk=project_procedure_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_project_procedure.id,
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [],
    }
    history_data2 = history_data1.copy()
    history_data2["history_type"] = "~"
    history_data2["workers"] = [
        {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        {
            "id": lab_worker.id,
            "repr": lab_worker.username,
        },
    ]

    post_data["id"] = project_procedure_id
    assert post_data == model_to_dict(db_project_procedure)

    client, _ = api_client_lab_manager

    post_data = {
        "name": "PB04 - szczury",
        "manager": project_manager.id,
        "workers": [project_manager.id, lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    project_procedure_id = response.data["id"]
    db_project_procedure = ProjectProcedure.objects.get(pk=project_procedure_id)
    post_data["is_validated_by_admin"] = True

    history_data3 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_project_procedure.id,
        "manager": {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        "workers": [],
    }
    history_data4 = history_data3.copy()
    history_data4["history_type"] = "~"
    history_data4["workers"] = [
        {
            "id": project_manager.id,
            "repr": project_manager.username,
        },
        {
            "id": lab_worker.id,
            "repr": lab_worker.username,
        },
    ]

    post_data["id"] = project_procedure_id
    assert post_data == model_to_dict(db_project_procedure)

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data4, history_data3, history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # For easier history filtering
    project_procedure_history = ProjectProcedure.history.all()  # pylint: disable=no-member
    project_procedure_history[0].delete()
    project_procedure_history[1].delete()

    # Ordering
    # `id`
    response = client.get(f"{reverse('projectprocedure-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('projectprocedure-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `name`
    response = client.get(f"{reverse('projectprocedure-get-historical-records')}?ordering=name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('projectprocedure-get-historical-records')}?ordering=-name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `name`
    response = client.get(f"{reverse('projectprocedure-get-historical-records')}?search=PB03")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "name": "PB05 - myszy",
        "manager": project_manager.id,
        "workers": [admin.id, lab_manager.id, project_manager.id, lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    project_procedure_id = response.data["id"]
    db_project_procedure = ProjectProcedure.objects.get(pk=project_procedure_id)
    post_data["id"] = project_procedure_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_project_procedure)

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "name": "PB06 - lisy",
        "manager": project_manager.id,
        "workers": [project_manager.id, lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("projectprocedure-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, _ = api_client_admin

    # The manager must have the project manager role
    post_data = {
        "name": "PB06 - lisy",
        "manager": admin.id,
        "workers": [project_manager.id, lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # The manager must belong to the workers as well
    post_data = {
        "name": "PB06 - lisy",
        "manager": project_manager.id,
        "workers": [lab_worker.id],
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client, _ = api_client_admin
    url = reverse("personal_reagents-list")

    # Laboratory
    client, _ = api_client_admin
    url = reverse("laboratory-list")

    post_data = {
        "laboratory": "LGM",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    laboratory1_id = response.data["id"]
    db_laboratory1 = Laboratory.objects.get(pk=laboratory1_id)

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_laboratory1.id,
    }

    post_data["id"] = laboratory1_id
    assert post_data == model_to_dict(db_laboratory1)

    post_data = {
        "laboratory": "LG",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    laboratory2_id = response.data["id"]
    db_laboratory2 = Laboratory.objects.get(pk=laboratory2_id)

    history_data2 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_laboratory2.id,
    }

    post_data["id"] = laboratory2_id
    assert post_data == model_to_dict(db_laboratory2)

    # Check history
    client, _ = api_client_admin
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('laboratory-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('laboratory-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `laboratory`
    response = client.get(f"{reverse('laboratory-get-historical-records')}?ordering=laboratory")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('laboratory-get-historical-records')}?ordering=-laboratory")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `laboratory`
    response = client.get(f"{reverse('laboratory-get-historical-records')}?search=LGM")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    post_data = {
        "laboratory": "LG",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("laboratory-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, _ = api_client_admin
    url = reverse("personal_reagents-list")

    # Personal reagents
    # We can never set `disposal_utilization_date`, `is_usage_record_generated` and `is_archived`
    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": True,
        "main_owner": lab_worker.id,
        "lot_no": "123",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)),
        "disposal_utilization_date": (mock_datetime_date_today + datetime.timedelta(days=17)),
        "laboratory": laboratory1_id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
        "is_usage_record_generated": True,
        "is_archived": True,
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent_id = response.data["id"]
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False
    post_data["disposal_utilization_date"] = None

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_personal_reagent.id,
        "reagent": {
            "id": reagent1.id,
            "repr": reagent1.name,
        },
        "project_procedure": {
            "id": project_procedure_id,
            "repr": db_project_procedure.name,
        },
        "laboratory": {
            "id": laboratory1_id,
            "repr": db_laboratory1.laboratory,
        },
        "main_owner": {
            "id": lab_worker.id,
            "repr": lab_worker.username,
        },
        "receipt_purchase_date": post_data["receipt_purchase_date"].isoformat(),
        "expiration_date": post_data["expiration_date"].isoformat(),
    }

    post_data["id"] = personal_reagent_id
    assert post_data == model_to_dict(db_personal_reagent)

    client, _ = api_client_lab_manager
    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "1234",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=14)),
        "laboratory": laboratory2_id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent_id = response.data["id"]
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)
    post_data["main_owner"] = lab_manager.id
    post_data["disposal_utilization_date"] = None
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_personal_reagent.id,
        "reagent": {
            "id": reagent1.id,
            "repr": reagent1.name,
        },
        "project_procedure": {
            "id": project_procedure_id,
            "repr": db_project_procedure.name,
        },
        "laboratory": {
            "id": laboratory2_id,
            "repr": db_laboratory2.laboratory,
        },
        "main_owner": {
            "id": lab_manager.id,
            "repr": lab_manager.username,
        },
        "receipt_purchase_date": post_data["receipt_purchase_date"].isoformat(),
        "expiration_date": post_data["expiration_date"].isoformat(),
    }

    post_data["id"] = personal_reagent_id
    assert post_data == model_to_dict(db_personal_reagent)

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `expiration_date`
    response = client.get(f"{reverse('personal_reagents-get-historical-records')}?ordering=expiration_date")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('personal_reagents-get-historical-records')}?ordering=-expiration_date")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `main_owner__username`
    response = client.get(f"{reverse('personal_reagents-get-historical-records')}?search=msc")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager
    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "12345",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=21)),
        "laboratory": laboratory2_id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent_id = response.data["id"]
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)
    post_data["id"] = personal_reagent_id
    post_data["main_owner"] = project_manager.id
    post_data["disposal_utilization_date"] = None
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False

    assert post_data == model_to_dict(db_personal_reagent)

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker
    # Minimal dataset with only required fields
    post_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "lot_no": "123456",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=28)),
        "laboratory": laboratory2_id,
        "room": "314",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent_id = response.data["id"]
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)
    post_data["id"] = personal_reagent_id
    post_data["project_procedure"] = None
    post_data["main_owner"] = lab_worker.id
    post_data["disposal_utilization_date"] = None
    post_data["detailed_location"] = ""
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False
    post_data["user_comment"] = ""

    assert post_data == model_to_dict(db_personal_reagent)

    # We can add multiple items as well
    post_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "lot_no": "123456",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=28)).isoformat(),
        "laboratory": laboratory2_id,
        "room": "314",
    }

    response = client.post(url, [post_data] * 5)

    assert response.status_code == status.HTTP_201_CREATED

    post_data["project_procedure"] = None
    post_data["main_owner"] = lab_worker.id
    post_data["receipt_purchase_date"] = mock_datetime_date_today
    post_data["expiration_date"] = mock_datetime_date_today + datetime.timedelta(days=28)
    post_data["disposal_utilization_date"] = None
    post_data["detailed_location"] = ""
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False
    post_data["user_comment"] = ""

    for personal_reagent in response.data:
        personal_reagent_id = personal_reagent["id"]
        post_data["id"] = personal_reagent_id
        db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)

        assert post_data == model_to_dict(db_personal_reagent)

    # We can't anything over 50 though
    post_data = {
        "reagent": reagent1.id,
        "is_critical": True,
        "lot_no": "123456",
        "receipt_purchase_date": mock_datetime_date_today.isoformat(),
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=28)).isoformat(),
        "laboratory": laboratory2_id,
        "room": "314",
    }

    response = client.post(url, [post_data] * 51)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon
    post_data = {
        "reagent": reagent1.id,
        "is_critical": False,
        "lot_no": "1234567",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=28)),
        "laboratory": laboratory2_id,
        "room": "314",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("personal_reagents-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client, _ = api_client_lab_worker
    # When the main owner wants to add a personal reagent to a project/procedure, they must belong to it.
    db_project_procedure.workers.remove(lab_worker.id)
    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "12345678",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)),
        "laboratory": laboratory1_id,
        "room": "314",
        "detailed_location": "Zamrażarka D17",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    db_project_procedure.workers.add(lab_worker.id)

    # Detailed location must be present if the project/procedure name starts with "PB".
    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "12345678",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)),
        "laboratory": laboratory1_id,
        "room": "314",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "12345678",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)),
        "laboratory": laboratory1_id,
        "room": "314",
        "detailed_location": "",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # It's fine to omit it if the name doesn't start with "PB" though.
    db_project_procedure.name = "myszy"
    db_project_procedure.save()

    post_data = {
        "reagent": reagent1.id,
        "project_procedure": project_procedure_id,
        "is_critical": False,
        "lot_no": "12345678",
        "receipt_purchase_date": mock_datetime_date_today,
        "expiration_date": (mock_datetime_date_today + datetime.timedelta(days=7)),
        "laboratory": laboratory1_id,
        "room": "314",
        "user_comment": "Ważny odczynnik.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    personal_reagent_id = response.data["id"]
    db_personal_reagent = PersonalReagent.objects.get(pk=personal_reagent_id)
    post_data["id"] = personal_reagent_id
    post_data["main_owner"] = lab_worker.id
    post_data["disposal_utilization_date"] = None
    post_data["detailed_location"] = ""
    post_data["is_usage_record_generated"] = False
    post_data["is_archived"] = False

    assert post_data == model_to_dict(db_personal_reagent)
